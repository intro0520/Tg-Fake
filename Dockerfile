FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 数据卷
VOLUME ["/app/data"]

# 默认端口
EXPOSE 8001

ENTRYPOINT ["sh", "-c", "python -m uvicorn web:app --host ${WEB_HOST:-0.0.0.0} --port ${WEB_PORT:-8001}"]
