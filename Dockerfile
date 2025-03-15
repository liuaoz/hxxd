# 使用官方 Python 3.10 slim 版镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .

RUN pip install -r requirements.txt

# 复制项目代码到容器
COPY ./app /app

# 设置环境变量，避免 Python 缓冲日志
ENV PYTHONUNBUFFERED=1

# 指定 FastAPI 运行端口
EXPOSE 8080

# 启动 FastAPI 应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
