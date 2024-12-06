# 阶段 1: 构建阶段
FROM python:3.12-alpine

WORKDIR /app

# 复制 requirements.txt 和 make 脚本
COPY . /app/

# 使 make 脚本可执行
RUN chmod +x /app/make
#RUN apt update && apt install gcc -y
# 安装依赖
RUN pip install --no-cache-dir -r requirements-runtime.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 构建索引
RUN if [ ! -d "/app/.index" ]; then echo "Index does not exist, stopping build"; exit 1; fi

# 删除不必要的文件和目录
RUN rm -rf /app/.cache

# 创建非 root 用户
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 健康检查
HEALTHCHECK --interval=10s --timeout=5s --retries=3 \
  CMD curl --fail http://localhost:8000/health || exit 1

# 更改为非 root 用户
USER appuser

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]