"""공유하기 전에 숨은 정보를 지운 사본을 만듭니다. 원본은 그대로 둡니다.

사용법: python clean_meta.py 원본 사본
- JPEG : EXIF 구간 전체(기기, 시각, GPS, 썸네일 포함)를 떼어 냅니다. 그림 데이터는 다시 압축하지 않습니다.
- docx : core.xml 의 작성자, 마지막 수정자, 설명, 키워드와 app.xml 의 회사, 관리자를 비우고 revision 을 1 로 맞춥니다.
         본문의 이름, 변경 추적(작성자 이름과 날짜 포함), 주석은 내용이라서 지우지 않고 남아 있다고 알려 줍니다.
"""
import re
import sys
import zipfile

import piexif


def clean_jpeg(src, dst):
    piexif.remove(src, dst)


def blank(xml, tags):
    for t in tags:
        xml = re.sub(rf"<{t}>.*?</{t}>", f"<{t}></{t}>", xml)
    return xml


def clean_docx(src, dst):
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "docProps/core.xml":
                x = blank(data.decode("utf-8"), ["dc:creator", "cp:lastModifiedBy", "dc:description", "cp:keywords"])
                data = re.sub(r"<cp:revision>.*?</cp:revision>", "<cp:revision>1</cp:revision>", x).encode("utf-8")
            elif item.filename == "docProps/app.xml":
                data = blank(data.decode("utf-8"), ["Company", "Manager"]).encode("utf-8")
            zout.writestr(item, data)
    with zipfile.ZipFile(dst) as z:
        body = z.read("word/document.xml").decode("utf-8")
        has_comments = "word/comments.xml" in z.namelist()
    left = len(re.findall(r"<w:(?:ins|del) ", body))
    if left or has_comments:
        print(f"주의: 본문에 변경 추적 {left}건(작성자 이름과 날짜 포함), 주석 파일 {'있음' if has_comments else '없음'}. 직접 확인해야 합니다.")


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    (clean_jpeg if src.lower().endswith((".jpg", ".jpeg")) else clean_docx)(src, dst)
    print("만들었습니다:", dst)
