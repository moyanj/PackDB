import msgpack
import json
import hashlib
import zipfile
import os
import aiofiles
import zlib
import time
import shutil
from typing import Any

import unittest
import tempfile
import asyncio


class DB:
    def __init__(self, uri: str) -> None:
        if uri.endswith(".zip"):
            self.base_dir = os.path.join(".", os.path.basename(uri).split(".")[0])
            shutil.rmtree(self.base_dir)
            with zipfile.ZipFile(uri) as f:
                f.extractall(self.base_dir)
        else:
            if os.path.isfile(uri):
                raise ValueError(f"{uri}是一个文件")
            elif not os.path.exists(uri):
                os.makedirs(uri)
            self.base_dir = uri
        self._keys = self.load_keys()
        self.will_write = {}

    def get_path(self, key: str) -> str:
        if not key:
            raise NameError("不正确的键名")

        file_suffix = hashlib.blake2s(key.encode()).hexdigest()[:2]
        # file_suffix = key[-1]
        return os.path.join(self.base_dir, f"{file_suffix}.d")

    def load_data(self, data: bytes) -> dict:
        try:
            decompressed = zlib.decompress(data)

            return msgpack.loads(decompressed)  # type: ignore
            # return json.loads(data)
        except:
            return {}

    def dump_data(self, data: dict):
        try:
            packed = msgpack.dumps(data)  # type: ignore
            return zlib.compress(packed, level=6)  # type: ignore
            # return json.dumps(data).encode()
        except:
            return b""

    async def save_keys(self):
        keys_path = os.path.join(self.base_dir, "keys")
        async with aiofiles.open(keys_path, "w") as f:
            await f.write(json.dumps(self._keys))  # type: ignore

    def load_keys(self) -> list:
        keys_path = os.path.join(self.base_dir, "keys")
        try:
            with open(keys_path, "rb") as f:
                return json.load(f)  # type: ignore
        except:
            return []

    async def add_key(self, key, act="a", no_sync=False):
        if act == "a":
            self._keys.append(key)
        else:
            self._keys.remove(key)
        self._keys = list(set(self._keys))
        if not no_sync:
            await self.save_keys()

    async def get(self, key: str) -> Any:
        if key not in self._keys:
            raise KeyError(key)
        async with aiofiles.open(self.get_path(key), "rb") as fp:
            d = await fp.read()
            return self.load_data(d)[key]

    async def set(self, key: str, data: Any, no_sync: bool = False):
        path = self.get_path(key)
        if os.path.exists(path):
            mode = "rb+"
        else:
            mode = "wb+"
        async with aiofiles.open(path, mode) as fp:
            fdata = await fp.read()
            fdata = self.load_data(fdata)
            fdata[key] = data
            await fp.seek(0)
            await fp.truncate(0)
            await fp.write(self.dump_data(fdata))
        await self.add_key(key, no_sync=no_sync)

    async def delete(self, key: str) -> None:
        if key not in self._keys:
            raise KeyError(f"{key}不存在")
        path = self.get_path(key)
        async with aiofiles.open(path, "rb+") as fp:
            existing_data = await fp.read()
            fdata = self.load_data(existing_data) if existing_data else {}
            fdata.pop(key)
            await fp.seek(0)
            await fp.truncate(0)
            await fp.write(self.dump_data(fdata))
        await self.add_key(key, "d")

    async def clear(self) -> None:
        for file in os.listdir(self.base_dir):
            if file.endswith(".d"):
                os.remove(os.path.join(self.base_dir, file))

    def keys(self):
        return self._keys

    async def values(self):
        for i in self.keys():
            yield await self.get(i)

    async def items(self):
        for i in self.keys():
            yield (i, await self.get(i))

    def export(self, name):
        with zipfile.ZipFile(name + ".zip", "w", zipfile.ZIP_DEFLATED) as zipf:
            # 获取文件夹中的文件列表
            for file_name in os.listdir(self.base_dir):
                # 构建文件的完整路径
                file_path = os.path.join(self.base_dir, file_name)
                # 确保是文件而不是文件夹
                if os.path.isfile(file_path):
                    # 将文件添加到zip文件中
                    zipf.write(file_path, file_name)

    def __len__(self):
        return len(self._keys)
    
    def __contains__(self, k):
        return k in self._keys


class TestDB(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.temp_dir = "test"  # tempfile.mkdtemp()
        self.db = DB(self.temp_dir)

    async def asyncTearDown(self):
        import shutil

        # shutil.rmtree(self.temp_dir)

    def test_init(self):
        # 测试初始化DB时目录是否正确创建
        self.assertTrue(os.path.exists(self.temp_dir))

    async def test_get_set(self):
        # 测试set和get方法是否正确
        key = "test_key"
        data = {key: "test_data"}
        await self.db.set(key, data[key])
        result = await self.db.get(key)
        self.assertEqual(result, data[key])

    async def test_delete(self):
        # 测试delete方法是否正确
        key = "test_key1"
        await self.db.set(key, "test_data")
        await self.db.delete(key)
        with self.assertRaises(KeyError):
            await self.db.get(key)

    async def test_add_index(self):
        # 测试add_index方法是否正确添加索引
        key = "test_key2"
        await self.db.add_key(key)
        self.assertIn(key, self.db.keys())

    async def test_clear(self):
        # 测试clear方法是否正确清除所有文件
        key = "test_key3"
        await self.db.set(key, "test_data")
        await self.db.clear()
        self.assertEqual(len(os.listdir(self.temp_dir)), 1)  # 只剩下index文件

    async def test_load_dump_data(self):
        # 测试数据的加载和转储是否正确
        data = {"test_key4": "test_data"}
        dumped_data = self.db.dump_data(data)
        loaded_data = self.db.load_data(dumped_data)
        self.assertEqual(loaded_data, data)


async def _main():
    db = DB("test")
    await db.set("1", "12")
    d = await db.get("1")
    print(d)


async def _speed_test():
    db = DB("test")
    st = time.time()
    for i in range(1000):
        await db.set(str(i), i, True)
    print("写入平均耗时：", (time.time() - st) / 1000 * 1000, "ms")
    st = time.time()
    for i in range(1000):
        await db.get(str(i))
    print("读取平均耗时：", (time.time() - st) / 1000 * 1000, "ms")


def test():
    unittest.main()


def speed_test():
    asyncio.run(_speed_test())


def main():
    asyncio.run(_main())


if __name__ == "__main__":
    speed_test()
