    # 第一阶段: 构建 Python 应用
FROM python:3.13 AS builder

# 设置工作目录
WORKDIR /app

# 将当前目录内容复制到容器的工作目录中
COPY . /app

# 安装任何必需的包指定在 requirements.txt 中
RUN pip install --no-cache-dir -r requirements.txt

# 使用 PyInstaller 编译成独立的可执行文件
RUN pyinstaller --onefile --additional-hooks-dir=./hooks FastApiDemo.py

# 第二阶段: 只包含运行时和可执行文件
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 从构建阶段复制编译后的可执行文件
COPY --from=builder /app/dist/FastApiDemo /app/FastApiDemo

# 使端口 80 可供容器外使用
EXPOSE 8000

# 运行应用
CMD ["/app/FastApiDemo"]