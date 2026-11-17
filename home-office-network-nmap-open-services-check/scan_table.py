"""nmap XML 결과로 기기별 열린 포트 표를 만듭니다.

사용법: python scan_table.py scan-before.xml            (한 번의 결과 표)
        python scan_table.py scan-before.xml scan-after.xml   (조치 전후 비교)
"""
import sys
import unicodedata
import xml.etree.ElementTree as ET

# 주소 -> 기기 이름 (연습 환경에서 정한 값)
NAMES = {
    "192.168.88.10": "프린터",
    "192.168.88.20": "NAS",
    "192.168.88.30": "공유기",
    "192.168.88.40": "일반 PC",
}
# 포트 -> (우선순위, 점검할 것). 열려 있다는 사실만으로 취약하다고 판단하지 않습니다.
RISK = {
    23: ("1 높음", "암호화 없는 원격 접속. 쓰지 않으면 끄기"),
    21: ("1 높음", "계정과 파일이 평문 전송. SMB나 SFTP로 대체"),
    80: ("2 확인", "관리 화면. 기본 계정 변경, 내부 접속 제한 확인"),
    445: ("2 확인", "파일 공유. 공유 대상과 계정 확인"),
    9100: ("3 낮음", "프린터 직접 출력. 쓰지 않으면 끄기"),
    631: ("3 낮음", "인쇄 서비스. 접근 범위 확인"),
}


def pad(text, width):
    """한글은 두 칸으로 세어 열을 맞춥니다."""
    used = sum(2 if unicodedata.east_asian_width(c) in "WF" else 1 for c in str(text))
    return str(text) + " " * max(1, width - used)


def load(path):
    """주소 -> [(포트, 서비스, 제품)] 과 응답한 주소 목록."""
    root = ET.parse(path).getroot()
    result, up = {}, []
    for host in root.findall("host"):
        addr = host.find("address").get("addr")
        up.append(addr)
        ports = []
        for p in host.findall("./ports/port"):
            if p.find("state").get("state") != "open":
                continue
            svc = p.find("service")
            name = svc.get("name", "?") if svc is not None else "?"
            prod = " ".join(x for x in (svc.get("product"), svc.get("version")) if x) if svc is not None else ""
            ports.append((int(p.get("portid")), name, prod))
        result[addr] = sorted(ports)
    return result, up


def table(path):
    data, up = load(path)
    print(pad("주소", 16) + pad("기기", 9) + pad("포트", 6) + pad("서비스", 13) + pad("우선순위", 9) + "점검할 것")
    for addr in up:
        label = NAMES.get(addr, "미확인")
        if not data[addr]:
            print(pad(addr, 16) + pad(label, 9) + pad("-", 6) + "(열린 포트 없음)")
        for port, name, prod in data[addr]:
            rank, note = RISK.get(port, ("2 확인", "용도 확인"))
            print(pad(addr, 16) + pad(label, 9) + pad(port, 6) + pad(name, 13) + pad(rank, 9) + note)
    total = sum(len(v) for v in data.values())
    print(f"\n응답한 기기 {len(up)}대, 열린 포트 {total}개")


def compare(before, after):
    b, _ = load(before)
    a, _ = load(after)
    print(pad("기기", 9) + pad("조치 전", 17) + pad("조치 후", 17) + "닫힌 포트")
    nb = na = 0
    for addr in sorted(b):
        pb = {p for p, _, _ in b[addr]}
        pa = {p for p, _, _ in a.get(addr, [])}
        nb, na = nb + len(pb), na + len(pa)
        fmt = lambda s: ",".join(map(str, sorted(s))) or "-"
        print(pad(NAMES.get(addr, addr), 9) + pad(fmt(pb), 17) + pad(fmt(pa), 17) + fmt(pb - pa))
    print(f"\n열린 포트 {nb}개 -> {na}개")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) == 2:
        table(sys.argv[1])
    elif len(sys.argv) == 3:
        compare(sys.argv[1], sys.argv[2])
    else:
        sys.exit(__doc__)
