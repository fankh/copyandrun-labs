"""이벤트를 STIX 2.1 로 내보내 파일로 저장합니다. PyMISP 를 씁니다.

사용법: MISP_URL=... MISP_KEY=... python export_stix.py <이벤트 번호> out.json
"""
import json
import os
import sys

from pymisp import PyMISP

misp = PyMISP(os.environ["MISP_URL"], os.environ["MISP_KEY"], ssl=False)
bundle = misp.search(controller="events", eventid=sys.argv[1], return_format="stix2")
with open(sys.argv[2], "w", encoding="utf-8") as f:
    json.dump(bundle, f, ensure_ascii=False, indent=2)
print("저장:", sys.argv[2], "객체", len(bundle.get("objects", [])), "개")
