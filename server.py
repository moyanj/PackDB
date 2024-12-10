from fastapi import FastAPI, Request, Response
from search import Engine
from db import DB

app = FastAPI()

engine = Engine()
db = DB("db")


@app.get("/search")
async def main(request: Request):
    query = request.query_params.get("q", "")
    if len(query) < 2:
        return []
    results = await engine.search_async(query)
    return list(set(results))


@app.get("/{name}")
async def get_info(name: str, response: Response):
    if name in db:
        return await db.get(name)
    else:
        response.status_code = 404
        return {"msg":"无该库"}


@app.get("/health")
async def read_root():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
