import yaml
import msgpack
import gzip

raw = yaml.load(open("db.yml"), yaml.CFullLoader)

msgpack.pack(raw, open("out/db.msgpack", "wb"))
open("out/db.msgpack.gz","wb").write(gzip.compress(open("out/db.msgpack","rb").read()))