# 읽는 연습에 쓰는 시험 샘플 세 개를 만듭니다. 원문은 호스트 이름을 출력하는 한 줄뿐입니다.
import base64, gzip, pathlib

PLAIN = "Write-Output ('host=' + (hostname))"
out = pathlib.Path("samples")
out.mkdir(exist_ok=True)
(out / "plain.txt").write_text(PLAIN + "\n", encoding="utf-8")  # 비교용 원문

# 샘플 1: -EncodedCommand 에 넣는 UTF-16LE base64
b64 = base64.b64encode(PLAIN.encode("utf-16-le")).decode()
(out / "sample1.txt").write_text(f"powershell -NoProfile -EncodedCommand {b64}\n", encoding="utf-8")

# 샘플 2: 문자열 조각 연결과 [char] 코드
def codes(s):
    return ",".join(str(ord(c)) for c in s)

line2 = (
    "& ('Write-'+'Out'+'put') (-join ([char[]]("
    + codes("host=")
    + ")) + (& ('host'+'name')))"
)
(out / "sample2.txt").write_text(line2 + "\n", encoding="utf-8")

# 샘플 3: 두 겹. 평문 -> UTF-16LE base64 -> gzip -> base64
inner = base64.b64encode(PLAIN.encode("utf-16-le"))
blob = base64.b64encode(gzip.compress(inner, mtime=0)).decode()
line3 = (
    f"$d=[Convert]::FromBase64String('{blob}');"
    "$s=New-Object IO.MemoryStream(,$d);"
    "$g=New-Object IO.Compression.GzipStream($s,[IO.Compression.CompressionMode]::Decompress);"
    "$t=(New-Object IO.StreamReader($g)).ReadToEnd();"
    "iex ([Text.Encoding]::Unicode.GetString([Convert]::FromBase64String($t)))"
)
(out / "sample3.txt").write_text(line3 + "\n", encoding="utf-8")
print("samples/ 에 plain.txt 와 sample1~3.txt 를 만들었습니다.")
