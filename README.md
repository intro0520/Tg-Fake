# 🎫 Telegram Auto Card Delivery System / Telegram 自动发卡系统

> **Open-source · Self-hosted · Multi-payment**  
> 开源 · 自托管 · 支持多种支付方式，在 Telegram 里自动售卖数字商品（礼品卡、序列号、游戏 Key 等）。

<div align="right">

🌐 **语言 / Language**: [English](#english--quick-start) · [中文](#中文--快速上手)

</div>

---

## ✨ Features / 功能特色

| Feature 功能 | Description / 描述 |
|---|---|
| 🤖 **Telegram Bot** | 用户发 `/start` 就能看到商品，点击购买自动发货，全程无需人工 |
| 🌐 **Web Admin** 管理后台 | 深色主题仪表盘，管理商品、订单、库存 |
| 💳 **Multi-Payment** 多支付方式 | 模拟支付（开箱即用） · EPAY · NOWPayments · Stripe |
| 📦 **Inventory** 库存管理 | 批量导入卡密，实时统计可用库存 |
| 🛡 **Order Control** 订单控制 | 每人同时最多 1 笔未支付订单，超时自动取消 |

---

## English — Quick Start

### Step 1: Get the code

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Fake
```

### Step 2: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

Then open your browser: **http://localhost:8001**

> 🌐 Click **EN** / **中文** in the top-right corner to switch language.

#### What you'll see

- **Dashboard** — revenue, stock, and order stats at a glance
- **Products** — add products, import card keys, manage stock
- **Orders** — view all orders and customer info

#### Payment is optional for testing

Out of the box, payments are **simulated** — orders complete instantly. To accept real payments, edit your `.env`:

```env
# For crypto (Bitcoin, USDT, etc.)
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-api-key

# For credit cards
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
```

[Full payment setup guide →](README.md#中文--支付配置)

---

## 中文 — 快速上手

### 第一步：拉取项目

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Fake
```

### 第二步：安装依赖

```bash
pip install -r requirements.txt
```

### 第三步：运行

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

打开浏览器访问：**http://localhost:8001**

> 🌐 点击右上角 **中文** / **EN** 切换语言。

#### 你会看到

- **仪表盘** — 一眼看清营收、库存、订单
- **商品管理** — 添加商品、批量导入卡密、查看可用库存
- **订单管理** — 查看所有订单和顾客信息

#### 支付可以暂时不管

默认开启**模拟支付** — 下单秒完成，方便测试。真正收款时再编辑 `.env`：

```env
# 加密货币（比特币、USDT 等）
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-api-key

# 信用卡 / 借记卡
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
```

[完整支付配置指南 →](README.md#中文--支付配置)

---

## 🤖 机器人命令 / Bot Commands

| 命令 Command | 说明 Description |
|---|---|
| `/start` | 👋 开始 / 浏览商品 Welcome & browse |
| `/admin` | 🛠️ 管理员面板 Admin panel |
| `/add 名称 描述 价格` | ➕ 添加商品 Add product |
| `/stock 商品ID` | 📦 查看某商品库存 View inventory |

---

## 💳 中文 — 支付配置

本项目通过 `.env` 里的 `PAYMENT_MODE` 切换支付方式：

| 模式 | 支付方式 | 需要填写的字段 |
|---|---|---|
| `simulate` | 模拟支付（默认，开箱即用） | 无需填写 |
| `epay` | 易支付（支付宝/微信扫码） | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | 加密货币（比特币、USDT 等 100+） | `NOWPAYMENTS_API_KEY` |
| `stripe` | 信用卡（Visa/Mastercard） | `STRIPE_API_KEY` |

### NOWPayments 注册配置

1. 去 [nowpayments.io](https://nowpayments.io) 注册
2. 获取 API Key
3. 填入 `.env`：

```env
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-api-key
NOWPAYMENTS_SANDBOX=true  # 测试时开启，正式环境改为 false
```

### Stripe 注册配置

1. 去 [stripe.com](https://stripe.com) 注册
2. 从 Dashboard 获取 API Key
3. 填入 `.env`：

```env
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

---

## 📁 项目结构 / Project Structure

```
Tg-Fake/
├── web.py                  # FastAPI 管理后台 + API
├── bot.py                  # Telegram 机器人核心
├── database.py             # SQLite 异步数据库
├── config.py               # 读取 .env 配置
├── payments/
│   ├── __init__.py         # 网关管理器（按配置自动加载）
│   ├── epay.py            # 易支付：下单、签名、验证
│   ├── nowpayments.py     # NOWPayments 加密支付 + IPN
│   └── stripe_gateway.py  # Stripe 结账 + Payment Intent
├── templates/               # 管理后台 HTML 模板
├── static/
│   ├── css/style.css       # 深色主题样式
│   └── js/main.js          # 前端交互逻辑
├── requirements.txt
├── .env.example
└── DEVELOPMENT.md           # 开发者文档（API 详情）
```

---

## 📝 License / 许可证

MIT

---

<div align="center">

🌐 **Language**: [English ↑](#english--quick-start) · [中文 ↑](#中文--快速上手)

</div>
