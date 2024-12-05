from fastapi import FastAPI, Request
from search import Engine
import os
import requests

app = FastAPI()

engine = Engine()

@app.get("/search")
async def main(request: Request):
    query = request.query_params.get("q", "")
    if len(query) < 2:
        return []
    results = await engine.search_async(query)
    return list(set(results))

@app.get("/health")
async def read_root():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)