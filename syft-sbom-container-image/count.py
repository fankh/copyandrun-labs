import json
from collections import Counter
d = json.load(open("sbom.json"))
print(d["bomFormat"], d["specVersion"], len(d["components"]))
print(Counter(c["type"] for c in d["components"]))
