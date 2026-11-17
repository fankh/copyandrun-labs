"""requirements.txt 의 패키지 이름이 실제로 존재하는지, 너무 새롭지 않은지 설치 전에 점검합니다.

사용법: python pkgcheck.py requirements.txt [--index URL] [--recent-days 30] [--min-releases 3] [--strict]
종료 코드: 0 통과, 1 존재하지 않는 이름이 있음(--strict 이면 경고도 1), 2 조회 실패(네트워크 등)
조회만 하며 어떤 패키지도 설치하지 않습니다.
"""
import argparse
import difflib
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


def read_names(path):
    names = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("-"):
            continue
        m = re.match(r"^([A-Za-z0-9][A-Za-z0-9._-]*)", line)
        if m:
            names.append(m.group(1))
    return names


def read_list(path):
    p = Path(path)
    if not p.exists():
        return set()
    return {normalize(x.split("#", 1)[0].strip()) for x in p.read_text(encoding="utf-8").splitlines() if x.split("#", 1)[0].strip()}


def fetch(index, name):
    """(상태코드, JSON 또는 None). 404 는 (404, None), 그 밖의 오류는 예외."""
    url = f"{index.rstrip('/')}/{normalize(name)}/json"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return 404, None
        raise


def first_release(data):
    times = []
    for files in data.get("releases", {}).values():
        for f in files:
            t = f.get("upload_time_iso_8601")
            if t:
                times.append(datetime.fromisoformat(t.replace("Z", "+00:00")))
    return min(times) if times else None


def similar_to(name, popular, cutoff=0.85):
    n = normalize(name)
    if n in popular:
        return None
    best = difflib.get_close_matches(n, sorted(popular), n=1, cutoff=cutoff)
    return best[0] if best else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("requirements")
    ap.add_argument("--index", default="https://pypi.org/pypi")
    ap.add_argument("--recent-days", type=int, default=30)
    ap.add_argument("--min-releases", type=int, default=3)
    ap.add_argument("--popular", default=str(HERE / "popular.txt"))
    ap.add_argument("--allow", default=str(HERE / "allowlist.txt"))
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()

    popular, allow = read_list(a.popular), read_list(a.allow)
    now = datetime.now(timezone.utc)
    missing = warned = 0
    print(f"{'이름':<30}{'판정':<8}{'최초 릴리스':<13}{'릴리스':>4}  비고")
    for name in read_names(a.requirements):
        n = normalize(name)
        try:
            code, data = fetch(a.index, name)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"{name:<30}{'조회실패':<8}{'-':<13}{'-':>4}  {e}")
            return 2
        notes = []
        if code == 404:
            missing += 1
            verdict, first, count = "없음", "-", "-"
            notes.append("인덱스에 없는 이름")
            if (s := similar_to(n, popular)):
                notes.append(f"{s} 와 비슷")
        else:
            first_dt = first_release(data)
            count = len(data.get("releases", {}))
            first = first_dt.strftime("%Y-%m-%d") if first_dt else "-"
            if n in allow:
                verdict = "허용"
                notes.append("allowlist")
            else:
                if first_dt and (now - first_dt).days < a.recent_days:
                    notes.append(f"최초 릴리스 {(now - first_dt).days}일 전")
                if count < a.min_releases:
                    notes.append(f"릴리스 {count}개")
                if (s := similar_to(n, popular)):
                    notes.append(f"{s} 와 비슷")
                verdict = "경고" if notes else "통과"
                warned += bool(notes)
        print(f"{name:<30}{verdict:<8}{first:<13}{count!s:>4}  {', '.join(notes)}")
    print(f"\n없음 {missing}건, 경고 {warned}건")
    return 1 if missing or (a.strict and warned) else 0


if __name__ == "__main__":
    sys.exit(main())
