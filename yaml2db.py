import yaml
from db import DB
import asyncio

async def main():
    db = DB("db")
    r_db = yaml.load(open("db.yml"), yaml.CLoader)
    for k, v in r_db.items():
        await db.set(k, v)

async def t():
    db = DB("db")
    data = await db.get("rsa")
    print(data["desc"])