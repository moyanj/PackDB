import yaml
from dicttoxml import dicttoxml
import gzip
from xml.dom.minidom import parseString

raw = yaml.load(open("db.yml"), yaml.CFullLoader)

xml = dicttoxml(raw, custom_root="Database", return_bytes=False)
xml = parseString(xml)
open("out/db.xml", "w").write(xml.toprettyxml())
open("out/db.xml.gz","wb").write(gzip.compress(open("out/db.xml","rb").read()))
