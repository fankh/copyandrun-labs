import json
d = json.load(open('sbom.json'))
print(d['bomFormat'], d['specVersion'], len(d['components']))
for c in d['components']:
    print(c['name'], c['version'], c['purl'].split('/')[0])
