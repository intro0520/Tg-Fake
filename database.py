"""数据库模块 - 发卡系统"""
import aiosqlite
import os
from datetime import datetime, timedelta
from decimal import Decimal
from uuid import uuid4

import config

DB_PATH = config.DATABASE_PATH


async def init_db():
    """初始化数据库"""
    async with aiosqlite.connect(DB_PATH) as db:
        # 商品表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                status INTEGER DEFAULT 1,
                created_at INTEGER NOT NULL,
                sort_order INTEGER DEFAULT 0
            )
        """)
        # 库存表（每一条就是一个发货内容）
        await db.execute("""
            CREATE TABLE IF NOT EXISTS product_items (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                content TEXT NOT NULL,
                status INTEGER DEFAULT 1,
                order_id TEXT,
                created_at INTEGER NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
            )
        """)
        # 订单表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                product_id TEXT NOT NULL,
                product_name TEXT NOT NULL,
                price REAL NOT NULL,
                tg_chat_id INTEGER NOT NULL,
                tg_message_id INTEGER,
                status INTEGER DEFAULT 0,
                created_at INTEGER NOT NULL,
                end_time INTEGER NOT NULL,
                paid_at INTEGER,
                FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
            )
        """)
        await db.commit()


# ==================== 商品操作 ====================

async def get_all_products():
    """获取所有商品（包含库存统计）"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("""
            SELECT p.*,
                   (SELECT COUNT(*) FROM product_items WHERE product_id = p.id AND status = 1) as stock_count,
                   (SELECT COUNT(*) FROM orders WHERE product_id = p.id) as order_count
            FROM products p
            WHERE p.status = 1
            ORDER BY p.sort_order DESC, p.created_at DESC
        """)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_product_by_id(product_id: str):
    """通过 ID 获取商品"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def create_product(name: str, description: str, price: float):
    """创建商品"""
    product_id = str(uuid4())
    now = int(datetime.now().timestamp())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO products (id, name, description, price, created_at) VALUES (?, ?, ?, ?, ?)",
            (product_id, name, description, price, now)
        )
        await db.commit()
    return product_id


async def delete_product(product_id: str):
    """删除商品（级联删除库存和订单）"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM product_items WHERE product_id = ?", (product_id,))
        await db.execute("DELETE FROM orders WHERE product_id = ?", (product_id,))
        await db.execute("DELETE FROM products WHERE id = ?", (product_id,))
        await db.commit()


# ==================== 库存操作 ====================

async def add_product_items(product_id: str, contents: list[str]):
    """批量添加库存"""
    now = int(datetime.now().timestamp())
    async with aiosqlite.connect(DB_PATH) as db:
        for content in contents:
            if content.strip():
                item_id = str(uuid4())
                await db.execute(
                    "INSERT INTO product_items (id, product_id, content, created_at) VALUES (?, ?, ?, ?)",
                    (item_id, product_id, content.strip(), now)
                )
        await db.commit()


async def get_stock_count(product_id: str) -> int:
    """获取某商品可用库存数"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT COUNT(*) FROM product_items WHERE product_id = ? AND status = 1", (product_id,)
        )
        result = await cursor.fetchone()
        return result[0] if result else 0


async def get_all_stock(product_id: str):
    """获取某商品所有库存"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM product_items WHERE product_id = ? ORDER BY created_at DESC", (product_id,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def consume_stock(product_id: str, order_id: str) -> str | None:
    """消耗库存（给订单发货），返回发货内容"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "SELECT id, content FROM product_items WHERE product_id = ? AND status = 1 LIMIT 1",
            (product_id,)
        )
        row = await cursor.fetchone()
        if not row:
            return None
        item_id, content = row
        await db.execute(
            "UPDATE product_items SET status = 2, order_id = ? WHERE id = ?",
            (order_id, item_id)
        )
        await db.commit()
        return content


async def delete_all_stock(product_id: str):
    """清空某商品库存"""
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("DELETE FROM product_items WHERE product_id = ?", (product_id,))
        await db.commit()


# ==================== 订单操作 ====================

async def get_user_pending_order(tg_chat_id: int):
    """获取用户未支付订单"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM orders WHERE tg_chat_id = ? AND status = 0", (tg_chat_id,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def create_order(product_id: str, product_name: str, price: float,
                     tg_chat_id: int, tg_message_id: int, duration_minutes: int = 30):
    """创建订单"""
    order_id = str(uuid4())
    now = int(datetime.now().timestamp())
    end_time = now + duration_minutes * 60
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            """INSERT INTO orders (id, product_id, product_name, price, tg_chat_id,
               tg_message_id, created_at, end_time)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (order_id, product_id, product_name, price, tg_chat_id, tg_message_id, now, end_time)
        )
        await db.commit()
    return order_id


async def get_order_by_id(order_id: str):
    """通过 ID 获取订单"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None


async def mark_order_paid(order_id: str):
    """标记订单为已支付"""
    now = int(datetime.now().timestamp())
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE orders SET status = 1, paid_at = ? WHERE id = ?", (now, order_id)
        )
        await db.commit()


async def get_all_orders(limit: int = 100):
    """获取所有订单"""
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT * FROM orders ORDER BY created_at DESC LIMIT ?", (limit,)
        )
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]


async def get_stats():
    """获取统计信息"""
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM products WHERE status = 1")
        products = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM product_items WHERE status = 1")
        stock = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM orders WHERE status = 1")
        paid_orders = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COUNT(*) FROM orders")
        total_orders = (await cursor.fetchone())[0]

        cursor = await db.execute("SELECT COALESCE(SUM(price), 0) FROM orders WHERE status = 1")
        total_revenue = (await cursor.fetchone())[0]

        return {
            "products": products,
            "stock": stock,
            "paid_orders": paid_orders,
            "total_orders": total_orders,
            "total_revenue": total_revenue,
        }
