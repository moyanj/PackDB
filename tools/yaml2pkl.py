import yaml
import pickle
import gzip

raw = yaml.load(open("db.yml"), yaml.CFullLoader)

pickle.dump(raw, open("out/db.pkl", "wb"))
open("out/db.pkl.gz","wb").write(gzip.compress(open("out/db.pkl","rb").read()))