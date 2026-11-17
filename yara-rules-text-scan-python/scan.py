import yara, pathlib, time
rules = yara.compile(filepath="rules.yar")
t = time.time()
for p in sorted(pathlib.Path("samples").iterdir()):
    m = rules.match(str(p))
    print(p.name, "->", [x.rule for x in m] or "no match")
print("%.4fs" % (time.time() - t))

try:
    yara.compile(source='rule x { condition: $a }')
except Exception as e:
    print(type(e).__name__, e)

r = yara.compile(source='rule big { strings: $s = "A" condition: #s > 2 }')
print([m.rule for m in r.match(data=b"AAAB")], [m.rule for m in r.match(data=b"AB")])
