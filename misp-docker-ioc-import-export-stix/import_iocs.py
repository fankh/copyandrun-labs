"""iocs.csv 를 읽어 MISP 이벤트 하나로 등록합니다. PyMISP 를 씁니다.

사용법: MISP_URL=http://127.0.0.1:18060 MISP_KEY=<API 키> python import_iocs.py iocs.csv
같은 제목의 이벤트가 이미 있으면 새로 만들지 않고 그 이벤트 번호만 출력합니다.
"""
import csv
import os
import sys

from pymisp import MISPEvent, PyMISP

INFO = "시험용 침해지표 묶음 (cr-c11)"
EVENT_TAGS = ["tlp:amber", "lab:exercise"]

misp = PyMISP(os.environ["MISP_URL"], os.environ["MISP_KEY"], ssl=False)

found = misp.search(controller="events", eventinfo=INFO, pythonify=True)
if found:
    print("이미 있음: 이벤트", found[0].id)
    sys.exit(0)

event = MISPEvent()
event.info = INFO
event.distribution = 0        # 0: 이 조직만 볼 수 있음
event.threat_level_id = 3     # 3: 낮음
event.analysis = 1            # 1: 진행 중

with open(sys.argv[1], encoding="utf-8", newline="") as f:
    for row in csv.DictReader(f):
        attr = event.add_attribute(
            row["type"], row["value"],
            category=row["category"],
            to_ids=row["to_ids"] == "1",
            comment=row["comment"],
        )
        attr.add_tag(row["tags"])

for tag in EVENT_TAGS:
    event.add_tag(tag)

created = misp.add_event(event, pythonify=True)
print("만든 이벤트:", created.id, "속성", len(created.attributes), "개")
