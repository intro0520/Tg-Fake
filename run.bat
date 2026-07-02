@echo off
chcp 65001 >nul 2>&1
echo ============================================
echo    🎫 Telegram FAKA System v1.0.0
echo ============================================
echo.

cd /d D:\telegram-faka-python

REM ==== 读取 .env 中的端口 ====
set WEB_PORT=8000
for /f "tokens=1,2 delims==" %%A in (.env) do (
    if "%%A"=="WEB_PORT" set WEB_PORT=%%B
)

REM 检查端口占用
netstat -ano | findstr ":%WEB_PORT%" >nul && (
    echo [!] Port %WEB_PORT% is already in use
    netstat -ano | findstr ":%WEB_PORT%"
    echo.
    echo Change WEB_PORT in .env or stop the process using this port
    pause
    exit /b 1
)

echo [+] Using port: %WEB_PORT%

REM 检查虚拟环境
IF NOT EXIST venv (
    echo [+] Creating Python virtual environment...
    "C:\Users\intro\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m venv venv
)

REM 激活虚拟环境并安装依赖
echo [+] Checking dependencies...
call venv\Scripts\activate.bat >nul 2>&1
python -c "import fastapi, telegram, aiosqlite" 2>nul || (
    echo [+] Installing dependencies...
    python -m pip install -q python-dotenv python-telegram-bot aiosqlite uvicorn jinja2
)

REM 初始化数据库
echo [+] Initializing database...
python -c "import asyncio; from database import init_db; asyncio.run(init_db())"

REM 启动服务
echo.
echo ============================================================
echo    🎫 FAKA System Started
echo.
echo    📊 Dashboard: http://localhost:%WEB_PORT%
echo    🤖 Send /start to your Telegram Bot
echo ============================================================
echo.

"C:\Users\intro\.workbuddy\binaries\python\versions\3.13.12\python.exe" -m uvicorn web:app --host 0.0.0.0 --port %WEB_PORT% --log-level info
