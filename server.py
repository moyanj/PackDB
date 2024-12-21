from fastapi import FastAPI, Response, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Annotated
from search import Engine
from db import DB

app = FastAPI()

engine = Engine()
db = DB("db")


class SearchQuery(BaseModel):
    q: str = Field(...)  # 查询参数


class BatchGetQuery(BaseModel):
    l: str = Field(...)  # 逗号分隔的查询参数列表


class PackageInfo(BaseModel):
    name: str
    info: dict


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 可以限制为特定的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
async def search(query: Annotated[SearchQuery, Query()]):
    """
    Search package
    """
    results = await engine.search_async(query.q)
    return list(set(results))


@app.get("/pack/{name}")
async def get_info(name: str, response: Response):
    if name in db:
        info = await db.get(name)
        return PackageInfo(name=name, info=info)
    else:
        response.status_code = 404
        return {"msg": "not found"}


@app.get("/packs")
async def get_keys():
    return db.keys()


@app.get("/batch")
async def get_batch(
    batch_get_query: Annotated[BatchGetQuery, Query()], response: Response
):
    need = set(batch_get_query.l.split(","))
    if len(need) > 15:
        response.status_code = 400
        return {"msg": "max is 15"}

    ret = {}

    for i in need:
        if not i:
            continue
        try:
            ret[i] = await db.get(i)
        except KeyError:
            return {"msg": f"{i} not found"}

    return ret


@app.get("/health")
async def read_root():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
