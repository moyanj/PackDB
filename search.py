from whoosh.fields import TEXT, SchemaClass
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StemmingAnalyzer
from whoosh.sorting import ScoreFacet
from jieba_fast.analyse import ChineseAnalyzer
from tqdm import tqdm
from bs4 import BeautifulSoup
import jieba_fast
import os
import json
import hashlib
import shutil
import baidu_translate as fanyi
import asyncio

jieba_fast.load_userdict("out.txt")

zh_analyzer = ChineseAnalyzer()
en_analyzer = StemmingAnalyzer()


class PackageSchema(SchemaClass):
    name = TEXT(stored=True, analyzer=en_analyzer)
    desc = TEXT(stored=True, analyzer=zh_analyzer)
    pypi_desc = TEXT(stored=True, analyzer=en_analyzer)
    pypi_desc_zh = TEXT(stored=True, analyzer=zh_analyzer)
    doc = TEXT(stored=True, analyzer=en_analyzer)
    doc_zh = TEXT(stored=True, analyzer=zh_analyzer)


class Indexing:
    def __init__(self):
        # 创建索引
        if os.path.exists(".index"):
            shutil.rmtree(".index")
        os.mkdir(".index")
        os.makedirs(".cache", exist_ok=True)
        self.index = create_in(".index", schema=PackageSchema)
        self.writer = self.index.writer()
        self.db = json.load(open("out/db.json"))

    def make(self):
        n = 0
        pbar = tqdm(self.db.items())
        for name, data in pbar:
            pbar.set_description(f"{name[:11]:11}")

            docs = self.getText(data["doc_html"])

            self.writer.add_document(
                name=name,
                desc=data["desc"],
                pypi_desc=data["pypi_desc"],
                pypi_desc_zh=self.tran(data["pypi_desc"]),
                doc=docs,
                doc_zh=self.tran(docs),
            )
            n += 1

        self.writer.commit()

    def getText(self, content):
        if not content:
            return "无"
        sha = hashlib.md5(content.encode()).hexdigest()
        path = os.path.join(".cache", f"{sha}-raw.txt")
        if os.path.exists(path):
            return open(path).read()
        else:
            soup = BeautifulSoup(content, "html.parser")
            ret = soup.getText().replace("\n", " ")
            open(path, "w").write(ret)
            return ret

    def tran(self, src: str):
        if not src:
            return "无"
        sha = hashlib.md5(src.encode()).hexdigest()
        path = os.path.join(".cache", f"{sha}-tran.txt")
        if os.path.exists(path):
            return open(path).read()
        else:
            ret = fanyi.translate_text(src, to=fanyi.Lang.ZH, from_=fanyi.Lang.EN)
            open(path, "w").write(ret)
            return ret


class Engine:
    def __init__(self):
        self.index = open_dir(".index", readonly=True, schema=PackageSchema)
        self.searcher = self.index.searcher()
        self.query = MultifieldParser(
            ["name", "desc", "pypi_desc", "pypi_desc_zh", "doc_zh", "doc"],
            self.index.schema,
        )
        self.score_facet = ScoreFacet()

    def search(self, s):
        query = self.query.parse(s)
        score_facet = ScoreFacet()
        for i in self.searcher.search(query, sortedby=score_facet, limit=None):
            yield i["name"]
    
    async def search_async(self, s):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, self.search, s)
        return result


if __name__ == "__main__":
    i = Indexing()
    i.make()
