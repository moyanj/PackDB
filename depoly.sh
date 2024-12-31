#!/bin/bash

# 定义变量
GIT_REPO_PATH="/firefly/packdb" # 替换为你的Git仓库本地路径
IMAGE_NAME="packdb" # 你想要构建的Docker镜像名称的基础名称
CONTAINER_NAME="packdb" # 你想要部署的容器名称
PORTS="-p 12112:80" # 映射的端口，根据你的应用需求修改

# 获取当前日期作为镜像版本
DATE=$(date +%Y%m%d)

# 构建完整的镜像名称，包含版本号
FULL_IMAGE_NAME="${IMAGE_NAME}:${DATE}"

# 进入Git仓库目录
cd $GIT_REPO_PATH

# 拉取Git仓库的最新代码
echo "正在拉取最新代码..."
git pull
if [ $? -ne 0 ]; then
    echo "拉取最新代码失败，请检查网络或Git仓库状态"
    exit 1
else
    echo "拉取最新代码成功"
    # 如果git pull没有新变化，退出脚本
    if [ -z "$(git status --porcelain)" ]; then
        echo "最新代码没有变化，退出脚本"
        exit 0
    fi
fi
source .venv/bin/activate
python search.py
# 构建Docker镜像
echo "构建$(FULL_IMAGE_NAME)镜像..."
docker build -t $FULL_IMAGE_NAME .
if [ $? -ne 0 ]; then
    echo "构建Docker镜像失败"
    exit 1
fi

# 停止并删除旧的容器（如果存在）
echo "停止并删除旧的容器..."
docker stop $CONTAINER_NAME 2>/dev/null
docker rm $CONTAINER_NAME 2>/dev/null

# 部署Docker容器
echo "使用${FULL_IMAGE_NAME}部署服务中..."
docker run -d --name $CONTAINER_NAME $PORTS $FULL_IMAGE_NAME
if [ $? -ne 0 ]; then
    echo "docker容器启动失败"
    exit 1
fi

echo "部署成功!"