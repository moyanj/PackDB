import asyncio
import time
import pypandoc
import tqdm
import os
import hashlib
import warnings
import datetime
import httpx
import random
import re
from db import DB

# 忽略所有警告
warnings.filterwarnings("ignore")


class PackDB:
    def __init__(self, path):
        self.db = DB(path)
        os.makedirs(".cache", exist_ok=True)

    async def get_info(self, name: str, max_retries=3) -> dict:
        urls = [
            f"https://mirrors.tuna.tsinghua.edu.cn/pypi/web/json/{name}",
            f"https://mirrors.ustc.edu.cn/pypi/json/{name}",
            f"https://mirrors.pku.edu.cn/pypi/web/json/{name}",
            f"https://mirrors.bfsu.edu.cn/pypi/web/json/{name}",
            f"https://mirrors.cloud.tencent.com/pypi/json/{name}",
            f"https://mirrors.hust.edu.cn/pypi/web/json/{name}",
        ]
        async with httpx.AsyncClient() as client:
            for attempt in range(max_retries + 1):
                url = random.choice(urls)
                # print(url)
                try:
                    response = await client.get(
                        url, timeout=httpx.Timeout(10, connect=10, read=10)
                    )

                    if response.status_code == 200:
                        return response.json()
                    else:
                        print(url)
                        print(
                            f"请求失败，状态码：{response.status_code}，尝试重新请求..."
                        )
                except httpx.RequestError as e:
                    print(f"请求错误：{e}，尝试重新请求...")
                except Exception as e:
                    print(f"未知错误：{e}，尝试重新请求...")

                if attempt < max_retries:
                    pass
                else:
                    raise NameError(f"{name}不存在或请求失败超过最大重试次数")
        return {}

    def make_rel_data(self, content):
        for v in content[-20:]:
            yield {
                "digests": v.get("digests"),
                "size": v.get("size"),
                "upload_time": int(
                    datetime.datetime.fromisoformat(
                        v.get("upload_time_iso_8601", "1970-01-01T00:00:00.00000Z")
                    ).timestamp()
                ),
                "file_name": v.get("filename"),
            }

    def make_rel(self, content: dict):
        r = []
        for k, v in content.items():
            r.append({"name": k, "files": list(self.make_rel_data(v))})
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
            ret = re.sub(r">\s+<", "><", ret)
            ret = re.sub(r"\s{2,}", " ", ret)
            ret = re.sub(
                r'(href|src|class|id|alt)\s*=\s*(["\'])([^"\']*)\2', r'\1="\3"', ret
            )
            open(path, "w").write(ret)
            return ret

    async def add(self, name: str, desc: str, every_save: bool = True):
        name = name.strip()
        name = name.lower()
        rels = {}
        # print("获取数据中。。。")
        if "内置库" in desc:
            pack_info = {
                "license": "PSF",
                "package_url": "https://github.com/python/cpython/tree/main/Lib",
                "home_page": "https://www.python.org",
            }
        else:
            ret = await self.get_info(name)
            pack_info = ret["info"]
            rels = ret["releases"]
        # print("处理数据中。。。")
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

        await self.db.set(
            name,
            {
                "desc": desc,
                "url": pack_info.get("package_url"),
                "requires": requires,
                "author": pack_info.get("author"),
                "license": pack_info.get("license"),
                "author_email": pack_info.get("author_email"),
                "home_page": pack_info.get("home_page"),
                "requires_python": pack_info.get("requires_python"),
                "classifiers": pack_info.get("classifiers"),
                "pypi_desc": pack_info.get("summary"),
                "project_urls": pack_info.get("project_urls", {}),
                "add_time": int(time.time()),
                "doc_html": doc,
                "doc": pack_info.get("description"),
                "latest": pack_info.get("version"),
                "keywords": keywords,
                "releases": self.make_rel(rels),
            },
        )

    def get(self, name: str):
        return self.db.get(name)

    async def update_all(self):
        n = 0
        pbar = tqdm.tqdm(self.db.keys())
        for i in pbar:
            pbar.set_description(f"{i[:11]:11}")
            data = await self.db.get(i)
            await self.add(i, data["desc"], every_save=False)
            n += 1

    def __len__(self):
        return len(self.db)


async def main():
    db = PackDB("db")
    while True:
        name = input("请输入包名：")
        if name.lower() in db.db:
            data = await db.get(name.lower())
            print(name, data["desc"])
            r = input("该包已存在，是否覆盖（y/n）：")
            if r == "n":
                continue
        desc = input("请输入介绍：")
        try:
            await db.add(name, desc)
        except NameError:
            print(f"{name}不存在")


if __name__ == "__main__":
   
    db = PackDB("db")
    asyncio.run(db.update_all())
    """
    asyncio.run(main())
    """
    
