"""Telegram Bot 核心 - 用户端交互"""
import os
from datetime import datetime
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler, MessageHandler,
    filters, ContextTypes
)

import config
# Use config.BOT_TOKEN, config.SUPPORT_USERNAME, etc.
import database as db


async def init_bot():
    """初始化并启动 Bot（Polling 模式）"""
    await db.init_db()
    app = Application.builder().token(config.BOT_TOKEN).build()

    # 命令路由
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("products", cmd_products))

    # 回调按钮
    app.add_handler(CallbackQueryHandler(callback_handler))

    # 兜底明文消息
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print(f"[Bot] Running in POLLING mode...")
    await app.run_polling(drop_pending_updates=True)


# ==================== 命令处理 ====================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """欢迎"""
    welcome = (
        f"👋 欢迎使用自动发卡系统！\n\n"
        f"→ 使用 /products 浏览商品列表\n\n"
        f"有问题请联系 @{config.SUPPORT_USERNAME}"
    )
    await update.message.reply_text(welcome)


async def cmd_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """商品列表"""
    products = await db.get_all_products()
    if not products:
        await update.message.reply_text("暂无商品，稍后再来~")
        return

    await send_product_list(update, context)


async def send_product_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """发送/编辑商品列表"""
    products = await db.get_all_products()
    keyboard = []
    for p in products:
        stock = await db.get_stock_count(p["id"])
        keyboard.append([
            InlineKeyboardButton(
                text=f"📦 {p['name']} | ¥{p['price']} | 库存: {stock}",
                callback_data=f"view:{p['id']}"
            )
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🛍️ **商品列表**\n\n点击商品查看详情："

    if update.callback_query:
        await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")


# ==================== 回调处理 ====================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """处理内联按钮点击"""
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat.id

    if data.startswith("view:"):
        product_id = data.split(":")[1]
        await show_product_detail(update, context, product_id)

    elif data.startswith("buy:"):
        product_id = data.split(":")[1]
        await start_buy(update, context, product_id)

    elif data == "back_products":
        await send_product_list(update, context)

    elif data.startswith("pay:order:"):
        order_id = data.split(":")[2]
        await check_payment(update, context, order_id)

    await query.answer()


async def show_product_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, product_id: str):
    """显示商品详情"""
    product = await db.get_product_by_id(product_id)
    if not product:
        await update.callback_query.edit_message_text("❌ 商品不存在")
        return

    stock = await db.get_stock_count(product_id)

    text = (
        f"📦 **{product['name']}**\n\n"
        f"📝 {product['description'] or '暂无描述'}\n"
        f"💰 价格: **¥{product['price']}**\n"
        f"📊 库存: **{stock}** 件\n\n"
        f"⏰ 购买后请在 {config.ORDER_DURATION_MINUTES} 分钟内完成支付"
    )

    keyboard = [
        [InlineKeyboardButton("🛒 立即购买", callback_data=f"buy:{product_id}")],
        [InlineKeyboardButton("⬅️ 返回列表", callback_data="back_products")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")


async def start_buy(update: Update, context: ContextTypes.DEFAULT_TYPE, product_id: str):
    """创建订单"""
    product = await db.get_product_by_id(product_id)
    if not product:
        await update.callback_query.edit_message_text("❌ 商品不存在")
        return

    chat_id = update.effective_message.chat.id
    message_id = update.effective_message.message_id

    # 检查未支付订单
    pending = await db.get_user_pending_order(chat_id)
    if pending:
        await update.callback_query.edit_message_text(
            f"⏳ 你有未完成的订单：\n{pending[0]['product_name']} - ¥{pending[0]['price']}\n"
            "请先完成支付或等待订单过期（30 分钟自动取消）。"
        )
        return

    # 创建订单
    order_id = await db.create_order(
        product_id=product["id"],
        product_name=product["name"],
        price=product["price"],
        tg_chat_id=chat_id,
        tg_message_id=message_id,
        duration_minutes=config.ORDER_DURATION_MINUTES,
    )

    end_time = datetime.now().timestamp() + config.ORDER_DURATION_MINUTES * 60

    # 根据支付模式生成支付链接
    pay_url = None
    pay_label = "✅ 模拟支付"

    if config.PAYMENT_MODE == "nowpayments":
        from payments import get_gateway
        gw = get_gateway("nowpayments")
        result = await gw.create_payment(
            amount=product["price"],
            order_id=order_id,
            description=product["name"],
        )
        pay_url = result.get("pay_address") or result.get("pay_url")
    elif config.PAYMENT_MODE == "stripe":
        from payments import get_gateway
        gw = get_gateway("stripe")
        result = await gw.create_payment_intent(
            amount=product["price"],
            description=product["name"],
        )
        pay_url = f"stripe:{result.get('client_secret')}"
    elif config.PAYMENT_MODE == "epay":
        from payments import get_gateway
        gw = get_gateway("epay")
        result = gw.create_order(
            order_id=order_id,
            amount=product["price"],
            title=product["name"],
        )
        pay_url = result.get("pay_url")

    # 构建消息文本
    text = (
        f"🧾 **订单已创建**\n\n"
        f"📦 商品: {product['name']}\n"
        f"💰 金额: **¥{product['price']}**\n"
        f"⏰ 支付截止: {datetime.fromtimestamp(end_time).strftime('%H:%M:%S')}\n"
    )
    if pay_url:
        text += f"\n💳 支付方式: {config.PAYMENT_MODE}"
    else:
        text += "\n💡 模拟支付：点击下方按钮直接标记已支付"

    # 构建按钮
    if pay_url and config.PAYMENT_MODE != "simulate":
        keyboard = [
            [InlineKeyboardButton("💳 去支付", url=pay_url)],
            [InlineKeyboardButton("✅ 模拟回调", callback_data=f"pay:order:{order_id}")],
            [InlineKeyboardButton("🗑️ 取消", callback_data="back_products")],
        ]
    else:
        keyboard = [
            [InlineKeyboardButton(pay_label, callback_data=f"pay:order:{order_id}")],
            [InlineKeyboardButton("🗑️ 取消", callback_data="back_products")],
        ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(
        text=text, reply_markup=reply_markup, parse_mode="Markdown"
    )


async def check_payment(update: Update, context: ContextTypes.DEFAULT_TYPE, order_id: str):
    """支付完成回调（模拟）"""
    order = await db.get_order_by_id(order_id)
    if not order:
        await update.callback_query.edit_message_text("❌ 订单不存在")
        return

    if order["status"] == 1:
        await update.callback_query.edit_message_text("✅ 该订单已支付")
        return

    # 标记已支付
    await db.mark_order_paid(order_id)

    # 发货：消耗库存
    content = await db.consume_stock(order["product_id"], order_id)

    if content:
        text = f"🎉 **支付成功！**\n\n📦 商品: {order['product_name']}\n💰 金额: **¥{order['price']}**\n\n🔑 **发货内容：**\n```\n{content}\n```"
    else:
        text = f"⚠️ **支付成功但库存不足**\n\n请联系 @{config.SUPPORT_USERNAME} 补发"

    keyboard = [[InlineKeyboardButton("⬅️ 返回商品列表", callback_data="back_products")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="Markdown")


# ==================== 管理员命令 ====================

async def admin_cmd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """管理员命令"""
    chat_id = update.message.chat.id
    if chat_id != config.ADMIN_TG_ID:
        return

    text = update.message.text.strip()

    if text == "/admin":
        keyboard = [
            [InlineKeyboardButton("📦 管理商品", callback_data="admin:products")],
            [InlineKeyboardButton("📋 订单列表", callback_data="admin:orders")],
            [InlineKeyboardButton("📊 数据统计", callback_data="admin:stats")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🔐 **管理面板**", reply_markup=reply_markup, parse_mode="Markdown")

    elif text.startswith("/add "):
        # /add 商品名 描述 价格
        parts = text[4:].strip().split()
        if len(parts) >= 3:
            name, desc, price = parts[0], " ".join(parts[1:-1]), parts[-1]
            try:
                pid = await db.create_product(name, desc, float(price))
                await update.message.reply_text(f"✅ 商品添加成功，ID: `{pid}`")
            except ValueError:
                await update.message.reply_text("❌ 价格格式错误")
        else:
            await update.message.reply_text("格式: `/add 商品名 描述 价格`")

    elif text.startswith("/stock "):
        # /stock 商品ID → 显示库存
        parts = text[7:].strip().split()
        if len(parts) == 2:
            pid = parts[0]
            items = await db.get_all_stock(pid)
            if items:
                text = "\n".join([f"{i['content']}" for i in items])
                await update.message.reply_text(f"库存列表:\n{text}")
            else:
                await update.message.reply_text("暂无库存")
        else:
            await update.message.reply_text("格式: `/stock 商品ID`")

    elif text.startswith("/addstock "):
        # /addstock 商品ID → 逐行输入库存
        parts = text.split()
        if len(parts) >= 2:
            pid = parts[1]
            contents = text[len("/addstock "):]
            await db.add_product_items(pid, [contents])
            await update.message.reply_text("✅ 库存添加成功")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """兜底文本消息处理"""
    if update.message.chat.id == config.ADMIN_TG_ID:
        await admin_cmd_handler(update, context)
    else:
        await update.message.reply_text("请使用 /products 查看商品列表")
