from whoosh.fields import TEXT, SchemaClass, KEYWORD
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser
from whoosh.analysis import StemmingAnalyzer
from whoosh.sorting import ScoreFacet
from tqdm import tqdm
from bs4 import BeautifulSoup
import os
import asyncio
import hashlib
import shutil
import baidu_translate as fanyi
import asyncio
from db import DB

try:
    from jieba_fast.analyse import ChineseAnalyzer
    import jieba_fast as jieba
except:
    from jieba.analyse import ChineseAnalyzer
    import jieba

#jieba.load_userdict("out.txt")

zh_analyzer = ChineseAnalyzer()
en_analyzer = StemmingAnalyzer()


class PackageSchema(SchemaClass):
    name = TEXT(stored=True, analyzer=en_analyzer)
    desc = TEXT(analyzer=zh_analyzer)
    pypi_desc = TEXT(analyzer=en_analyzer)
    pypi_desc_zh = TEXT(analyzer=zh_analyzer)
    doc = TEXT(analyzer=en_analyzer)
    doc_zh = TEXT(analyzer=zh_analyzer)
    hash = KEYWORD()
    keywords = KEYWORD()


class Indexing:
    def __init__(self):
        # 创建索引
        if os.path.exists(".index"):
            shutil.rmtree(".index")
        os.mkdir(".index")
        os.makedirs(".cache", exist_ok=True)
        self.index = create_in(".index", schema=PackageSchema)
        self.writer = self.index.writer()
        self.db = DB("db")

    async def make(self):
        n = 0
        pbar = tqdm(total=len(self.db))
        async for name, data in self.db.items():
            pbar.set_description(f"{name[:11]:11}")
            pbar.update()

            docs = self.getText(data["doc_html"])

            self.writer.add_document(
                name=name,
                desc=data["desc"],
                pypi_desc=data["pypi_desc"],
                pypi_desc_zh=await self.tran(data["pypi_desc"]),
                doc=docs,
                doc_zh=await self.tran(docs),
                hash=self.getHash(data["releases"]),
            )
            n += 1
        pbar.close()
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

    def getHash(self, rels):
        ret = []
        for i in rels:
            for f in i["files"]:
                for h in f["digests"].values():
                    ret.append(h)

        return " ".join(ret)

    async def tran(self, src: str):
        if not src:
            return "无"
        sha = hashlib.md5(src.encode()).hexdigest()
        path = os.path.join(".cache", f"{sha}-tran.txt")
        if os.path.exists(path):
            return open(path).read()
        else:
            ret = await fanyi.translate_text_async(src, to=fanyi.Lang.ZH, from_=fanyi.Lang.EN)
            open(path, "w").write(ret)
            return ret


class Engine:
    def __init__(self):
        self.index = open_dir(".index", readonly=True, schema=PackageSchema)
        self.searcher = self.index.searcher()
        self.query = MultifieldParser(
            ["name", "desc", "pypi_desc", "pypi_desc_zh", "doc_zh", "doc", "keyword"],
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
    asyncio.run(i.make())
