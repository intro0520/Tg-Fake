# 🎫 Telegram 发卡系统 v1.0.0

> 基于 **Python + FastAPI + python-telegram-bot** 构建的开源 Telegram 自动发卡系统。
> 参考开源项目 [yuimoi/tg_faka](https://github.com/yuimoi/tg_faka) 重新设计，
> 增加 **Web 管理后台**、**库存管理**、**订单系统**，UI 更加清爽。

---

## ✨ 特性一览

| 功能 | 说明 |
|------|------|
| 🤖 Telegram Bot 端 | 商品浏览、下单、支付（模拟）、自动发货 |
| 🌐 Web 管理后台 | 商品管理、库存管理、订单管理、数据统计 |
| 💾 数据持久化 | SQLite 数据库，开箱即用 |
| 🔌 易扩展支付 | 预留易支付 / 微信支付接口 |
| 🛡 订单防滥用 | 同一用户只能有一个未支付订单 |
| 📊 实时统计 | 收入、订单数、库存一目了然 |
| 🎨 清爽 UI | 暗色主题 Web 管理后台 |

---

## 📁 项目结构

```
telegram-faka/
├── main.py              # 入口文件（同时启动 Web + Bot）
├── bot.py               # Telegram Bot 核心
├── web.py               # FastAPI Web 后台
├── database.py          # 数据库操作
├── config.py            # 配置文件
├── .env                 # 环境变量（从 .env.example 复制）
├── templates/           # Jinja2 模板
│   ├── base.html        # 基础布局
│   ├── index.html       # 仪表盘
│   ├── products.html    # 商品管理
│   └── orders.html      # 订单管理
├── static/              # 静态资源
│   ├── css/
│   │   └── style.css    # 主样式文件
│   └── js/
│       └── main.js      # 前端交互逻辑
├── requirements.txt     # Python 依赖
└── faka.db             # SQLite 数据库（自动创建）
```

---

## 🚀 快速开始

### 1. 环境要求

- Python 3.9+
- pip

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
fastapi>=0.124.0
uvicorn>=0.33.0
python-telegram-bot>=21.6
aiosqlite>=0.20.0
jinja2>=3.1.0
python-multipart>=0.0.20
pydantic>=2.10.0
python-dotenv>=1.0.1
```

### 3. 获取 Telegram Bot Token

1. 在 Telegram 中打开 **@BotFather**
2. 发送 `/newbot` 按提示创建机器人
3. 获得 Token，格式：`123456789:ABCdef...`
4. 通过 **@userinfobot** 获取你的 Telegram ID

### 4. 配置环境变量

```bash
# Windows PowerShell
Copy-Item .env.example .env

# 编辑 .env 文件，填入你的配置
```

**.env 配置项**：
```env
# Telegram
BOT_TOKEN=你的BotToken
ADMIN_TG_ID=你的TelegramID
SUPPORT_USERNAME=admin

# 系统设置
ORDER_DURATION_MINUTES=30
WEB_PORT=8001

# 支付模式
PAYMENT_MODE=simulate

# 易支付配置（可选）
EPAY_PID=
EPAY_KEY=
EPAY_URL=
EPAY_NOTIFY_URL=
```

### 5. 启动系统

```bash
python main.py
```

启动后控制台输出：

```
╔══════════════════════════════════════════════════╗
║         🎫 Telegram 发卡系统 v1.0.0               ║
╠══════════════════════════════════════════════════╣
║  管理后台: http://localhost:8001                ║
║  Bot Token: 已配置                              ║
║  支付模式: simulate                              ║
║  数据库:  ...                                   ║
╚══════════════════════════════════════════════════╝
```

- 管理后台：`http://localhost:8001`
- 在 Telegram 搜索你的机器人，发送 `/start` 使用

---

## 💬 Bot 用户命令

| 命令 | 功能 |
|------|------|
| `/start` | 欢迎页面 |
| `/products` | 浏览商品列表 |

### 用户流程

```
用户 → /products → 点击商品 → 查看详情 → 点击购买 → 确认订单 → 模拟支付 → 发货
```

### 管理员命令（在 Telegram Bot 内）

| 命令 | 功能 |
|------|------|
| `/admin` | 管理员面板 |
| `/add 商品名 描述 价格` | 添加商品 |
| `/stock 商品ID` | 查看库存 |
| `/addstock 商品ID` | 添加库存（逐行） |

---

## 🌐 Web API 接口

### 商品管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/products` | 获取所有商品（含库存统计） |
| POST | `/api/products` | 创建商品（Form: name, description, price） |
| DELETE | `/api/products/{id}` | 删除商品（级联删除库存和订单） |
| GET | `/api/products/{id}/stock` | 获取商品库存列表 |
| POST | `/api/products/{id}/stock` | 添加库存（Form: contents，每行一条） |
| DELETE | `/api/products/{id}/stock` | 清空商品库存 |

### 订单管理

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/orders` | 获取订单列表 |

### 统计

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats` | 获取统计数据 |

### 健康检查

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 服务健康检查 |

---

## 🗄️ 数据库结构

### products（商品表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT PRIMARY KEY | 商品唯一 ID（UUID） |
| name | TEXT NOT NULL | 商品名称 |
| description | TEXT | 商品描述 |
| price | REAL NOT NULL | 价格（元） |
| status | INTEGER | 状态：1=在售 |
| created_at | INTEGER | 创建时间戳 |

### product_items（库存表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT PRIMARY KEY | 库存唯一 ID（UUID） |
| product_id | TEXT NOT NULL | 所属商品 ID |
| content | TEXT NOT NULL | 发货内容（卡号/密钥等） |
| status | INTEGER | 状态：1=可用，2=已售出 |
| order_id | TEXT | 关联订单 ID |
| created_at | INTEGER | 创建时间戳 |

### orders（订单表）

| 字段 | 类型 | 说明 |
|------|------|------|
| id | TEXT PRIMARY KEY | 订单唯一 ID（UUID） |
| product_id | TEXT NOT NULL | 商品 ID |
| product_name | TEXT NOT NULL | 商品名称 |
| price | REAL NOT NULL | 订单金额 |
| tg_chat_id | INTEGER NOT NULL | 用户 Telegram Chat ID |
| status | INTEGER | 状态：0=待支付，1=已支付 |
| created_at | INTEGER | 创建时间戳 |
| end_time | INTEGER | 过期时间戳 |
| paid_at | INTEGER | 支付时间戳 |

---

## 🔌 支付方式对接

### 支持的支付方式

已实现以下支付网关：

| 网关 | 说明 | 配置方式 | Webhook 端点 |
|------|------|----------|-------------|
| **模拟支付** | 默认测试用 | `PAYMENT_MODE=simulate` | — |
| **易支付** | 国内虚拟支付 | `.env` 中配置 EPAY_* | `GET /webhook/epay` |
| **NOWPayments** | 比特币/USDT 等加密货币 | `.env` 中配置 NOWPAYMENTS_* | `GET /webhook/nowpayments` |
| **Stripe** | 国际信用卡（Visa/Mastercard） | `.env` 中配置 STRIPE_* | `POST /webhook/stripe` |

### 切换支付方式

修改 `.env` 中的 `PAYMENT_MODE`：

```env
# 模拟（测试用）
PAYMENT_MODE=simulate

# 易支付（支付宝/微信扫码）
PAYMENT_MODE=epay

# NOWPayments（加密货币）
PAYMENT_MODE=nowpayments

# Stripe（信用卡）
PAYMENT_MODE=stripe
```

### 易支付配置示例

```env
PAYMENT_MODE=epay
EPAY_PID=你的商户ID
EPAY_KEY=商户密钥
EPAY_URL=https://xxx.com/submit.php
EPAY_NOTIFY_URL=https://yourdomain.com/webhook/epay
```

### NOWPayments 配置示例

1. 在 [nowpayments.io](https://nowpayments.io) 注册并获取 API Key
2. 设置 `.env`：

```env
PAYMENT_MODE=nowpayments
NOWPAYMENTS_API_KEY=你的API_KEY
NOWPAYMENTS_SANDBOX=true   # 测试时设为 true
NOWPAYMENTS_SUCCESS_URL=https://yourdomain.com/payment/success
NOWPAYMENTS_CANCEL_URL=https://yourdomain.com/payment/cancel
```

### Stripe 配置示例

1. 在 [stripe.com](https://stripe.com) 注册并获取 API Key
2. 设置 `.env`：

```env
PAYMENT_MODE=stripe
STRIPE_API_KEY=sk_test_xxx  # 测试用
STRIPE_WEBHOOK_SECRET=whsec_xxx  # 从 Stripe Dashboard 获取
```

### 支付流程

```
下单 → 创建订单 → 生成支付链接 → 用户支付 → 回调 → 标记已支付 → 发货
```

### 查看可用网关

```
GET /api/payments/gateways
```

返回当前已加载的支付网关列表。

---

## 🛠 开发与扩展

### 添加支付方式

1. 在 `bot.py` `start_buy()` 中生成支付 URL
2. 在 `web.py` 中实现支付回调 `/webhook/xxx`
3. 在回调中标记订单和发货

### 自定义 UI

修改 `templates/` 下的 HTML 和 `static/css/style.css`。

### 数据库升级

需要添加表时，修改 `database.py` 中的 `init_db()`。

---

## 📝 常见问题

**Q: 如何部署到服务器？**
A: 使用 `nohup python main.py &` 或配置系统服务。

**Q: 如何修改端口？**
A: 修改 `.env` 中的 `WEB_PORT`。

**Q: 数据库数据丢失怎么办？**
A: `faka.db` 是 SQLite 文件，定期备份即可。

**Q: 支持多管理员吗？**
A: 目前只支持单管理员，在 `ADMIN_TG_ID` 修改。

---

## 📜 许可证

MIT License

## 🙏 致谢

- [yuimoi/tg_faka](https://github.com/yuimoi/tg_faka) - 原版 Go 项目
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram Bot 框架
- [FastAPI](https://fastapi.tiangolo.com/) - Web 框架
