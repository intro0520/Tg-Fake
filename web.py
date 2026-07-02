"""Web 管理后台 - FastAPI"""
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from urllib.parse import parse_qs
import os
import asyncio

import config
import database as db
from i18n import t as translate, switch_locale

BASE_DIR = os.path.dirname(__file__)

# 使用 Jinja2 直接加载模板
env = Environment(
    loader=FileSystemLoader(os.path.join(BASE_DIR, "templates")),
    autoescape=False,
)

def timestamp_to_date(ts):
    """时间戳转日期"""
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")
    except:
        return str(ts)

def format_price(val):
    """格式化价格"""
    return f"{float(val):.2f}"

env.filters["timestamp_to_date"] = timestamp_to_date
env.filters["format_price"] = format_price

def render(template_name: str, context: dict) -> str:
    """渲染模板"""
    template = env.get_template(template_name)
    return template.render(**context)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()
    print("[Main] 数据库初始化完成")

    # 启动 Telegram Bot
    if not config.BOT_TOKEN:
        print("[Main] ⚠️ BOT_TOKEN 未配置，Telegram Bot 未启动")
    else:
        try:
            from bot import init_bot
            asyncio.create_task(init_bot())
            print("[Main] ✓ Telegram Bot 已启动")
        except Exception as e:
            print(f"[Main] ⚠️ Bot 启动失败: {e}")

    yield


app = FastAPI(title="发卡系统管理后台", version="1.0.0", lifespan=lifespan)

# 挂载静态文件
app.mount("/static",
          StaticFiles(directory=os.path.join(BASE_DIR, "static")),
          name="static")


def get_lang(request: Request) -> str:
    """从 query string 获取语言，默认中文"""
    query = parse_qs(request.url.query)
    lang = query.get("lang", [config.DEFAULT_LOCALE])[0]
    if lang not in ("zh", "en"):
        lang = config.DEFAULT_LOCALE
    return lang


# ==================== 页面路由 ====================

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """仪表盘"""
    lang = get_lang(request)
    stats = await db.get_stats()
    products = await db.get_all_products()
    orders = await db.get_all_orders(limit=20)
    html = render("index.html", {
        "request": request,
        "active_page": "dashboard",
        "lang": lang,
        "other_lang": switch_locale(),
        "t": lambda key: translate(key, lang),
        "bot_running": False,
        "stats": stats,
        "products": products,
        "orders": orders,
    })
    return HTMLResponse(html)


@app.get("/products", response_class=HTMLResponse)
async def products_page(request: Request):
    """商品管理"""
    lang = get_lang(request)
    products = await db.get_all_products()
    html = render("products.html", {
        "request": request,
        "active_page": "products",
        "lang": lang,
        "other_lang": switch_locale(),
        "t": lambda key: translate(key, lang),
        "bot_running": False,
        "products": products,
    })
    return HTMLResponse(html)


@app.get("/orders", response_class=HTMLResponse)
async def orders_page(request: Request):
    """订单管理"""
    lang = get_lang(request)
    orders = await db.get_all_orders(limit=200)
    html = render("orders.html", {
        "request": request,
        "active_page": "orders",
        "lang": lang,
        "other_lang": switch_locale(),
        "t": lambda key: translate(key, lang),
        "bot_running": False,
        "orders": orders,
    })
    return HTMLResponse(html)


# ==================== API ====================

@app.get("/api/products")
async def api_get_products():
    return await db.get_all_products()


@app.post("/api/products")
async def api_create_product(
    name: str = Form(...),
    description: str = Form(""),
    price: float = Form(...),
):
    if price <= 0:
        raise HTTPException(status_code=400, detail="价格必须大于0")
    product_id = await db.create_product(name, description, price)
    return {"success": True, "id": product_id}


@app.delete("/api/products/{product_id}")
async def api_delete_product(product_id: str):
    await db.delete_product(product_id)
    return {"success": True}


@app.post("/api/products/{product_id}/stock")
async def api_add_stock(
    product_id: str,
    contents: str = Form(...),
):
    lines = [l.strip() for l in contents.split("\n") if l.strip()]
    if not lines:
        raise HTTPException(status_code=400, detail="库存内容不能为空")
    await db.add_product_items(product_id, lines)
    return {"success": True, "count": len(lines)}


@app.delete("/api/products/{product_id}/stock")
async def api_clear_stock(product_id: str):
    await db.delete_all_stock(product_id)
    return {"success": True}


@app.get("/api/products/{product_id}/stock")
async def api_get_stock(product_id: str):
    items = await db.get_all_stock(product_id)
    return items


@app.get("/api/orders")
async def api_get_orders():
    return await db.get_all_orders()


@app.get("/api/stats")
async def api_get_stats():
    return await db.get_stats()


@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}


@app.get("/webhook/epay")
async def epay_notify(request: Request):
    """易支付回调"""
    params = dict(request.query_params)
    # TODO: 验证签名、标记订单
    return {"status": "ok"}


@app.post("/webhook/stripe")
async def stripe_webhook(request: Request):
    """Stripe webhook"""
    body = await request.body()
    signature = request.headers.get("stripe-signature", "")
    # TODO: 验证签名、处理订单
    return {"status": "ok"}


@app.get("/webhook/nowpayments")
async def nowpayments_ipn(request: Request):
    """NOWPayments IPN"""
    signature = request.headers.get("X-NOWPayments-Signature", "")
    body = await request.body()
    # TODO: 验证签名、处理订单
    return {"status": "ok"}


@app.get("/api/payments/gateways")
async def api_payment_gateways():
    """获取可用支付网关"""
    from payments import _available_gateways
    return {"gateways": list(_available_gateways.keys())}
