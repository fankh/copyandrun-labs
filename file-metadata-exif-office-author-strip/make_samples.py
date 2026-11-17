"""연습용 시험 파일 두 개를 만듭니다. 사진도 이름도 모두 가짜입니다.

사용법: python make_samples.py
- IMG_20261031_142530.jpg : 단색 그라데이션 + 가짜 촬영 기기, 시각, GPS 좌표, 기기 일련번호, 소유자 이름, 썸네일
- report.docx            : 작성자 "Test Author", 마지막 수정자 "Test Reviewer", 회사 "Example Corp",
                           본문 속 이름, 변경 추적(삭제와 삽입) 한 건씩
"""
import io
import re
import zipfile
from datetime import datetime

import piexif
from docx import Document
from docx.oxml import parse_xml
from PIL import Image

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def gradient(size, rgb):
    base = Image.linear_gradient("L").resize(size)
    r, g, b = rgb
    return Image.merge("RGB", (base.point(lambda v: v * r // 255),
                               base.point(lambda v: v * g // 255),
                               base.point(lambda v: v * b // 255)))


def make_jpeg(path):
    photo = gradient((640, 480), (40, 120, 255))
    thumb_buf = io.BytesIO()
    gradient((160, 120), (255, 80, 40)).save(thumb_buf, "JPEG")  # 썸네일은 일부러 다른 색
    exif = {
        "0th": {piexif.ImageIFD.Make: b"TestCam", piexif.ImageIFD.Model: b"TC-100",
                piexif.ImageIFD.Software: b"TestCam FW 1.2",
                piexif.ImageIFD.DateTime: b"2026:10:31 14:25:30"},
        "Exif": {piexif.ExifIFD.DateTimeOriginal: b"2026:10:31 14:25:30",
                 piexif.ExifIFD.BodySerialNumber: b"SN-TEST-0001",
                 piexif.ExifIFD.CameraOwnerName: b"Test Owner"},
        "GPS": {piexif.GPSIFD.GPSLatitudeRef: b"N",
                piexif.GPSIFD.GPSLatitude: ((33, 1), (30, 1), (1230, 100)),
                piexif.GPSIFD.GPSLongitudeRef: b"E",
                piexif.GPSIFD.GPSLongitude: ((125, 1), (42, 1), (1860, 100))},
        "1st": {piexif.ImageIFD.Compression: 6},
        "thumbnail": thumb_buf.getvalue(),
    }
    photo.save(path, "JPEG", exif=piexif.dump(exif))


def make_docx(path):
    doc = Document()
    cp = doc.core_properties
    cp.author = "Test Author"
    cp.last_modified_by = "Test Reviewer"
    cp.comments = "Test Author 의 초안"
    cp.keywords = "draft"
    cp.revision = 7
    cp.created = datetime(2026, 10, 1, 9, 0, 0)
    cp.modified = datetime(2026, 10, 30, 17, 30, 0)
    doc.add_heading("분기 보고서 초안", 1)
    doc.add_paragraph("작성: Test Author, 검토: Test Reviewer")
    p = doc.add_paragraph("예산: ")
    p._p.append(parse_xml(
        f'<w:del xmlns:w="{W}" w:id="1" w:author="Test Reviewer" w:date="2026-10-30T17:00:00Z">'
        f'<w:r><w:delText>5000만원</w:delText></w:r></w:del>'))
    p._p.append(parse_xml(
        f'<w:ins xmlns:w="{W}" w:id="2" w:author="Test Reviewer" w:date="2026-10-30T17:00:00Z">'
        f'<w:r><w:t>4000만원</w:t></w:r></w:ins>'))
    buf = io.BytesIO()
    doc.save(buf)
    # 회사 이름은 docProps/app.xml 에 있으므로 압축 파일을 다시 써서 넣습니다.
    with zipfile.ZipFile(io.BytesIO(buf.getvalue())) as zin, zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/app.xml":
                text = data.decode("utf-8")
                text = re.sub(r"<Company>.*?</Company>|<Company/>", "", text)
                text = text.replace("</Properties>", "<Company>Example Corp</Company></Properties>")
                data = text.encode("utf-8")
            zout.writestr(item, data)


if __name__ == "__main__":
    make_jpeg("IMG_20261031_142530.jpg")
    make_docx("report.docx")
    print("만들었습니다: IMG_20261031_142530.jpg, report.docx")
