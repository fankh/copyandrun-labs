#!/usr/bin/env bash
# Pandoc 심화: 목차와 번호, 메타데이터, 단일 HTML 파일, 참조 문서로 글꼴 바꾸기, Lua 필터, 되돌려 변환.
# 준비: Docker, 파이썬. Pandoc 은 컨테이너(pandoc/core)로 실행한다. 같은 폴더에 report.md 가 있어야 한다.
# 실행(Git Bash): bash pandoc_more.sh   (약 1분)
set -u
export MSYS_NO_PATHCONV=1
export PYTHONWARNINGS=ignore
HERE="$(pwd -W 2>/dev/null || pwd)"
P="docker run --rm -v $HERE:/data pandoc/core:latest"
mkdir -p out

echo "## 1. 목차(--toc)와 장 번호(--number-sections)"
$P report.md -o out/plain.docx
$P report.md --toc --number-sections -o out/toc.docx
python -X utf8 - <<'PY'
import re, zipfile
def info(f):
    x = zipfile.ZipFile(f).read("word/document.xml").decode("utf-8")
    return len(x), x.count('TOC ' + chr(92) + 'o'), len(re.findall(r'<w:tbl>', x)), len(re.findall(r'w:pStyle w:val="Heading\d"', x))
for f in ("out/plain.docx", "out/toc.docx"):
    n, toc, tbl, head = info(f)
    print(f"  {f:<16} 문서 XML {n:>6}바이트, 목차 필드 {toc}개, 표 {tbl}개, 제목 {head}개")
PY

echo "## 2. 메타데이터(YAML 머리말)가 어디로 가나"
printf -- '---\ntitle: 월간 보고서\nauthor: 김민수\ndate: 2026-10-29\n---\n\n# 개요\n\n본문입니다.\n' > meta.md
$P meta.md -o out/meta.docx
python -X utf8 - <<'PY'
import re, zipfile
z = zipfile.ZipFile("out/meta.docx")
x = z.read("word/document.xml").decode("utf-8")
texts = re.findall(r'<w:t[^>]*>([^<]*)</w:t>', x)
styles = re.findall(r'w:pStyle w:val="([A-Za-z0-9]+)"', x)
print("  문서의 글:", texts[:5])
print("  문단 스타일:", styles[:5])
PY

echo "## 3. 단일 HTML 파일(--embed-resources --standalone)과 CSS"
printf 'body{font-family:sans-serif;color:#223}h1{color:#c33}\n' > style.css
$P report.md -s --embed-resources --css style.css -o out/report.html 2>&1 | tail -1
python -X utf8 - <<'PY'
x = open("out/report.html", encoding="utf-8").read()
print(f"  크기 {len(x.encode())}바이트, CSS 포함 {'color:#c33' in x}, 외부 링크 없음 {'href=\"style.css\"' not in x}")
PY

echo "## 4. 참조 문서(reference.docx)로 글꼴 바꾸기"
$P -o ref.docx --print-default-data-file reference.docx 2>/dev/null
python -X utf8 - <<'PY'
import re, zipfile
src = zipfile.ZipFile("ref.docx")
out = zipfile.ZipFile("out/my-ref.docx", "w", zipfile.ZIP_DEFLATED)
for item in src.infolist():
    data = src.read(item.filename)
    if item.filename == "word/theme/theme1.xml":      # 글꼴은 스타일이 아니라 테마에 들어 있다
        t = data.decode("utf-8")
        print("  기본 테마 글꼴:", sorted(set(re.findall(r'<a:latin typeface="([^"]+)"', t))))
        t = re.sub(r'(<a:latin typeface=")[^"]*(")', r'Malgun Gothic', t)
        t = t.replace('<a:ea typeface=""', '<a:ea typeface="Malgun Gothic"')
        data = t.encode("utf-8")
    out.writestr(item, data)
out.close()
PY
$P report.md --reference-doc out/my-ref.docx -o out/styled.docx
python -X utf8 - <<'PY'
import zipfile
for f in ("out/plain.docx", "out/styled.docx"):
    t = zipfile.ZipFile(f).read("word/theme/theme1.xml").decode("utf-8")
    print(f"  {f:<16} Malgun Gothic {t.count('Malgun Gothic')}곳, Aptos {t.count('Aptos')}곳")
PY

echo "## 5. Lua 필터: 본문의 TODO 를 [할 일] 로 바꾸기"
cat > todo.lua <<'LUA'
function Str(el)
  if el.text == "TODO" then return pandoc.Str("[할 일]") end
end
LUA
printf '# 목록\n\nTODO 항목을 정리한다. TODO 는 두 번 나온다.\n' > todo.md
$P todo.md --lua-filter todo.lua -t plain | sed 's/^/  /'

echo "## 6. 되돌려 변환: docx 를 다시 마크다운으로"
$P out/plain.docx -t gfm -o out/back.md
python -X utf8 - <<'PY'
import re
a = open("report.md", encoding="utf-8").read()
b = open("out/back.md", encoding="utf-8").read()
ha = re.findall(r'^#+ .*', a, re.M); hb = re.findall(r'^#+ .*', b, re.M)
print(f"  원본 제목 {len(ha)}개, 되돌린 제목 {len(hb)}개, 같은 제목 {len(set(h.lstrip('# ').strip() for h in ha) & set(h.lstrip('# ').strip() for h in hb))}개")
print(f"  원본 {len(a)}글자, 되돌린 {len(b)}글자 (표와 코드가 어떻게 바뀌는지는 두 파일을 비교해 본다)")
PY
rm -rf out meta.md style.css ref.docx todo.lua todo.md
