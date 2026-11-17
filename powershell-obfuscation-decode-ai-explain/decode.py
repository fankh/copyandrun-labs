# 실행하지 않고 풉니다. 문자열 처리만 하고 PowerShell 을 부르지 않습니다.
import base64, gzip, pathlib, re

def show(title, text):
    print(f"[{title}]")
    print(text)
    print()

def sample1(src):
    b64 = re.search(r"-EncodedCommand\s+(\S+)", src).group(1)
    raw = base64.b64decode(b64)
    show("1단계 base64 해제 (바이트 앞부분)", raw[:16])
    show("2단계 UTF-16LE 디코드", raw.decode("utf-16-le"))

def sample2(src):
    # [char[]]( ... ) 안의 숫자를 글자로 바꾸고, 따옴표 조각은 이어 붙입니다.
    nums = re.search(r"\[char\[\]\]\(([\d,]+)\)", src).group(1)
    show("[char] 코드 -> 글자", "".join(chr(int(n)) for n in nums.split(",")))
    for m in re.finditer(r"\(((?:'[^']*'\+?)+)\)", src):
        frag = "".join(re.findall(r"'([^']*)'", m.group(1)))
        show("조각 연결", frag)

def sample3(src):
    blob = re.search(r"FromBase64String\('([^']+)'\)", src).group(1)
    gz = base64.b64decode(blob)
    show("1단계 base64 해제 (gzip 머리 바이트)", gz[:4].hex())
    inner = gzip.decompress(gz)
    show("2단계 gzip 해제", inner.decode("ascii"))
    raw = base64.b64decode(inner)
    show("3단계 base64 해제 후 UTF-16LE 디코드", raw.decode("utf-16-le"))

for name, fn in [("sample1", sample1), ("sample2", sample2), ("sample3", sample3)]:
    print("=" * 10, name, "=" * 10)
    fn(pathlib.Path("samples", name + ".txt").read_text(encoding="utf-8"))
