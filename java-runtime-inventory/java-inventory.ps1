# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File java-inventory.ps1 [-Roots C:\,D:\] [-Out result.csv] [-Quick] [-NoContainers] [-ContainerFilter name]
#   -Roots            folders to search (default: every fixed drive)
#   -Quick            search only Program Files, Program Files (x86), ProgramData and the user profile folder
#   -NoContainers     do not look inside running Docker containers
#   -ContainerFilter  look only inside containers whose name contains this text
# Finds every Java runtime on this PC or server and writes vendor, full build version, architecture
# and running process IDs to a CSV file.
#   1) java.exe files on disk (including runtimes bundled with products)
#   2) runtimes used by running java processes
#   3) JAVA_HOME, PATH and the JavaSoft registry keys
#   4) bin/java inside running Docker containers
# Each java found is started once with -version to read its version. Nothing else is changed.
# Run from an elevated prompt to see every process and folder.
param(
  [string[]]$Roots,
  [string]$Out,
  [switch]$Quick,
  [switch]$NoContainers,
  [string]$ContainerFilter = ""
)
$ErrorActionPreference = "SilentlyContinue"
$hostName = $env:COMPUTERNAME
if (-not $Out) { $Out = "java-inventory-$hostName.csv" }
$osName = (Get-CimInstance Win32_OperatingSystem).Caption + " " + (Get-CimInstance Win32_OperatingSystem).Version

if (-not $Roots) {
  if ($Quick) {
    $Roots = @($env:ProgramFiles, ${env:ProgramFiles(x86)}, $env:ProgramData, $env:USERPROFILE) | Where-Object { $_ }
  } else {
    $Roots = Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object { $_.DeviceID + "\" }
  }
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

$rows = @()
foreach ($exe in ($found | Sort-Object)) {
  $lines = Invoke-Capture $exe "-XshowSettings:properties -version"
  $info = Read-JavaProps $lines
  $binDir = Split-Path $exe
  $pids = ($procs | Where-Object { (Split-Path $_.ExecutablePath) -eq $binDir } | ForEach-Object { $_.ProcessId }) -join " "
  $rows += [pscustomobject]@{
    host = $hostName; os = $osName; where = "host"; java_path = $exe
    vendor = $info.Vendor; version = $info.Version; runtime_build = $info.Build; arch = $info.Arch; running_pids = $pids
  }
}

# 4) running Docker containers (Linux containers)
if (-not $NoContainers -and (Get-Command docker -CommandType Application)) {
  # no double quotes inside: Windows PowerShell does not pass them to native programs reliably
  $probe = "find / -xdev \( -path /proc -o -path /sys \) -prune -o \( -type f -o -type l \) -name java -path '*/bin/java' -print 2>/dev/null | while IFS= read -r j; do readlink -f `$j; done | sort -u | while IFS= read -r j; do echo @@ `$j; `$j -XshowSettings:properties -version 2>&1; done"
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
          $rows += [pscustomobject]@{
            host = $hostName; os = $osName; where = "container:$name ($image)"; java_path = $path
            vendor = $info.Vendor; version = $info.Version; runtime_build = $info.Build; arch = $info.Arch; running_pids = ""
          }
        }
        $path = $line.Substring(3); $buf = @()
      } else { $buf += $line }
    }
  }
}

$rows | Export-Csv -LiteralPath $Out -NoTypeInformation -Encoding UTF8
"Found $($rows.Count) Java runtime(s). Result file: $Out"
$rows | Format-Table where, vendor, runtime_build, arch, running_pids, java_path -AutoSize | Out-String -Width 220
