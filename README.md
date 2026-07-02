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
cd Tg-Faka
pip install -r requirements.txt
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

Then:
- 🌐 Admin dashboard: `http://localhost:8001`
- 🤖 In Telegram, start your bot and send `/start`

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

### Deployment Scenarios

#### 🔹 Option 1: Local Testing (localhost)

No external access. Good for getting familiar with the system.

```bash
python -m uvicorn web:app --host 127.0.0.1 --port 8001
```

Dashboard: `http://localhost:8001`

> ⚠️ **Payment limitation**: Only `simulate` mode works locally. Real payments need a public address.

---

#### 🔹 Option 2: VPS with IP Access (Port-based)

Deploy to any cloud server (Tencent Cloud, Alibaba Cloud, AWS, Vultr, etc.) and access via `http://IP:PORT`.

**.env:**

```env
WEB_HOST=0.0.0.0
WEB_PORT=8001
```

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

Dashboard: `http://your-server-ip:8001`

> ⚠️ **Firewall**: Open port `8001` (or your custom port) in your cloud provider's security group / firewall.
> 
> 💡 **Tip**: To use a different port (e.g. `80` or `443`), set `WEB_PORT=80` in `.env`.

---

#### 🔹 Option 3: VPS with Domain + Reverse Proxy (Recommended for Production)

Use your own domain (e.g. `panel.yourdomain.com`) with Nginx reverse proxy. Supports HTTPS.

##### Step 1: Point domain to server

Add an **A record** in your DNS provider:

| Type | Name | Value |
|------|------|-------|
| A | `panel` (or `@`) | `your-server-ip` |

##### Step 2: Configure TG-Faka

**.env:**

```env
WEB_HOST=127.0.0.1
WEB_PORT=8001
```

> 🔒 Bind to `127.0.0.1` only — not directly exposed to the internet.

##### Step 3: Nginx site config

```nginx
server {
    listen 80;
    server_name panel.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Dashboard: `http://panel.yourdomain.com`

##### Step 4: Enable HTTPS (Let's Encrypt) — Required for Payments

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d panel.yourdomain.com
```

Automatically renews. Dashboard is now:
**`https://panel.yourdomain.com`**

---

#### 🔹 Option 4: Docker (Any Environment)

```bash
docker compose up -d
```

Data persists in `./data` across restarts. Same access rules as above apply based on your `WEB_HOST`/`WEB_PORT` settings.

---

### Access the Dashboard

After deployment:

| Scenario | URL |
|----------|-----|
| Local testing | `http://localhost:8001` |
| VPS with IP | `http://your-server-ip:8001` |
| Domain + Nginx | `http://panel.yourdomain.com` |
| HTTPS (recommended) | `https://panel.yourdomain.com` |

Use the **🌐 EN / 中文** button in the top corner to switch the UI language.

---

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `WEB_HOST` | `0.0.0.0` | IP to bind: `0.0.0.0` for direct access, `127.0.0.1` behind reverse proxy |
| `WEB_PORT` | `8001` | Port the service listens on |
| `BOT_TOKEN` | _(none)_ | Telegram Bot token (required) |
| `ADMIN_TG_ID` | `0` | Your Telegram admin ID |
| `PAYMENT_MODE` | `simulate` | `simulate` · `epay` · `nowpayments` · `stripe` |
| `DATABASE_PATH` | `./faka.db` | Database file path (override for Docker volume) |
| `DEFAULT_LOCALE` | `zh` | Default UI language: `zh` or `en` |

---

### Payment Gateways

| Mode | Description | What to configure |
|------|-------------|------------------|
| `simulate` | Test mode — orders complete instantly | Nothing |
| `epay` | Alipay / WeChat QR (China) | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | Bitcoin, USDT, 100+ cryptos | `NOWPAYMENTS_API_KEY` |
| `stripe` | Visa / Mastercard | `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` |

> ℹ️ **Internet required**: For payment callbacks to work, your service **must be reachable from the public internet** (Option 2 or 3). Localhost-only deployment supports simulated payments only.

#### NOWPayments Setup

```env
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-api-key
NOWPAYMENTS_IPN_SECRET=your-ipn-secret
NOWPAYMENTS_SANDBOX=true   # false in production
```

#### Stripe Setup

```env
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

#### EPAY Setup

```env
PAYMENT_MODE=epay
EPAY_PID=your-merchant-id
EPAY_KEY=your-merchant-key
EPAY_URL=https://xxx.com/submit.php
```

---

## 中文

TG-Faka 是一个 **开源的 Telegram 自动发卡机器人**。在 Telegram 里卖礼品卡、序列号、游戏 Key 等数字商品 — 浏览、下单、发货全自动，零人工。

---

### 快速启动

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Faka
pip install -r requirements.txt
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

启动后：
- 🌐 管理后台：`http://localhost:8001`
- 🤖 在 Telegram 里找到机器人，发 `/start` 使用

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

#### 🔹 方式一：本地测试（localhost）

不暴露外网，适合先跑通流程。

```bash
python -m uvicorn web:app --host 127.0.0.1 --port 8001
```

管理后台：`http://localhost:8001`

> ⚠️ **支付限制**：只能使用模拟支付。真实支付需要公网地址。

---

#### 🔹 方式二：VPS 公网 IP 访问（端口直连）

部署到任意云服务器（腾讯云、阿里云、AWS、Vultr 等），通过 `http://IP:端口` 访问。

**.env：**

```env
WEB_HOST=0.0.0.0
WEB_PORT=8001
```

```bash
python -m uvicorn web:app --host 0.0.0.0 --port 8001
```

管理后台：`http://你的服务器IP:8001`

> ⚠️ **安全组/防火墙**：在云厂商控制台开放对应端口（如 `8001`）。
>
> 💡 **改端口**：想用 `80` 或 `443`？改 `WEB_PORT=80` 即可。

---

#### 🔹 方式三：VPS + 域名 + 反向代理（推荐生产环境）

用自己的域名（如 `panel.yourdomain.com`），配合 Nginx + HTTPS。

##### 第一步：域名解析

在你的 DNS 服务商添加 **A 记录**：

| 类型 | 名称 | 值 |
|------|------|-----|
| A | `panel`（或 `@`） | `你的服务器IP` |

##### 第二步：配置 TG-Faka

**.env：**

```env
WEB_HOST=127.0.0.1
WEB_PORT=8001
```

> 🔒 绑定 `127.0.0.1`，仅本机可访问，Nginx 反代后外网才能触达。

##### 第三步：Nginx 站点配置

```nginx
server {
    listen 80;
    server_name panel.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

重载 Nginx：

```bash
sudo nginx -t
sudo systemctl reload nginx
```

管理后台：`http://panel.yourdomain.com`

##### 第四步：开启 HTTPS（Let's Encrypt，支付必须）

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d panel.yourdomain.com
```

自动续签。管理后台变为：
**`https://panel.yourdomain.com`**

---

#### 🔹 方式四：Docker（任意环境通用）

```bash
docker compose up -d
```

数据持久化在 `./data`，重启不丢失。访问规则与上面保持一致，取决于 `WEB_HOST`/`WEB_PORT` 设置。

---

### 访问管理后台

部署完成后，打开浏览器：

| 场景 | 地址 |
|------|------|
| 本地测试 | `http://localhost:8001` |
| VPS 公网 IP | `http://你的服务器IP:8001` |
| 域名 + Nginx | `http://panel.yourdomain.com` |
| HTTPS（推荐） | `https://panel.yourdomain.com` |

用右上角 **🌐 EN / 中文** 按钮切换界面语言。

---

### 环境变量

| 变量 | 默认值 | 用途 |
|------|--------|------|
| `WEB_HOST` | `0.0.0.0` | 绑定 IP：`0.0.0.0` 直连暴露，`127.0.0.1` 走反代 |
| `WEB_PORT` | `8001` | 服务监听端口 |
| `BOT_TOKEN` | _(无)_ | Telegram Bot 令牌（必填） |
| `ADMIN_TG_ID` | `0` | 你的 Telegram 管理员 ID |
| `PAYMENT_MODE` | `simulate` | `simulate` · `epay` · `nowpayments` · `stripe` |
| `DATABASE_PATH` | `./faka.db` | 数据库文件路径（Docker volume 挂载时覆盖） |
| `DEFAULT_LOCALE` | `zh` | 默认 UI 语言：`zh` 或 `en` |

---

### 支付网关配置

| 模式 | 支付方式 | 需要填写的字段 |
|------|----------|----------------|
| `simulate` | 模拟支付（测试用，秒完成） | 无需填写 |
| `epay` | 易支付（支付宝 / 微信扫码） | `EPAY_PID`, `EPAY_KEY`, `EPAY_URL` |
| `nowpayments` | 加密货币（比特币、USDT 等 100+） | `NOWPAYMENTS_API_KEY` |
| `stripe` | 国际信用卡（Visa/Mastercard） | `STRIPE_API_KEY`, `STRIPE_WEBHOOK_SECRET` |

> ℹ️ **公网要求**：接入真实支付需要服务**能从公网访问**（方式二或方式三）。本地 localhost 部署只能使用模拟支付。

#### NOWPayments 配置（加密货币）

```env
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=your-api-key
NOWPAYMENTS_IPN_SECRET=your-ipn-secret
NOWPAYMENTS_SANDBOX=true   # 测试开启，正式环境关闭
```

#### Stripe 配置（信用卡）

```env
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
```

#### 易支付配置（支付宝/微信）

```env
PAYMENT_MODE=epay
EPAY_PID=商户ID
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
