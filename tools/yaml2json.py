import yaml
import json
import gzip

raw = yaml.load(open("db.yml"), yaml.CFullLoader)

json.dump(raw, open("out/db.json", "w"), ensure_ascii=False)
open("out/db.json.gz","wb").write(gzip.compress(open("out/db.json","rb").read()))


raw = yaml.load(open("index.yml"), yaml.CFullLoader)

json.dump(raw, open("out/index.json", "w"), ensure_ascii=False)
open("out/index.json.gz","wb").write(gzip.compress(open("out/index.json","rb").read()))

