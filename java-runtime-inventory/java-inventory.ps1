# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File java-inventory.ps1 [-Roots C:\,D:\] [-Out result.csv] [-Quick] [-NoContainers] [-ContainerFilter name] [-Offline]
#   -Roots            folders to search, comma separated (default: every fixed drive)
#   -Quick            search only Program Files, Program Files (x86), ProgramData and the user profile folder
#   -NoContainers     do not look inside running Docker containers
#   -ContainerFilter  look only inside containers whose name contains this text
#   -Offline          do not look up the latest builds on the internet (status column stays empty)
# Finds every Java runtime on this PC or server and writes vendor, full build version, architecture
# and running process IDs to a CSV file, then checks each runtime for current security problems.
#   1) java.exe files on disk (including runtimes bundled with products)
#   2) runtimes used by running java processes
#   3) JAVA_HOME, PATH and the JavaSoft registry keys
#   4) bin/java inside running Docker containers
# Checks per runtime:
#   latest_build, status  the vendor's latest build for the same Java version, from https://endoflife.date
#                         (compares feature.interim.update, then the patch level after it; the date is when
#                          that source last saw a release, so newer vendor notices may exist)
#   emudhra_roots         eMudhra root certificates still in cacerts (CVE-2026-91403, CVE-2026-114820)
#   java4shell            Java4Shell (CVE-2026-114938): JDK 17/21/25/27 up to the last affected build, on an x86-64
#                         CPU with AVX-512 VBMI; running JVMs are checked for -XX:UseAVX=0/1/2 or
#                         -XX:-UseBASE64Intrinsics (JAVA_TOOL_OPTIONS and other option files are not read)
# Each java found is started once with -version, and keytool once with -list. Nothing else is changed.
# Run from an elevated prompt to see every process and folder.
param(
  [string[]]$Roots,
  [string]$Out,
  [switch]$Quick,
  [switch]$NoContainers,
  [string]$ContainerFilter = "",
  [switch]$Offline
)
$ErrorActionPreference = "SilentlyContinue"
$hostName = $env:COMPUTERNAME
if (-not $Out) { $Out = "java-inventory-$hostName.csv" }
$osName = (Get-CimInstance Win32_OperatingSystem).Caption + " " + (Get-CimInstance Win32_OperatingSystem).Version

if ($Roots) {
  # "-File ... -Roots C:\,D:\" arrives as one string; split it here
  $Roots = $Roots | ForEach-Object { $_ -split "," } | ForEach-Object { $_.Trim() } | Where-Object { $_ }
} elseif ($Quick) {
  $Roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:ProgramData, $env:USERPROFILE) | Where-Object { $_ }
} else {
  $Roots = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object { $_.DeviceID + "\" }
}

# Runs a program and returns stdout and stderr lines together (java prints -version to stderr).
function Invoke-Capture([string]$file, [string]$arguments) {
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $file
  $psi.Arguments = $arguments
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.CreateNoWindow = $true
  try {
    $proc = [System.Diagnostics.Process]::Start($psi)
    $errTask = $proc.StandardError.ReadToEndAsync()
    $text = $proc.StandardOutput.ReadToEnd()
    $proc.WaitForExit()
    ($text + "`n" + $errTask.Result) -split "`r?`n"
  } catch { @() }
}

function Read-JavaProps([string[]]$lines) {
  $get = {
    param($key)
    $m = $lines | Where-Object { $_ -match ("^\s*" + [regex]::Escape($key) + " = (.*)$") } | Select-Object -First 1
    if ($m) { ($m -replace ("^\s*" + [regex]::Escape($key) + " = "), "").Trim() } else { "" }
  }
  $version = & $get "java.version"
  if (-not $version -and $lines) { $version = "$($lines[0])".Trim() }
  [pscustomobject]@{
    Vendor = & $get "java.vendor"
    Version = $version
    Build = & $get "java.runtime.version"
    Arch = & $get "os.arch"
  }
}

# eMudhra roots that the OpenJDK and Oracle alerts remove (CVE-2026-91403, CVE-2026-114820).
$emudhraCNs = @("emSign Root CA - G1", "emSign Root CA - G2", "emSign ECC Root CA - G3", "AAA Certificate Services")
# $ownerLines: the "Owner: " lines of keytool -list -v. Empty means keytool or cacerts was not found.
function Get-EmudhraResult([string[]]$ownerLines) {
  $owners = @($ownerLines | Where-Object { $_ -like "Owner: *" })
  if ($owners.Count -eq 0) { return "not checked (no keytool or cacerts)" }
  $hits = $emudhraCNs | Where-Object { $cn = "CN=$_,"; $owners | Where-Object { $_.Contains($cn) } }
  if ($hits) { "FOUND: " + ($hits -join "; ") } else { "none" }
}
function Get-HostOwnerLines([string]$javaExe) {
  $binDir = Split-Path $javaExe
  $homeDir = Split-Path $binDir
  $keytool = Join-Path $binDir "keytool.exe"
  $ks = Join-Path $homeDir "lib\security\cacerts"
  if (-not (Test-Path -LiteralPath $ks)) { $ks = Join-Path $homeDir "jre\lib\security\cacerts" }
  if (-not (Test-Path -LiteralPath $keytool) -or -not (Test-Path -LiteralPath $ks)) { return @() }
  Invoke-Capture $keytool ("-J-Duser.language=en -J-Duser.country=US -list -v -keystore `"$ks`" -storepass changeit") |
    Where-Object { $_ -like "Owner: *" }
}

# Latest builds per vendor from endoflife.date. java.vendor -> product name there.
$vendorProduct = @{
  "Eclipse Adoptium" = "eclipse-temurin"; "Oracle Corporation" = "oracle-jdk"; "Amazon.com Inc." = "amazon-corretto"
  "Red Hat, Inc." = "redhat-build-of-openjdk"; "Microsoft" = "microsoft-build-of-openjdk"; "BellSoft" = "bellsoft-liberica"
  "SAP SE" = "sapmachine"; "IBM Corporation" = "ibm-semeru-runtime"
}
$eolCache = @{}
$today = (Get-Date).Date
[Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12

# Version key: Java 8 -> (8, update); Java 9+ -> every number before "+" or "-" (feature, interim, update, patch...).
# Works for runtime and vendor strings.
function Get-VersionKey([string]$s) {
  if ($s -match "^(1\.8|8u|8\.|8$)") {
    $u = [regex]::Matches($s, "\d+") | ForEach-Object { [int]$_.Value } | Where-Object { $_ -ge 100 } | Select-Object -First 1
    if ($null -eq $u) { $u = 0 }
    return @(8, $u)
  }
  $k = @([regex]::Matches(($s -split "[+-]")[0], "\d+") | ForEach-Object { [int]$_.Value })
  if ($k.Count -eq 0) { return $null }
  while ($k.Count -lt 3) { $k += 0 }
  return $k
}
function Compare-Key($a, $b, [int]$from, [int]$to) {
  for ($i = $from; $i -lt $to; $i++) {
    $x = if ($i -lt $a.Count) { $a[$i] } else { 0 }
    $y = if ($i -lt $b.Count) { $b[$i] } else { 0 }
    if ($x -lt $y) { return -1 }
    if ($x -gt $y) { return 1 }
  }
  0
}
# older | newer | equal | patch (same update, but the vendor has a later patch build such as 21.0.13.0.3)
function Compare-Build($key, $lkey) {
  $m = if ($key[0] -eq 8 -and $key.Count -eq 2) { 2 } else { 3 }
  $c = Compare-Key $key $lkey 0 $m
  if ($c -lt 0) { return "older" }
  if ($c -gt 0) { return "newer" }
  if ($m -eq 2) { return "equal" }
  if ($key.Count -gt 3) {
    $c = Compare-Key $key $lkey 3 ([Math]::Max($key.Count, $lkey.Count))
    if ($c -lt 0) { return "older" } elseif ($c -gt 0) { return "newer" } else { return "equal" }
  }
  if (@($lkey | Select-Object -Skip 3 | Where-Object { $_ -gt 0 }).Count -gt 0) { return "patch" }
  "equal"
}
function Test-DatePast($v) {
  if ($v -is [bool]) { return $v }
  if ("$v" -match "^\d{4}-\d{2}-\d{2}$") { return ([datetime]"$v") -lt $today }
  $false
}
function Get-LatestStatus([string]$vendor, [string]$build) {
  if ($Offline) { return @("", "") }
  $product = $vendorProduct[$vendor]
  if (-not $product) { return @("", "check manually (no vendor data for '$vendor'; for OS packages use the OS security notices)") }
  if (-not $eolCache.ContainsKey($product)) {
    $eolCache[$product] = $null
    try { $eolCache[$product] = Invoke-RestMethod -Uri "https://endoflife.date/api/$product.json" -TimeoutSec 15 } catch { }
  }
  $data = $eolCache[$product]
  if (-not $data) { return @("", "not checked (could not download latest builds)") }
  $key = Get-VersionKey $build
  if (-not $key) { return @("", "check manually (version not read)") }
  $entry = $data | Where-Object { "$($_.cycle)" -eq "$($key[0])" } | Select-Object -First 1
  if (-not $entry) { return @("", "check manually (no data for Java $($key[0]))") }
  $latest = "$($entry.latest) ($($entry.latestReleaseDate))"
  if ((Test-DatePast $entry.eol) -and -not ("$($entry.extendedSupport)" -match "^\d{4}" -and -not (Test-DatePast $entry.extendedSupport))) {
    return @($latest, "end of support ($($entry.eol))")
  }
  $note = ""
  if ((Test-DatePast $entry.eol)) { $note = " (free support ended $($entry.eol); paid extended support only)" }
  if ("$($entry.latestReleaseDate)" -match "^\d{4}-\d{2}-\d{2}$" -and ([datetime]$entry.latestReleaseDate) -lt $today.AddDays(-120)) {
    return @($latest, "check manually (vendor data last updated $($entry.latestReleaseDate))")
  }
  switch (Compare-Build $key (Get-VersionKey "$($entry.latest)")) {
    "older" { return @($latest, "update needed$note") }
    "patch" { return @($latest, "check manually (vendor has a later patch build of the same update)$note") }
  }
  @($latest, "up to date as of $($entry.latestReleaseDate)$note")
}

# Java4Shell (CVE-2026-114938): OpenJDK Base64 decoder, x86-64 CPUs with AVX-512 VBMI only.
# Last affected builds per the OpenJDK advisory of 2026-11-17; later builds are fixed.
$j4sLastAffected = @{ 17 = @(17, 0, 21, 0, 3); 21 = @(21, 0, 13, 0, 3); 25 = @(25, 0, 5, 0, 3); 27 = @(27, 0, 1, 0, 3) }
# $cpu: yes | no | unknown (AVX-512 VBMI). $mit / $run: running PIDs with / without a mitigation option.
function Get-Java4Shell([string]$build, [string]$arch, [string]$cpu, [string]$mit, [string]$run) {
  $key = Get-VersionKey $build
  if (-not $key) { return "check manually (version not read)" }
  $major = $key[0]
  if ($major -eq 8) {
    if ($build -match "perf") { return "check manually (Oracle 8 -perf build: 8u513-perf or later is fixed)" }
    return "not affected (Java 8)"
  }
  if ($major -lt 17) { return "not affected (Java $major)" }
  if (-not $j4sLastAffected.ContainsKey($major)) { return "check manually (Java $major is out of support; move to a supported version)" }
  if ((Compare-Key $key $j4sLastAffected[$major] 0 ([Math]::Max($key.Count, 5))) -gt 0) { return "fixed (build is after the affected range)" }
  if ($arch -and $arch -notmatch "^(amd64|x86_64)$") { return "not affected (not x86-64: $arch)" }
  if ($cpu -eq "no") { return "not affected (CPU has no AVX-512 VBMI)" }
  $what = if ($cpu -eq "yes") { "AFFECTED" } else { "AFFECTED if CPU has AVX-512 VBMI (CPU not checked)" }
  if ($run) { return "$what (running without mitigation: PID $run)" }
  if ($mit) { return "$what (running JVMs use a temporary mitigation: PID $mit; still update)" }
  "$what (update needed)"
}
# Splits running PIDs into "with mitigation option" and "without", from their command lines.
function Split-Mitigation($procList) {
  $mit = @(); $run = @()
  foreach ($p in $procList) {
    if ("$($p.CommandLine)" -match "-XX:UseAVX=[012]\b|-XX:-UseBASE64Intrinsics") { $mit += $p.ProcessId } else { $run += $p.ProcessId }
  }
  @(($mit -join " "), ($run -join " "))
}

function New-Row([string]$where, [string]$path, $info, [string]$pids, [string]$emudhra, [string]$j4s) {
  $ls = Get-LatestStatus $info.Vendor $info.Build
  [pscustomobject]@{
    host = $hostName; os = $osName; where = $where; java_path = $path
    vendor = $info.Vendor; version = $info.Version; runtime_build = $info.Build; arch = $info.Arch; running_pids = $pids
    latest_build = $ls[0]; status = $ls[1]; emudhra_roots = $emudhra; java4shell = $j4s
  }
}

# 1) disk
$found = New-Object System.Collections.Generic.HashSet[string] ([System.StringComparer]::OrdinalIgnoreCase)
foreach ($root in $Roots) {
  Get-ChildItem -LiteralPath $root -Filter java.exe -File -Recurse -Force |
    Where-Object { $_.Directory.Name -eq "bin" } |
    ForEach-Object { [void]$found.Add($_.FullName) }
}

# 2) running processes
$procs = Get-CimInstance Win32_Process -Filter "Name='java.exe' OR Name='javaw.exe'" | Where-Object { $_.ExecutablePath }
foreach ($p in $procs) {
  $exe = Join-Path (Split-Path $p.ExecutablePath) "java.exe"
  if (Test-Path -LiteralPath $exe) { [void]$found.Add($exe) }
}

# 3) JAVA_HOME, PATH, registry
$homes = @($env:JAVA_HOME)
foreach ($key in "HKLM:\SOFTWARE\JavaSoft", "HKLM:\SOFTWARE\WOW6432Node\JavaSoft") {
  Get-ChildItem -Path $key -Recurse | ForEach-Object { $homes += (Get-ItemProperty -LiteralPath $_.PSPath).JavaHome }
}
foreach ($h in ($homes | Where-Object { $_ })) {
  $exe = Join-Path $h "bin\java.exe"
  if (Test-Path -LiteralPath $exe) { [void]$found.Add((Get-Item -LiteralPath $exe).FullName) }
}
Get-Command java.exe -All -CommandType Application | ForEach-Object {
  # skip the Oracle launcher stubs that only forward to an installed runtime
  if ($_.Source -notmatch "\\javapath\\") { [void]$found.Add($_.Source) }
}

$hostRuntimes = @()
foreach ($exe in ($found | Sort-Object)) {
  $hostRuntimes += [pscustomobject]@{ Exe = $exe; Info = (Read-JavaProps (Invoke-Capture $exe "-XshowSettings:properties -version")) }
}
# CPU features as the JVM sees them (-Xlog exists from Java 9). One runtime is enough for this host.
$hostCpu = "unknown"
foreach ($r in $hostRuntimes) {
  $k = Get-VersionKey $r.Info.Build
  if (-not $k -or $k[0] -lt 9) { continue }
  $cpuLine = Invoke-Capture $r.Exe "-Xlog:os+cpu -version" | Where-Object { $_ -match "os,cpu.*CPU:" } | Select-Object -First 1
  if ($cpuLine) { $hostCpu = if ($cpuLine -match "avx512_vbmi") { "yes" } else { "no" }; break }
}
$rows = @()
foreach ($r in $hostRuntimes) {
  $binDir = Split-Path $r.Exe
  $mine = @($procs | Where-Object { (Split-Path $_.ExecutablePath) -eq $binDir })
  $pids = ($mine | ForEach-Object { $_.ProcessId }) -join " "
  $mr = Split-Mitigation $mine
  $rows += New-Row "host" $r.Exe $r.Info $pids (Get-EmudhraResult (Get-HostOwnerLines $r.Exe)) (Get-Java4Shell $r.Info.Build $r.Info.Arch $hostCpu $mr[0] $mr[1])
}

# 4) running Docker containers (Linux containers)
if (-not $NoContainers -and (Get-Command docker -CommandType Application)) {
  # no double quotes inside: Windows PowerShell does not pass them to native programs reliably
  $probe = "find / -xdev \( -path /proc -o -path /sys \) -prune -o \( -type f -o -type l \) -name java -path '*/bin/java' -print 2>/dev/null | while IFS= read -r j; do readlink -f `$j; done | sort -u | while IFS= read -r j; do echo @@ `$j; `$j -XshowSettings:properties -version 2>&1; h=`${j%/bin/java}; k=`$h/lib/security/cacerts; [ -f `$k ] || k=`$h/jre/lib/security/cacerts; [ -x `$h/bin/keytool ] && `$h/bin/keytool -J-Duser.language=en -J-Duser.country=US -list -v -keystore `$k -storepass changeit 2>/dev/null | grep '^Owner: '; cl=`$(`$j -Xlog:os+cpu -version 2>&1 | grep 'os,cpu.*CPU:' | head -1); if [ `${#cl} -gt 0 ]; then case `$cl in *avx512_vbmi*) echo @CPU yes ;; *) echo @CPU no ;; esac; elif grep -q avx512vbmi /proc/cpuinfo 2>/dev/null; then echo @CPU yes; elif [ -r /proc/cpuinfo ]; then echo @CPU no; fi; for d in /proc/[0-9]*; do [ `$(readlink -f `$d/exe 2>/dev/null)x = `${j}x ] || continue; c=`$(tr '\000' ' ' < `$d/cmdline 2>/dev/null); case `$c in *-XX:UseAVX=[012]*|*-XX:-UseBASE64Intrinsics*) echo @MIT `${d#/proc/} ;; *) echo @RUN `${d#/proc/} ;; esac; done; done"
  $psArgs = "ps --format {{.Names}}|{{.Image}}"
  if ($ContainerFilter) { $psArgs += " --filter name=$ContainerFilter" }
  $containers = Invoke-Capture "docker" $psArgs | Where-Object { $_ -match "\|" }
  foreach ($c in $containers) {
    $name, $image = "$c".Split("|", 2)
    $outLines = Invoke-Capture "docker" ("exec $name sh -c `"$probe`"")
    $path = $null; $buf = @()
    foreach ($line in @($outLines) + "@@ ") {
      if ($line.StartsWith("@@ ")) {
        if ($path) {
          $info = Read-JavaProps $buf
          $cCpu = "unknown"
          $cl = $buf | Where-Object { $_ -like "@CPU *" } | Select-Object -First 1
          if ($cl) { $cCpu = $cl.Substring(5).Trim() }
          $cMit = ($buf | Where-Object { $_ -like "@MIT *" } | ForEach-Object { $_.Substring(5).Trim() }) -join " "
          $cRun = ($buf | Where-Object { $_ -like "@RUN *" } | ForEach-Object { $_.Substring(5).Trim() }) -join " "
          $cPids = (@($cMit, $cRun) | Where-Object { $_ }) -join " "
          $rows += New-Row "container:$name ($image)" $path $info $cPids (Get-EmudhraResult $buf) (Get-Java4Shell $info.Build $info.Arch $cCpu $cMit $cRun)
        }
        $path = $line.Substring(3); $buf = @()
      } else { $buf += $line }
    }
  }
}

$rows | Export-Csv -LiteralPath $Out -NoTypeInformation -Encoding UTF8
"Found $($rows.Count) Java runtime(s). Result file: $Out"
$rows | Format-Table where, vendor, runtime_build, latest_build, status, emudhra_roots, java4shell, running_pids, java_path -AutoSize | Out-String -Width 320
exit 0
