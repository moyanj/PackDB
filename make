#!/usr/bin/env python
import os
import shutil
import sys
import subprocess
import zipfile


def zip_directory(directory_path, output_zip_path):
    with zipfile.ZipFile(
        output_zip_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9
    ) as zipf:
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if file == "all.zip":
                    continue
                # 创建文件的完整路径
                file_path = os.path.join(root, file)
                # 将文件添加到zip文件中
                # arcname是zip文件中文件的存储路径，这里我们使用相对路径
                zipf.write(
                    file_path,
                    os.path.relpath(file_path, os.path.join(directory_path, os.pardir)),
                )


# 删除out目录及其内容（如果存在）
if os.path.exists("out"):
    shutil.rmtree("out")
os.mkdir("out")

subprocess.run([sys.executable, "search.py"], check=True)
# 复制数据库配置文件到out目录
shutil.copy("db.yml", "out/db.yml")
shutil.copy("index.yml", "out/index.yml")

# 调用外部Python脚本处理db.yaml文件
external_scripts = [
    "tools/yaml2gz.py",
    "tools/yaml2json.py",
    "tools/yaml2msgpack.py",
    "tools/yaml2pkl.py",
    "tools/yaml2xml.py",
]

for script in external_scripts:
    print(" ".join([sys.executable, script]))
    subprocess.run([sys.executable, script], check=True)

zip_directory("./out", "out/all.zip")

shutil.copy("out/index.json", "html/src/assets/index.json")
shutil.copy("out/db.json", "html/src/assets/db.json")