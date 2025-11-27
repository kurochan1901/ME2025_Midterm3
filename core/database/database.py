import datetime
import os
import random
import sqlite3


class Database():

    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)

    # 產生訂單 ID
    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    # 查詢分類下所有商品名稱
    def get_product_names_by_category(self, category):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("SELECT product FROM commodity WHERE category = ?", (category,))
        rows = cur.fetchall()
        conn.close()

        return [r[0] for r in rows]

    # 查詢商品價格
    def get_product_price(self, product):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("SELECT price FROM commodity WHERE product = ?", (product,))
        row = cur.fetchone()
        conn.close()

        return row[0] if row else None

    # 新增訂單
    def add_order(self, order_data):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO order_list
            (order_id, date, customer_name, product, amount, total, status, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            order_data["order_id"],
            order_data["product_date"],
            order_data["customer_name"],
            order_data["product_name"],
            order_data["product_amount"],
            order_data["product_total"],
            order_data["product_status"],
            order_data["product_note"]
        ))

        conn.commit()
        conn.close()
        return True

    # 查詢所有訂單（JOIN commodity 取 price）
    def get_all_orders(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                o.order_id, o.date, o.customer_name, 
                o.product, o.amount, o.total, o.status, o.note,
                c.price
            FROM order_list o
            LEFT JOIN commodity c ON o.product = c.product
            ORDER BY o.date DESC
        """)

        rows = cur.fetchall()
        conn.close()
        return rows

    # 刪除訂單
    def delete_order(self, order_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM order_list WHERE order_id = ?", (order_id,))
        conn.commit()
        conn.close()
        return True
