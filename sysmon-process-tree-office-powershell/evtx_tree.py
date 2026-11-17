import ntpath
import re
import sys
import xml.etree.ElementTree as ET

from Evtx.Evtx import Evtx

NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"

# 문서 앱 실행 파일 이름과, 문서 앱이 자식으로 두면 눈여겨볼 실행 파일 이름입니다.
OFFICE = {"winword.exe", "excel.exe", "powerpnt.exe", "outlook.exe", "msaccess.exe", "mspub.exe", "visio.exe", "onenote.exe"}
SHELLS = {"cmd.exe", "powershell.exe", "pwsh.exe", "wscript.exe", "cscript.exe", "mshta.exe", "rundll32.exe", "regsvr32.exe"}
# 정상 Office 설치 경로의 앞부분(소문자)
OFFICE_DIRS = (r"c:\program files\microsoft office", r"c:\program files (x86)\microsoft office")


def base(path):
    return ntpath.basename(path).lower()


def classify(parent_image, image):
    """부모와 자식 경로를 보고 표시할 꼬리표 목록을 돌려줍니다."""
    tags = []
    if base(parent_image) in OFFICE:
        if base(image) in SHELLS:
            tags.append("OFFICE>SHELL")
        if not ntpath.dirname(parent_image).lower().startswith(OFFICE_DIRS):
            tags.append("PATH?")
    return tags


def read_process_events(path):
    """EVTX 에서 Sysmon 이벤트 ID 1 만 골라 딕셔너리 목록으로 돌려줍니다."""
    events = []
    with Evtx(path) as log:
        for rec in log.records():
            root = ET.fromstring(rec.xml())
            if root.findtext(f"{NS}System/{NS}EventID") != "1":
                continue
            d = {e.get("Name"): (e.text or "") for e in root.iter(f"{NS}Data")}
            d["Time"] = root.find(f"{NS}System/{NS}TimeCreated").get("SystemTime")
            events.append(d)
    return events


def print_tree(events):
    by_guid = {e["ProcessGuid"]: e for e in events}
    children = {}
    roots = []
    for e in events:
        pg = e["ParentProcessGuid"]
        if pg in by_guid:
            children.setdefault(pg, []).append(e)
        else:
            roots.append(e)  # 부모 생성 이벤트가 이 로그에 없는 프로세스

    flagged = 0

    def show(e, depth):
        nonlocal flagged
        tags = classify(e["ParentImage"], e["Image"])
        flagged += bool(tags)
        mark = ("  <== " + " ".join(tags)) if tags else ""
        t = re.search(r"\d\d:\d\d:\d\d", e["Time"]).group(0)
        print(f"{'    ' * depth}{t} pid={e['ProcessId']} {ntpath.basename(e['Image'])}{mark}")
        print(f"{'    ' * depth}   cmd: {e['CommandLine']}")
        for c in children.get(e["ProcessGuid"], []):
            show(c, depth + 1)

    for r in roots:
        print(f"[부모 {ntpath.basename(r['ParentImage'])} pid={r['ParentProcessId']} 는 이 로그에 생성 이벤트 없음]")
        show(r, 1)
    print(f"프로세스 생성 {len(events)}건, 표시 {flagged}건")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    events = read_process_events(sys.argv[1])
    if "--fields" in sys.argv:
        # 마지막 프로세스 생성 이벤트 한 건의 주요 필드를 그대로 보여 줍니다.
        for key in ("UtcTime", "ProcessGuid", "ProcessId", "Image", "CommandLine", "User",
                    "ParentProcessGuid", "ParentProcessId", "ParentImage", "ParentCommandLine"):
            print(f"{key:18}: {events[-1].get(key, '')}")
    else:
        print_tree(events)
