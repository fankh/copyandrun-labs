"""report.docx 는 압축 파일이다. 안의 word/document.xml 을 열어 표, 문단, 굵은 글씨, 글자를 확인한다."""
import re
import zipfile

z = zipfile.ZipFile("report.docx")
x = z.read("word/document.xml").decode("utf8")
text = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()

print("압축 안 파일 수:", len(z.namelist()))
print("표:", x.count("<w:tbl>"), "| 문단:", x.count("<w:p>") + x.count("<w:p "))
print("굵은 글씨 서식:", "있음" if "<w:b" in x else "없음")
print("추출한 글:", text[:80])
html = open("report.html", encoding="utf8").read()
print("HTML 안의 표:", html.count("<table"))
