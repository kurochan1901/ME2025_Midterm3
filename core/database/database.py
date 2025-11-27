import datetime
import os
import random
import sqlite3

class Database():
    def __init__(self, db_filename="order_management.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(base_dir, db_filename)
    # 產生訂單編號
    @staticmethod
    def generate_order_id() -> str:
        now = datetime.datetime.now()
        timestamp = now.strftime("%Y%m%d%H%M%S")
        random_num = random.randint(1000, 9999)
        return f"OD{timestamp}{random_num}"

    def get_product_names_by_category(self, cur, category):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute(
            "SELECT product FROM commodity WHERE category = ?",
            (category,)
        )
        rows = cur.fetchall()
        conn.close()

        # 回傳商品名稱 string list
        return [r[0] for r in rows]

    def get_product_price(self, cur, product):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute(
            "SELECT price FROM commodity WHERE product = ?",
            (product,)
        )
        row = cur.fetchone()
        conn.close()

        return row[0] if row else None

    def add_order(self, cur, order_data):
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

    def get_all_orders(self, cur):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("SELECT * FROM order_list ORDER BY date DESC")
        rows = cur.fetchall()
        conn.close()
        return rows

    def delete_order(self, cur, order_id):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        cur.execute("DELETE FROM order_list WHERE order_id = ?", (order_id,))
        conn.commit()
        conn.close()
        return True

