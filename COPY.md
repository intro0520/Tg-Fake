# 文案素材 / Copy Library

---

## 一句话简介 / One-liners

**中文**

- 在 Telegram 里自动卖数字商品的开源工具。顾客下单、付款、收货，全自动。
- 基于 Python + FastAPI 的数字卡密自动发货系统，自托管即开源。
- 用 Telegram Bot 卖游戏 Key、礼品卡、序列号，零人工介入。
- 轻量级数字商品电商 Bot：商品管理 → 库存管理 → 订单处理 → 自动发货。
- 你负责铺货，Bot 负责凌晨两点还在帮你发货。

**English**

- Open-source Telegram bot that sells digital goods while you sleep.
- Python + FastAPI self-hosted card delivery bot — browse, pay, receive, done.
- Sell game keys, gift cards, license codes on Telegram — fully automated.
- Zero-manual digital goods storefront, living inside your Telegram Bot.
- You stock the shelves. The Bot sells at 2am.

---

## 商品介绍文案 / Product Description

### 简短版（GitHub About、Twitter Bio）

**中文（≤150字）**

> TG-Faka 是开源的 Telegram 自动发卡系统。用 Bot 售卖任何数字商品 — 礼品卡、游戏 Key、License、序列号。从浏览到发货全流程自动化。Python 编写，FastAPI 后台，支持易支付/NOWPayments/Stripe，开箱即用。

**English (≤150 chars)**

> TG-Faka is an open-source Telegram bot for automated digital goods delivery. Sell gift cards, game keys, licenses — browse, pay, deliver on autopilot. Python + FastAPI, multi-payment, self-hosted.

---

### 标准版（landing page 首屏、项目文档）

**中文**

#### 🎫 这就是你一直想要的 Telegram 开店方式

**客户走进你的 Bot → 选商品 → 付款 → 秒收卡密。**
全程没有你。没有手动复制粘贴。没有下班后的未读消息。

**TG-Faka** 是一个 100% 开源的数字商品自动发货系统。你部署一次，剩下的事 Bot 全干了。它替你接单、替你处理支付、替你发密码、替你记账。

- 🌐 Web 管理后台，深色主题，商品/订单/库存一览无余
- 📦 批量导入库存，逐条扣减，永不超卖
- 💳 多支付网关：模拟测试 · 易支付 · NOWPayments · Stripe
- 📊 实时统计：销量、库存、收入、订单状态
- 🔐 自主可控：代码全在你手里，数据不依赖任何平台
- 🌍 中英双语，一键切换，开箱即用

**适合谁：** Game Key 卖家、礼品卡经销商、软件 License 卖家、付费社群运营、任何卖数字商品的创业者。

---

#### 🎫 This Is How You Sell on Telegram

**Customer hits your bot → picks a product → pays → receives the key instantly.**
Zero you. No copy-pasting. No unread DMs at midnight.

**TG-Faka** is a 100% open-source digital goods automation system. Deploy once, the Bot does the rest. It takes orders, processes payments, delivers keys, and tracks sales — all while you sleep.

- 🌐 Dark-theme web dashboard — products, orders, inventory at a glance
- 📦 Bulk inventory import — auto-deduct, never oversells
- 💳 Multi-payment — simulate · NOWPayments · Stripe · EPAY
- 📊 Real-time analytics — revenue, stock levels, order stats
- 🔐 Self-hosted — code and data under your control
- 🌍 Bilingual (zh/en) — one click switch

**Built for:** Game key sellers, gift card merchants, software license sellers, paid community operators — anyone selling digital goods.

---

### 长文版（少数派/掘金/CSDN 文章）

**中文**

# 我写了一个 Telegram Bot，凌晨 3 点还在帮我卖东西

去年年底我开始卖一些游戏兑换码，一开始是用微信手动发，生意不错的时候凌晨两点有人下单还要爬起来改库存。后来生意扩大了，我受不了了，于是写了这个项目。

## 它是什么

**TG-Faka** 是一个完全开源的 Telegram 自动发卡系统。用一句话说就是：把 Telegram 变成一个全自动的数字商店。

## 核心架构

整个系统由两部分组成：

**Bot 前端**（`bot.py`）—— 给用户看的商店橱窗。用户发 `/start` 就能看到所有商品，点进商品可以查看详情、选择支付方式、下单。支持一个用户只有一笔未支付订单，30 分钟超时取消。

**Web 后端**（`web.py`）—— 给你用的管理后台。像运营电商平台一样操作：加减商品、批量导入库存、看订单、看收入。深色主题，手机上也能用。

**支付网关**（`payments/`）—— 模块化的支付接口。默认是模拟支付（测得好再上线），已经实现了易支付、NOWPayments（比特币/Stripe、Visa/Mastercard）三个接入门。

**数据库**（`database.py`）—— SQLite + aiosqlite 异步驱动。开箱即用，不用另外部署数据库。

## 我为什么开源

市面上也有类似的发卡系统，但要么就是收费高昂，要么做得太差，要么不懂哪个后门把你的卡密漏了一份。这个项目诞生于我自己的实际需求，我一直用到现在还挺满意。

既然这样就开源吧。代码很干净，没有乱七八糟的依赖，如果你想 fork 改改就能卖自己的东西。

## 30 秒部署

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Faka
pip install -r requirements.txt
python -m uvicorn web:app --port 8000
```

管理后台：`http://localhost:8000`
机器人：找 @BotFather 拿 Token，写进 .env，重启。

30 秒你就有了一个自己的自动发卡商店。MIT 协议，随便用。

## 后续计划

- [ ] 多管理员支持
- [ ] 商品分类 / 搜索
- [ ] 优惠券 / 折扣码
- [ ] 销售报表导出（CSV/Excel）
- [ ] Webhook 通知（新订单 → Telegram/微信推送）

欢迎提 Issue、PR。⭐ Star 是对我最大的鼓励。

---

# I Built a Bot That Sells Stuff at 3 AM

I started selling game codes last year. At first, I used WeChat to deliver manually. Busiest nights, I woke up at 2am to check orders and update stock. Eventually, I couldn't take it anymore — so I built this.

## What It Is

**TG-Faka** is a fully open-source Telegram automated card delivery system. In one sentence: turns your Telegram into a self-running digital store.

## Architecture

The system has two parts:

**Bot Frontend** (`bot.py`) — the storefront for customers. `/start` lists all products — browse, view details, choose payment, order. One pending order per user, 30-minute timeout.

**Web Backend** (`web.py`) — the admin dashboard for you. Manage products, bulk-import stock, view orders, track revenue. Dark theme, mobile-friendly.

**Payment Gateways** (`payments/`) — modular payment interfaces. Default is simulation for testing. Already implemented: EPAY, NOWPayments, and Stripe.

**Database** (`database.py`) — SQLite + aiosqlite async driver. Works out of the box, no extra database setup.

## Why Open Source

Other card delivery systems are either expensive, badly made, or — who knows — leaking your inventory in the background. This project was born from my own frustration and I keep using it because it works.

So I open-sourced it. The code is clean, dependencies are minimal, fork it and make it yours.

## Deploy in 30 Seconds

```bash
git clone https://github.com/intro0520/Tg-Fake.git
cd Tg-Faka
pip install -r requirements.txt
python -m uvicorn web:app --port 8000
```

Dashboard: `http://localhost:8000`
Bot: get a token from @BotFather, put it in `.env`, restart.

30 seconds and your own autopilot store is live. MIT — do literally anything with it.

## Roadmap

- [ ] Multi-admin support
- [ ] Product categories / search
- [ ] Coupon / discount codes
- [ ] Sales export (CSV/Excel)
- [ ] Webhook notifications (new order → Telegram/WeChat push)

Open an issue, submit a PR. ⭐ Stars are the best support.

---

## 适用场景文 / Use-case Copy

### Game Key 卖家

> 你的客人在 Discord 群里问你"有没有 XX 游戏激活码"。
> 告诉他："找我的 Bot 自己下单。"
> 五分钟后他已经在 Steam 上玩了。

### 礼品卡商家

> 节假日前的下单潮让你回复到手软？
> 试试让 Bot 替你接单。客户下单的时候，库存已经在减了。

### 社群运营

> 付费入群的老办法是：转账 → 截图 → 人工拉群。
> 现在改成：Bot 发付款链接 → 系统回调 → Bot 自动发放邀请链接。
> 你可以去睡觉了。

### 软件 License 卖家

> 还在手动发 License 吗？
> TG-Faka 的库存表就是你的 License 库。卖一条减一条，卖了 100 条就自动下架。
> 精准、不变、不遗漏。

---
