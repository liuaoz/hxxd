# 使用官方 Python 镜像作为基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 复制项目依赖文件
COPY requirements.txt .

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码到容器中
COPY ./app/ /app/

# 暴露端口（FastAPI 默认使用 8000 端口）
EXPOSE 8080

# 启动 FastAPI 应用
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]