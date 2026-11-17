#!/usr/bin/env python3
# 사용: python dmarc_summary.py 보고서.xml
# DMARC 집계 보고서(rua)의 XML 을 읽어 발신 IP 별로 SPF, DKIM 결과를 요약한다. 읽기만 한다.
# DMARC 통과 = DKIM 과 SPF 중 하나 이상이 정렬(alignment)되어 통과한 경우.
import sys
import xml.etree.ElementTree as ET


def text(node, path, default=""):
    found = node.find(path)
    return found.text.strip() if found is not None and found.text else default


def main(path):
    root = ET.parse(path).getroot()
    domain = text(root, "policy_published/domain")
    policy = text(root, "policy_published/p")
    reporter = text(root, "report_metadata/org_name")
    print(f"도메인 {domain}  정책 p={policy}  보고자 {reporter}")
    print()
    print(f"{'SOURCE IP':<16}{'COUNT':>6}  {'DKIM':<6}{'SPF':<6}DMARC")
    total = 0
    failed = 0
    for rec in root.findall("record"):
        ip = text(rec, "row/source_ip")
        count = int(text(rec, "row/count", "0"))
        dkim = text(rec, "row/policy_evaluated/dkim")
        spf = text(rec, "row/policy_evaluated/spf")
        ok = dkim == "pass" or spf == "pass"
        total += count
        if not ok:
            failed += count
        print(f"{ip:<16}{count:>6}  {dkim:<6}{spf:<6}{'통과' if ok else '실패'}")
    print()
    rate = failed * 100 / total if total else 0
    print(f"전체 {total}건 중 DMARC 실패 {failed}건 ({rate:.1f}%)")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("사용: python dmarc_summary.py 보고서.xml")
        sys.exit(1)
    main(sys.argv[1])
