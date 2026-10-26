"""대응 표(asi_mapping.json)가 일관된지, 연결한 글이 실제로 있는지 검사한다.

사용법:
  python check_asi_mapping.py --posts <글 폴더>     로컬에 글 파일(<slug>.md)이 있을 때
  python check_asi_mapping.py --site https://copyandrun.com   공개된 글 주소로 확인할 때
추가로 --md <글.md> 를 주면 그 글 본문의 /blog/<slug>/ 내부 링크도 같은 방식으로 검사한다.
"""
import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

BASE = Path(__file__).resolve().parent
IDS = [f"ASI{n:02d}" for n in range(1, 11)]


def exists_local(posts, slug):
    return (Path(posts) / f"{slug}.md").is_file()


def exists_site(site, slug):
    req = urllib.request.Request(f"{site.rstrip('/')}/blog/{slug}/", method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status == 200
    except Exception:
        return False


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--posts")
    ap.add_argument("--site")
    ap.add_argument("--md")
    ap.add_argument("--data", default=str(BASE / "asi_mapping.json"))
    a = ap.parse_args()
    if not a.posts and not a.site:
        sys.exit("--posts 또는 --site 가 필요합니다")
    exists = (lambda s: exists_local(a.posts, s)) if a.posts else (lambda s: exists_site(a.site, s))

    data = json.loads(Path(a.data).read_text(encoding="utf-8"))
    problems = []
    ids = [i["id"] for i in data["items"]]
    if ids != IDS:
        problems.append(f"항목 id 가 ASI01 부터 ASI10 까지 순서대로 있어야 합니다: {ids}")

    slugs = set()
    for item in data["items"]:
        st = item["status"]
        if st not in data["status_labels"]:
            problems.append(f"{item['id']}: 알 수 없는 상태 {st}")
        if st in ("tested", "partial") and not item["posts"]:
            problems.append(f"{item['id']}: 시험했다고 표시했지만 연결한 글이 없습니다")
        if st == "untested" and item["posts"]:
            problems.append(f"{item['id']}: 미시험인데 글이 연결되어 있습니다")
        if st != "tested" and not item["checklist"]:
            problems.append(f"{item['id']}: 완전히 시험하지 않은 항목에는 체크리스트가 필요합니다")
        for p in item["posts"]:
            slugs.add(p["slug"])
            if not p.get("fact"):
                problems.append(f"{item['id']}/{p['slug']}: 관찰 내용이 비어 있습니다")

    if a.md:
        body = Path(a.md).read_text(encoding="utf-8")
        slugs |= set(re.findall(r"\]\(/blog/([a-z0-9-]+)/?\)", body))

    for s in sorted(slugs):
        if not exists(s):
            problems.append(f"링크 대상 글이 없습니다: {s}")

    if problems:
        print("\n".join(problems))
        sys.exit(1)
    print(f"대응 표 일치: 항목 {len(IDS)}개, 확인한 글 {len(slugs)}편 모두 존재")


if __name__ == "__main__":
    main()
