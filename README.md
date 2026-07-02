# 🎫 Telegram Auto Card Delivery System

> 开源 · 自托管 · 多支付 · 在 Telegram 里自动售卖数字商品

<div align="right">

🌐 **语言 / Language**: [English](#english) · [中文](#中文)

</div>

---

## English

TG-Faka is an **open-source digital card delivery bot** for Telegram. Sell gift cards, license keys, game codes, or any digital goods automatically — browse, pay, receive — all inside Telegram, zero manual work.

---

### Quick Start

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Fake
pip install -r requirements.txt
python -m uvicorn web:app --host 0.0.0.0 --port 8000
```

Then:
- 🌐 Admin dashboard: `http://localhost:8000`
- 🤖 In Telegram, start your bot and send `/start`

> 💡 **Port is configurable**: Default is `8000`. To change, set `WEB_PORT=8080` in `.env`.

---

### First-Time Setup

1. **Create a Telegram Bot** — talk to [@BotFather](https://t.me/BotFather), send `/newbot`, copy the token.
2. **Get your Telegram ID** — talk to [@userinfobot](https://t.me/userinfobot), copy the number.
3. **Configure** — copy `.env.example` to `.env`:

```env
BOT_TOKEN=123456:ABC-DEF...
ADMIN_TG_ID=your-telegram-id
PAYMENT_MODE=simulate
```

4. **Run again** — your bot is live.

---

### Deployment

Any deployment method works. Choose what fits your setup:

#### 🔹 Local Testing (localhost)

```bash
python -m uvicorn web:app --host 127.0.0.1 --port 8000
```

Dashboard: `http://localhost:8000`

> ⚠️ Only `simulate` payment works locally. Real payments need a public address.

---

#### 🔹 VPS with Public IP

Deploy to any cloud server and access via `http://IP:PORT`.

**.env**:

```env
WEB_HOST=0.0.0.0
WEB_PORT=8000    # any port you like
```

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8000
```

Dashboard: `http://your-server-ip:8000`

Don't forget to open the port in your cloud provider's firewall / security group.

---

#### 🔹 VPS + Domain + Reverse Proxy (Recommended)

Use your own domain with Nginx + HTTPS:

1. **DNS** — point domain to your server IP:

| Type | Name | Value |
|------|------|-------|
| A | `panel` (or `@`) | `your-server-ip` |

2. **TG-Faka** — bind to localhost only:

```env
WEB_HOST=127.0.0.1
WEB_PORT=8000
```

3. **Nginx** — reverse proxy:

```nginx
server {
    listen 80;
    server_name panel.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. **HTTPS** (required for real payments):

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d panel.yourdomain.com
```

Dashboard: `https://panel.yourdomain.com`

---

#### 🔹 Docker

```bash
docker compose up -d
```

Data persists in `./data`. Port and host are controlled by `WEB_HOST` / `WEB_PORT` in `.env`.

---

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `WEB_HOST` | `0.0.0.0` | Bind IP: `0.0.0.0` for direct, `127.0.0.1` behind proxy |
| `WEB_PORT` | `8000` | Any port you want to use |
| `BOT_TOKEN` | _(none)_ | Telegram Bot token (required) |
| `ADMIN_TG_ID` | `0` | Your Telegram admin ID |
| `PAYMENT_MODE` | `simulate` | `simulate` · `epay` · `nowpayments` · `stripe` |
| `DATABASE_PATH` | `./faka.db` | Database file path |
| `DEFAULT_LOCALE` | `zh` | UI language: `zh` or `en` |

---

### Access the Dashboard

| Scenario | URL |
|----------|-----|
| Local testing | `http://localhost:8000` |
| VPS with IP | `http://your-server-ip:8000` |
| Domain + Nginx | `http://panel.yourdomain.com` |
| HTTPS | `https://panel.yourdomain.com` |

Use the **🌐 EN / 中文** button in the top corner to switch the UI language.

---

### Payment Gateways

| Mode | Description | What to configure |
|------|-------------|------------------|
| `simulate` | Test mode — orders complete instantly | Nothing |
| `epay` | Alipay / WeChat QR | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | Bitcoin, USDT, 100+ cryptos | `NOWPAYMENTS_API_KEY` |
| `stripe` | Visa / Mastercard | `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` |

```env
# NOWPayments
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-key

# Stripe
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# EPAY
PAYMENT_MODE=epay
EPAY_PID=your-id
EPAY_KEY=your-key
EPAY_URL=https://xxx.com/submit.php
```

> ℹ️ Real payments require your service to be **reachable from the public internet**. Localhost-only supports simulate mode.

---

### Internationalization (i18n)

This project uses lightweight dictionary-based translation. If you need more advanced i18n features (pluralization, locale detection, etc.), these open-source libraries can be added:

- **[python-i18n](https://github.com/timoldenburg/python-i18n)** — simple YAML-based translations
- **[Babel](https://babel.pocoo.org/)** — full-featured i18n for Python (gettext, pluralization)
- **[fastapi-babel](https://github.com/hepers/fastapi-babel)** — Babel integration for FastAPI

To add a new language: add a new key in `i18n.py` → `TRANSLATIONS` dict, and add corresponding entries to all templates.

---

## 中文

TG-Faka 是一个 **开源的 Telegram 自动发卡机器人**。礼品卡、序列号、游戏 Key、付费群 等数字商品 — 浏览、下单、发货全自动，零人工。

---

### 快速启动

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Faka
pip install -r requirements.txt
python -m uvicorn web:app --host 0.0.0.0 --port 8000
```

启动后：
- 🌐 管理后台：`http://localhost:8000`
- 🤖 在 Telegram 里找到机器人，发 `/start` 使用

> 💡 **端口可配置**：默认 `8000`，改 `.env` 中 `WEB_PORT=8080` 即可。

---

### 首次配置

1. **创建 Telegram 机器人** — 给 [@BotFather](https://t.me/BotFather) 发 `/newbot`，获取 Token
2. **获取你的 Telegram ID** — 给 [@userinfobot](https://t.me/userinfobot) 发条消息，获取数字 ID
3. **配置** — 复制 `.env.example` 为 `.env`：

```env
BOT_TOKEN=123456:ABC-DEF...
ADMIN_TG_ID=你的telegram-id
PAYMENT_MODE=simulate
```

4. **重新运行** — 机器人上线

---

### 部署方式

**任意方式均可部署**，根据你的情况选择：

---

#### 🔹 方式一：本地测试（localhost）

```bash
python -m uvicorn web:app --host 127.0.0.1 --port 8000
```

管理后台：`http://localhost:8000`

> ⚠️ 只能使用模拟支付。真实支付需要公网地址。

---

#### 🔹 方式二：VPS 公网 IP

部署到任意云服务器（腾讯云、阿里云、AWS、Vultr 等）。

**.env：**

```env
WEB_HOST=0.0.0.0
WEB_PORT=8000    # 任意可用端口
```

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8000
```

管理后台：`http://你的服务器IP:8000`

别忘了在云厂商安全组里开放端口。

---

#### 🔹 方式三：VPS + 域名 + 反向代理（推荐生产）

用自家域名 + Nginx + HTTPS：

1. **DNS 解析** — A 记录指向服务器 IP：

| 类型 | 名称 | 值 |
|------|------|-----|
| A | `panel`（或 `@`） | `你的服务器IP` |

2. **TG-Faka** — 绑定本机回环地址，不外露：

```env
WEB_HOST=127.0.0.1
WEB_PORT=8000
```

3. **Nginx 反代**：

```nginx
server {
    listen 80;
    server_name panel.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

4. **HTTPS**（真实支付必须）：

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d panel.yourdomain.com
```

管理后台：`https://panel.yourdomain.com`

---

#### 🔹 方式四：Docker

```bash
docker compose up -d
```

数据持久化在 `./data`。端口通过 `.env` 中的 `WEB_PORT` 控制。

---

### 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `WEB_HOST` | `0.0.0.0` | 绑定 IP：`0.0.0.0` 直连，`127.0.0.1` 走反代 |
| `WEB_PORT` | `8000` | 任意可用端口 |
| `BOT_TOKEN` | _(无)_ | Telegram Bot 令牌（必填） |
| `ADMIN_TG_ID` | `0` | 管理员 Telegram ID |
| `PAYMENT_MODE` | `simulate` | `simulate` · `epay` · `nowpayments` · `stripe` |
| `DATABASE_PATH` | `./faka.db` | 数据库路径 |
| `DEFAULT_LOCALE` | `zh` | UI 语言：`zh` 或 `en` |

---

### 访问管理后台

| 场景 | 地址 |
|------|------|
| 本地测试 | `http://localhost:8000` |
| VPS 公网 IP | `http://你的服务器IP:8000` |
| 域名 + Nginx | `http://panel.yourdomain.com` |
| HTTPS | `https://panel.yourdomain.com` |

右上角 **🌐 EN / 中文** 按钮切换语言。

---

### 支付网关配置

| 模式 | 支付方式 | 配置字段 |
|------|----------|----------|
| `simulate` | 模拟支付（测试用） | 无需填写 |
| `epay` | 易支付（支付宝 / 微信） | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | 加密货币 | `NOWPAYMENTS_API_KEY` |
| `stripe` | 国际信用卡 | `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` |

```env
# NOWPayments
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-key

# Stripe
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# 易支付
PAYMENT_MODE=epay
EPAY_PID=your-id
EPAY_KEY=your-key
EPAY_URL=https://xxx.com/submit.php
```

> ℹ️ 真实支付需要服务**能从公网访问**，本地 localhost 部署只能使用模拟支付。

---

### 多语言翻译（i18n）

本项目使用轻量级字典翻译。如果项目规模扩大，需要更完善的国际化（复数形式、语言自动检测等），可接入以下开源库：

- **[python-i18n](https://github.com/timoldenburg/python-i18n)** — 简单的 YAML 翻译文件方案
- **[Babel](https://babel.pocoo.org/)** — Python 全功能 i18n（gettext、复数形式）
- **[fastapi-babel](https://github.com/hepers/fastapi-babel)** — Babel + FastAPI 集成

添加新语言：在 `i18n.py` 的 `TRANSLATIONS` 字典中新增对应语言键，模板中同步添加翻译即可。

---

## Bot Commands / 机器人命令

| Command / 命令 | Description / 说明 |
|---|---|
| `/start` | 👋 Welcome & browse / 欢迎并浏览商品 |
| `/admin` | 🛠️ Admin panel / 管理员面板 |
| `/add <name> <desc> <price>` | ➕ Add product / 添加商品 |
| `/stock <id>` | 📦 View inventory / 查看库存 |

---

## License / 许可证

MIT

---

<div align="center">

🌐 **Language**: [English ↑](#english) · [中文 ↑](#中文)

</div>
