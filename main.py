import yaml
import requests
import time
import pypandoc
import tqdm
import os
import hashlib
import warnings

# 忽略所有警告
warnings.filterwarnings("ignore")

class PackDB:
    def __init__(self, path):
        self.path = path
        self.db = {}
        self.load()
        os.makedirs(".cache", exist_ok=True)

    def load(self):
        self.db = yaml.load(open(self.path), yaml.CFullLoader)
        if self.db is None:
            self.db = {}

    def save(self):
        yaml.dump(self.db, open(self.path, "w"), yaml.CDumper, allow_unicode=True)
        self.load()

    def get_info(self, name: str):
        response = requests.get(
            f"https://mirrors.tuna.tsinghua.edu.cn/pypi/web/json/{name}"
        )

        if response.status_code != 200:
            raise NameError(f"{name}不存在")

        return response.json()

    def make_rel(self, content: dict):
        r = []
        for v in content.keys():
            r.append(v)
        return r

    def toHTML(self, type, content):
        if not content:
            return ""
        sha = hashlib.md5(content.encode()).hexdigest()
        path = os.path.join(".cache", f"{sha}-cov.txt")
        if os.path.exists(path):
            return open(path).read()
        else:
            ret = pypandoc.convert_text(content, "html", format=type)
            open(path, "w").write(ret)
            return ret

    def add(self, name: str, desc: str, every_save: bool = True):
        name = name.strip()
        name = name.lower()
        rels = {}
        print("获取数据中。。。")
        if "内置库" in desc:
            pack_info = {
                "license": "PSF",
                "package_url": "https://github.com/python/cpython/tree/main/Lib",
                "home_page": "https://www.python.org",
            }
        else:
            ret = self.get_info(name)
            pack_info = ret["info"]
            rels = ret["releases"]
        print("处理数据中。。。")
        raw_requires: list[str] = pack_info.get("requires_dist", [])  # type: ignore
        requires: list[str] = []
        if raw_requires:
            for i in raw_requires:
                out: str = i
                if ";" in out:
                    out = out.split(";")[0]
                if "==" in out:
                    out = out.split("==")[0]
                if ">=" in out:
                    out = out.split(">=")[0]
                if "!=" in out:
                    out = out.split("!=")[0]
                if "<" in out:
                    out = out.split("<")[0]
                if ">" in out:
                    out = out.split(">")[0]
                if "~=" in out:
                    out = out.split("~=")[0]
                if " " in out:
                    out = out.split(" ")[0]

                requires.append(out.strip())
        requires = list(set(requires))

        desc = desc.strip()
        if desc[-1] == "。":
            desc = desc[:-1]

        keywords = []
        raw_keywords = pack_info.get("keywords", None)
        if raw_keywords:
            for i in raw_keywords.split(","):
                keywords.append(i.strip())

        doc_type = pack_info.get("description_content_type")
        if doc_type is None:
            doc_type = "rst"
        elif doc_type == "text/markdown":
            doc_type = "markdown"
        else:
            doc_type = "rst"

        doc = self.toHTML(doc_type, pack_info.get("description"))

        self.db[name] = {
            "desc": desc,
            "url": pack_info.get("package_url"),
            "requires": requires,
            "author": pack_info.get("author"),
            "author_email": pack_info.get("author_email"),
            "home_page": pack_info.get("home_page"),
            "requires_python": pack_info.get("requires_python"),
            "classifiers": pack_info.get("classifiers"),
            "pypi_desc": pack_info.get("summary"),
            "project_urls": pack_info.get("project_urls", {}),
            "add_time": int(time.time()),
            "doc_html": doc,
            "doc": pack_info.get("description"),
            "doc_type": pack_info.get("description_content_type"),
            "latest": pack_info.get("version"),
            "keywords": keywords,
            "releases": self.make_rel(rels),
        }

        if every_save:
            self.save()

    def get(self, name: str):
        return self.db[name]

    def update(self, name: str, obj: object):
        self.db[name] = obj
        self.save()

    def update_all(self):
        db = self.db.copy()
        n = 0
        for i in tqdm.tqdm(db.keys()):
            self.add(i, db[i]["desc"], every_save=False)
            n += 1
            if n % 25 == 0:
                self.save()
        self.save()

    def __len__(self):
        return len(self.db)


def main():
    db = PackDB("db.yml")
    while True:
        name = input("请输入包名：")
        if name.lower() in db.db:
            print(name, db.db[name.lower()]["desc"])
            r = input("该包已存在，是否覆盖（y/n）：")
            if r == "n":
                continue
        desc = input("请输入介绍：")
        try:
            db.add(name, desc)
        except NameError:
            print(f"{name}不存在")


if __name__ == "__main__":
    '''
    db = PackDB("db.yml")
    db.update_all()
    '''
    main()
