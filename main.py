"""主入口"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

import uvicorn
import config

print(f"""
╔══════════════════════════════════════════════════╗
║     🎫 Telegram 发卡系统 v1.0.0                   ║
╠══════════════════════════════════════════════════╣
║  管理后台: http://localhost:{config.WEB_PORT}            ║
║  支付模式: {config.PAYMENT_MODE:20}                   ║
║  数据库:  {config.DATABASE_PATH}          ║
╚══════════════════════════════════════════════════╝
""")

uvicorn.run("web:app", host=config.WEB_HOST, port=config.WEB_PORT, reload=False,
            log_level="info", access_log=False)
