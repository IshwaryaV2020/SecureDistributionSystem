import sqlite3
from pathlib import Path

def view_products():
    db_path = Path(__file__).resolve().parent / "instance" / "retail.db"

    with sqlite3.connect(db_path) as retail_conn:
        retail_conn.row_factory = sqlite3.Row
        retail_cursor = retail_conn.cursor()

        retail_cursor.execute("""
            SELECT p_id, p_name, p_category, p_price,
                   p_quantity, p_desc, p_sku, p_creationdate
            FROM retail_inventory
            ORDER BY p_id
        """)

        return retail_cursor.fetchall()