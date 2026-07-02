@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo    🎫 Telegram 发卡系统 v1.0.0        
echo ============================================
echo.

REM 检查端口占用
netstat -ano | findstr ":8001" >nul && (
    echo [!] 端口 8001 已被占用
    netstat -ano | findstr ":8001"
    echo.
    echo 请修改 .env 中的 WEB_PORT 或关闭占用该端口的程序
    exit /b 1
)

cd /d D:\telegram-faka-python

REM 检查虚拟环境
IF NOT EXIST venv (
    echo [+] 正在创建 Python 虚拟环境...
    "C:\Users\intro\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m venv venv
)

REM 激活虚拟环境并安装依赖
echo [+] 正在检查依赖...
call venv\Scripts\activate.bat >nul 2>&1
python -c "import fastapi, telegram, aiosqlite" 2>nul || (
    echo [+] 正在安装依赖...
    python -m pip install -q python-dotenv python-telegram-bot aiosqlite uvicorn jinja2
)

REM 初始化数据库
echo [+] 正在初始化数据库...
python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

REM 启动服务
echo [+] 启动服务...
echo.
echo =================================================================
echo      🎫 发卡系统已启动
echo.
echo      📊 管理后台: http://localhost:8001        
echo      📝 日志文件: D:\telegram-faka-python\server.log
echo.
echo      按 Ctrl+C 停止服务
echo =================================================================

"C:\Users\intro\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m uvicorn web:app --host 0.0.0.0 --port 8001 --log-level info
