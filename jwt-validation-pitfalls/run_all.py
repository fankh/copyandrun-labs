"""토큰을 검증기에 넣어 수락/거절을 보인다.
검증기 하나를 주면 상세 결과와 게이트(공격 토큰 수락이 있으면 종료 코드 1), 둘 이상을 주면 표로 비교한다.
사용: python run_all.py 폴더 good   |   python run_all.py 폴더 nosig bad good"""
import importlib
import json
import sys

sys.stdout.reconfigure(encoding="utf-8")
folder, names = sys.argv[1], sys.argv[2:]
tokens = json.load(open(f"{folder}/tokens.json", encoding="utf-8"))
pub = open(f"{folder}/server_pub.pem", "rb").read()


def run(which):
    verify = importlib.import_module(f"verifier_{which}").verify
    out = {}
    for name, tok in tokens.items():
        try:
            claims = verify(tok, pub)
            out[name] = ("수락", f"sub={claims.get('sub')}, role={claims.get('role')}")
        except Exception as e:
            out[name] = ("거절", type(e).__name__)
    return out


results = {n: run(n) for n in names}
accepted = {n: sum(1 for k, (r, _) in res.items() if k != "정상 토큰" and r == "수락") for n, res in results.items()}
legit = {n: results[n]["정상 토큰"][0] == "수락" for n in names}

if len(names) == 1:
    n = names[0]
    print(f"== verifier_{n}")
    for k, (r, why) in results[n].items():
        print(f"  {k:<10} {r}  ({why})")
    print(f"  공격 토큰 수락 {accepted[n]}건, 정상 토큰 {'수락' if legit[n] else '거절'}")
    sys.exit(1 if accepted[n] or not legit[n] else 0)

print(f"{'토큰':<12}" + "".join(f"{n:>8}" for n in names))
for k in tokens:
    print(f"{k:<12}" + "".join(f"{results[n][k][0]:>8}" for n in names))
print(f"{'공격 수락':<10}" + "".join(f"{accepted[n]:>8}" for n in names))
