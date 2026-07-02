# 🎫 Telegram Auto Card Delivery System

> 开源 · 自托管 · 多支付 · 在 Telegram 里自动售卖数字商品

<div align="right">

🌐 **语言 / Language**: [English](#english) · [中文](#中文)

</div>

---

## English

TG-Faka is an **open-source digital card delivery bot** for Telegram. Sell gift cards, license keys, game codes, or any digital goods automatically — browse, pay, receive — all inside Telegram, zero manual work.

### Quick Start

You can run TG-Faka in **30 seconds**:

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Fake
pip install -r requirements.txt
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

Then:
- 🌐 Admin dashboard: `http://your-server-ip:8001`
- 🤖 In Telegram, start your bot and send `/start`

> Note: Replace `your-server-ip` with your actual IP or domain. The service binds to `0.0.0.0` so it's accessible from outside.

### First-Time Setup

1. **Create a Telegram Bot** — talk to [@BotFather](https://t.me/BotFather) on Telegram, send `/newbot`, and copy the token.
2. **Get your Telegram ID** — talk to [@userinfobot](https://t.me/userinfobot) on Telegram, copy the number.
3. **Configure** — copy `.env.example` to `.env` and fill in:

```env
BOT_TOKEN=123456:ABC-DEF...
ADMIN_TG_ID=your-telegram-id
PAYMENT_MODE=simulate
```

4. **Run again** — now your bot is live. Access the admin dashboard at `http://your-server-ip:8001`.

### Deploy with Docker

```bash
docker compose up -d
```

Data persists in `./data` across restarts.

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `WEB_HOST` | `0.0.0.0` | IP the service binds to |
| `WEB_PORT` | `8001` | Port the service listens on |
| `BOT_TOKEN` | _(none)_ | Telegram Bot token (required) |
| `ADMIN_TG_ID` | `0` | Your Telegram admin ID |
| `PAYMENT_MODE` | `simulate` | `simulate` · `epay` · `nowpayments` · `stripe` |
| `DEFAULT_LOCALE` | `zh` | Default UI language: `zh` or `en` |

### Access the Dashboard

After deployment, open your browser and go to:

- **`http://your-server-ip:8001`** — if running on a VPS/cloud server with a public IP
- **`http://localhost:8001`** — if testing locally on your machine

Use the **🌐 EN / 中文** button in the top corner to switch the UI language.

### Custom Domain & Reverse Proxy

To use a domain (e.g. `panel.yourdomain.com`), set up a reverse proxy with Nginx:

```nginx
server {
    listen 80;
    server_name panel.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Payment Gateways

| Mode | Description | What to configure |
|------|-------------|------------------|
| `simulate` | Test mode — orders complete instantly | Nothing |
| `epay` | Alipay / WeChat QR (China) | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | Bitcoin, USDT, 100+ cryptos | `NOWPAYMENTS_API_KEY` |
| `stripe` | Visa / Mastercard | `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` |

> ℹ️ For payment callbacks to work, your service **must be accessible from the Internet**. Localhost-only deployments can receive simulated payments only.

[See full payment setup guide →](README.md#支付网关配置)

---

## 中文

TG-Faka 是一个 **开源的 Telegram 自动发卡机器人**。在 Telegram 里卖礼品卡、序列号、游戏 Key 等数字商品 — 浏览、下单、发货全自动，零人工。

### 快速部署

**30 秒启动**：

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Fake
pip install -r requirements.txt
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

启动后：
- 🌐 管理后台：`http://你的服务器IP:8001`
- 🤖 在 Telegram 里找到机器人，发 `/start` 使用

> 注：`你的服务器IP` 替换为实际 IP 或域名。服务默认绑定 `0.0.0.0`，支持外部访问。

### 首次配置

1. **创建 Telegram 机器人** — 给 Telegram 的 [@BotFather](https://t.me/BotFather) 发 `/newbot`，获取 Token
2. **获取你的 Telegram ID** — 给 Telegram 的 [@userinfobot](https://t.me/userinfobot) 发条消息，获取数字 ID
3. **配置** — 复制 `.env.example` 为 `.env`，填入：

```env
BOT_TOKEN=123456:ABC-DEF...
ADMIN_TG_ID=你的telegram-id
PAYMENT_MODE=simulate
```

4. **重新运行** — 机器人上线，管理后台访问 `http://你的服务器IP:8001`

### Docker 部署

```bash
docker compose up -d
```

数据持久化在 `./data` 目录，重启不丢失。

### 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `WEB_HOST` | `0.0.0.0` | 服务绑定的 IP |
| `WEB_PORT` | `8001` | 服务监听的端口 |
| `BOT_TOKEN` | _(无)_ | Telegram Bot 令牌（必填） |
| `ADMIN_TG_ID` | `0` | 你的 Telegram 管理员 ID |
| `PAYMENT_MODE` | `simulate` | `simulate` · `epay` · `nowpayments` · `stripe` |
| `DEFAULT_LOCALE` | `zh` | 默认 UI 语言：`zh` 或 `en` |

### 访问管理后台

部署完成后，打开浏览器：

- **`http://你的服务器IP:8001`** — VPS / 云服务器，用公网 IP
- **`http://localhost:8001`** — 本地机器测试

用右上角的 **🌐 EN / 中文** 按钮切换界面语言。

### 自定义域名 & 反向代理

想用域名访问（比如 `panel.yourdomain.com`），用 Nginx 反代：

```nginx
server {
    listen 80;
    server_name panel.yourdomain.com;
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 支付网关配置

本项目通过 `.env` 中的 `PAYMENT_MODE` 切换支付方式：

| 模式 | 支付方式 | 需要填写的字段 |
|------|----------|----------------|
| `simulate` | 模拟支付（测试用，秒完成） | 无需填写 |
| `epay` | 易支付（支付宝 / 微信扫码） | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | 加密货币（比特币、USDT 等 100+） | `NOWPAYMENTS_API_KEY` |
| `stripe` | 国际信用卡（Visa/Mastercard） | `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` |

> ℹ️ 接入真实支付需要服务**能从公网访问**，本地 localhost 部署只能使用模拟支付。

#### NOWPayments 配置（加密货币）

1. 去 [nowpayments.io](https://nowpayments.io) 注册
2. 获取 API Key
3. 填入 `.env`：

```env
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-api-key
NOWPAYMENTS_SANDBOX=true   # 测试时开启，正式环境改为 false
```

#### Stripe 配置（信用卡）

1. 去 [stripe.com](https://stripe.com) 注册
2. 从 Dashboard 获取 API Key
3. 填入 `.env`：

```env
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

#### 易支付配置（支付宝/微信）

```env
PAYMENT_MODE=epay
EPAY_PID=你的商户ID
EPAY_KEY=商户密钥
EPAY_URL=https://xxx.com/submit.php
```

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
