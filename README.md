<div align="right">

🌐 **Language**: [中文](#) · [English](#readme-en)

</div>

<div align="center">

# 🎫 Telegram Auto Card Delivery System

**Open-source · Self-hosted · Multi-payment**

*Automated digital card delivery bot for Telegram. Sell gift cards, license keys, game codes, and any digital goods.*

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python&logoColor=white)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124%2B-009688?style=flat-square&logo=fastapi&logoColor=white)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-2CA5E0?style=flat-square&logo=telegram&logoColor=white)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

[Features](#features) · [Quick Start](#quick-start) · [Payment Gateways](#payment-gateways) · [Screenshots](#screenshots) · [Development](DEVELOPMENT.md)

</div>

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🤖 **Telegram Bot** | Automated product browsing, ordering, and delivery |
| 🌐 **Web Admin Dashboard** | Clean dark-theme UI for managing products, orders, and inventory |
| 💳 **Multi-Payment Gateway** | Simulated · EPAY · NOWPayments · Stripe |
| 📦 **Inventory Management** | Add stock in bulk, track usage |
| 🔌 **Extensible** | Modular payment gateway, easy to add new providers |
| 🛡 **Order Control** | One pending order per user, timeout auto-cancellation |
| 📊 **Statistics** | Real-time stats for revenue, inventory, and sales |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- pip

### 1. Clone & Install

```bash
git clone https://github.com/your-username/tg-faka.git
cd tg-faka
pip install -r requirements.txt
```

### 2. Configure (optional - works out-of-the-box)

Copy `.env.example` to `.env` and fill in your details:

```bash
copy .env.example .env
```

Minimum config for testing:

```env
# Leave empty for testing - simulated payment enabled by default
BOT_TOKEN=
ADMIN_TG_ID=0
```

For production, configure at minimum:

```env
BOT_TOKEN=123456:ABC-DEF...
ADMIN_TG_ID=123456789
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your_key
```

### 3. Run

#### Development (reload enabled)

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8001 --reload
```

#### Production

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8001 --workers 4
```

Or using Docker:

```bash
docker compose up -d
```

### 4. Access

| Service | URL |
|---------|-----|
| 🌐 Web Admin | `http://localhost:8001` |
| 🔌 API Docs | `http://localhost:8001/docs` |
| 🏥 Health Check | `http://localhost:8001/health` |

---

## 💳 Payment Gateways

The system supports multiple payment gateways, toggle via `PAYMENT_MODE` in `.env`:

| Mode | Description | Config Required |
|------|-------------|----------------|
| `simulate` | Simulated testing (default) | None |
| `epay` | EPAY (Alipay/WeChat QR) | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | Bitcoin, USDT, and 100+ cryptos | `NOWPAYMENTS_API_KEY` |
| `stripe` | Visa/Mastercard credit cards | `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` |

### Setup NOWPayments (Crypto)

1. Register at [nowpayments.io](https://nowpayments.io)
2. Get your API Key
3. Add to `.env`:

```env
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-api-key
NOWPAYMENTS_SANDBOX=true  # set false in production
```

### Setup Stripe (Credit Cards)

1. Register at [stripe.com](https://stripe.com)
2. Get API Keys from Dashboard
3. Add to `.env`:

```env
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

---

## 📁 Project Structure

```
tg-faka/
├── web.py                 # FastAPI web admin + API
├── bot.py                 # Telegram Bot core
├── database.py            # SQLite async operations
├── config.py               # Configuration (reads .env)
├── payments/
│   ├── __init__.py        # Gateway manager + auto-loading
│   ├── epay.py           # EPAY: order, sign, verify
│   ├── nowpayments.py     # NOWPayments: crypto payment + IPN
│   └── stripe_gateway.py  # Stripe: checkout + payment intent
├── templates/              # Web admin HTML templates
├── static/
│   ├── css/style.css       # Dark theme styles
│   └── js/main.js        # Frontend interaction
├── requirements.txt
├── .env.example
└── DEVELOPMENT.md         # Developer documentation
```

---

## 🔌 API Reference

### Products

```
GET    /api/products              List all products
POST   /api/products              Create product
DELETE /api/products/{id}         Delete product
GET    /api/products/{id}/stock   Get stock list
POST   /api/products/{id}/stock   Add stock (form: contents)
DELETE /api/products/{id}/stock   Clear stock
```

### Orders & Stats

```
GET /api/orders          List all orders
GET /api/stats           Revenue, inventory, order stats
GET /api/payments/gateways   List active payment gateways
```

### Webhooks

```
GET  /webhook/epay           EPAY callback
POST /webhook/stripe         Stripe webhook
GET  /webhook/nowpayments    NOWPayments IPN
```

---

## 📸 Screenshots

<details>
<summary><b>📊 Dashboard</b></summary>

![Dashboard](screenshots/dashboard.png)

</details>

<details>
<summary><b>📦 Product Management</b></summary>

![Products](screenshots/products.png)

</details>

<details>
<summary><b>📋 Order Management</b></summary>

![Orders](screenshots/orders.png)

</details>

---

## 🤖 Bot User Flow

```
/start → 👋 Welcome
/products → 🛍️ Browse products
  → 📦 Click product → 🛒 Buy
    → 💳 Payment link (or simulate)
      → ✅ Auto-deliver card/key
```

### Telegram Admin Commands

| Command | Description |
|---------|-------------|
| `/admin` | Admin panel |
| `/add <name> <desc> <price>` | Add new product |
| `/stock <id>` | View stock for product |
| `/addstock <id>` | Add stock items |

---

## 🗄️ Database

SQLite — zero configuration, auto-created on first run.

```sql
-- Main tables
products        -- Product catalog
product_items   -- Inventory (one row = one card/key)
orders          -- Order records
```

---

## 📝 License

MIT

---

<a id="readme-en"></a>

## 🌐 English Version

*Telegram Auto Card Delivery System — open-source, self-hosted digital goods seller bot.*

**Quick Start:**

```bash
git clone https://github.com/your-username/tg-faka.git
cd tg-faka
pip install -r requirements.txt
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

Access admin at: `http://localhost:8001`

See [full API reference](#api-reference) and [payment setup](#payment-gateways) above.
