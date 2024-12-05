import gzip
open("out/db.yml.gz","wb").write(gzip.compress(open("out/db.yml","rb").read()))
open("out/index.yml.gz","wb").write(gzip.compress(open("out/index.yml","rb").read()))