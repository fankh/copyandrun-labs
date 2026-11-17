import csv
import sys

# mactime -d -y 로 만든 CSV 를 파일 단위로 묶어 읽기 쉽게 요약합니다.
# Type 열은 m(수정) a(접근) c(inode 변경) b(생성) 네 글자이며, 해당하지 않으면 점입니다.
LABEL = {"m": "수정", "a": "접근", "c": "inode 변경", "b": "생성"}

files = {}
with open(sys.argv[1], newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        name = row["File Name"]
        stamp = row["Date"].replace("T", " ").rstrip("Z")
        kinds = [LABEL[c] for c in row["Type"] if c in LABEL]
        entry = files.setdefault(name, {"inode": row["Meta"], "dir": row["Mode"].startswith("d/"), "events": []})
        entry["events"].append((stamp, kinds))

for name, entry in sorted(files.items()):
    deleted = name.endswith("(deleted)")
    print(f"{name}  (inode {entry['inode']})")
    for stamp, kinds in entry["events"]:
        print(f"  {stamp}  {', '.join(kinds)}")
    last = entry["events"][-1][0]
    if entry["dir"]:
        print("  => 디렉터리입니다. 수정은 안의 항목이 추가되거나 지워진 때를 뜻합니다.")
    elif deleted:
        print(f"  => 삭제된 파일입니다. 마지막 기록은 {last} 입니다. 삭제 시각은 istat 의 Deleted 로 확인합니다.")
    elif len(entry["events"]) > 1 and any("수정" in k for _, k in entry["events"][1:]):
        print("  => 생성 뒤에 내용이 수정된 기록이 있습니다.")
