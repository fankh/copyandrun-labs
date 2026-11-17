"""파일에 남은 숨은 정보를 읽어 보여 줍니다. 파일은 바꾸지 않습니다.

사용법: python inspect_meta.py 파일... [--name 찾을이름]
- JPEG : 촬영 기기, 시각, 일련번호, 소유자, GPS(십진수), 썸네일 크기
- docx : core.xml 과 app.xml 의 사람 관련 항목, 변경 추적(건수와 작성자, 날짜), 주석 파일, 본문 속 이름
"""
import re
import sys
import zipfile

import piexif


def dms(v, ref):
    d, m, s = (a / b for a, b in v)
    deg = d + m / 60 + s / 3600
    return -deg if ref in (b"S", b"W") else deg


def show_jpeg(path):
    ex = piexif.load(path)
    get = lambda ifd, tag: ex[ifd].get(tag, b"").decode(errors="replace") or "(없음)"
    print("  촬영 기기   :", get("0th", piexif.ImageIFD.Make), get("0th", piexif.ImageIFD.Model))
    print("  촬영 시각   :", get("Exif", piexif.ExifIFD.DateTimeOriginal))
    print("  일련번호    :", get("Exif", piexif.ExifIFD.BodySerialNumber))
    print("  소유자      :", get("Exif", piexif.ExifIFD.CameraOwnerName))
    g = ex["GPS"]
    if piexif.GPSIFD.GPSLatitude in g:
        lat = dms(g[piexif.GPSIFD.GPSLatitude], g[piexif.GPSIFD.GPSLatitudeRef])
        lon = dms(g[piexif.GPSIFD.GPSLongitude], g[piexif.GPSIFD.GPSLongitudeRef])
        print(f"  GPS 좌표    : {lat:.5f}, {lon:.5f}")
    else:
        print("  GPS 좌표    : (없음)")
    print("  썸네일      :", f"{len(ex['thumbnail'])} 바이트" if ex["thumbnail"] else "(없음)")


def show_docx(path, names):
    with zipfile.ZipFile(path) as z:
        core = z.read("docProps/core.xml").decode("utf-8")
        app = z.read("docProps/app.xml").decode("utf-8") if "docProps/app.xml" in z.namelist() else ""
        body = z.read("word/document.xml").decode("utf-8")
        files = z.namelist()
    for tag in ("dc:creator", "cp:lastModifiedBy", "dc:description", "cp:keywords", "cp:revision", "dcterms:modified"):
        m = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", core)
        print(f"  core.xml {tag:<18}:", (m.group(1) if m else "") or "(비어 있음)")
    for tag in ("Company", "Manager"):
        m = re.search(rf"<{tag}>(.*?)</{tag}>", app)
        print(f"  app.xml  {tag:<18}:", (m.group(1) if m else "") or "(비어 있음)")
    print("  변경 추적   : 삭제", len(re.findall(r"<w:del ", body)), "건, 삽입", len(re.findall(r"<w:ins ", body)), "건")
    marks = sorted(set(re.findall(r'<w:(?:ins|del) [^>]*?w:author="([^"]*)"[^>]*?w:date="([^"]*)"', body)))
    print("  변경 추적 작성자:", ", ".join(f"{n} ({d})" for n, d in marks) or "(없음)")
    print("  주석 파일   :", "있음" if "word/comments.xml" in files else "없음")
    text = re.sub(r"<[^>]+>", "", body)
    for n in names:
        print(f"  본문 속 '{n}' :", text.count(n), "곳")


if __name__ == "__main__":
    args = sys.argv[1:]
    names = []
    if "--name" in args:
        i = args.index("--name")
        names = [args[i + 1]]
        del args[i:i + 2]
    for p in args:
        print(p)
        (show_jpeg(p) if p.lower().endswith((".jpg", ".jpeg")) else show_docx(p, names))
