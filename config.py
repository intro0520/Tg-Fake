"""配置文件 - 发卡系统"""
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_TG_ID = int(os.getenv("ADMIN_TG_ID", "0"))
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "admin")

# 系统设置
ORDER_DURATION_MINUTES = int(os.getenv("ORDER_DURATION_MINUTES", "30"))
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "faka.db")

# Web 服务
WEB_HOST = os.getenv("WEB_HOST", "0.0.0.0")
WEB_PORT = int(os.getenv("WEB_PORT", "8001"))

# 多语言
DEFAULT_LOCALE = os.getenv("DEFAULT_LOCALE", "zh")

# EPay（易支付）- 可选
EPAY_PID = os.getenv("EPAY_PID", "")
EPAY_KEY = os.getenv("EPAY_KEY", "")
EPAY_URL = os.getenv("EPAY_URL", "")
EPAY_NOTIFY_URL = os.getenv("EPAY_NOTIFY_URL", "")

# 支付模式：simulate（模拟）/ epay（易支付）
PAYMENT_MODE = os.getenv("PAYMENT_MODE", "simulate")

# NOWPayments（加密货币）
NOWPAYMENTS_API_KEY = os.getenv("NOWPAYMENTS_API_KEY", "")
NOWPAYMENTS_SANDBOX = os.getenv("NOWPAYMENTS_SANDBOX", "true").lower() == "true"
NOWPAYMENTS_SUCCESS_URL = os.getenv("NOWPAYMENTS_SUCCESS_URL", "")
NOWPAYMENTS_CANCEL_URL = os.getenv("NOWPAYMENTS_CANCEL_URL", "")

# Stripe
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
