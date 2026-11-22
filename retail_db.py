
import sqlite3
from pathlib import Path

def create_retail_db():
    db_path = Path(__file__).resolve().parent / "instance" / "retail.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as retail_conn:
        retail_cursor = retail_conn.cursor()

        retail_cursor.execute("""
            CREATE TABLE IF NOT EXISTS retail_inventory (
                p_id INTEGER PRIMARY KEY AUTOINCREMENT,
                p_name TEXT NOT NULL,
                p_category TEXT NOT NULL CHECK (
                    p_category IN (
                        'Clothing',
                        'Bags & accessories',
                        'Electronics & accessories'
                    )
                ),
                p_price INTEGER NOT NULL CHECK (p_price >= 0),
                p_quantity INTEGER NOT NULL CHECK (p_quantity >= 0),
                p_desc TEXT,
                p_sku TEXT NOT NULL UNIQUE,
                p_creationdate TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

        retail_cursor.execute("""
            CREATE TABLE IF NOT EXISTS retail_users (
                userid INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                user_pwd_hash TEXT NOT NULL,
                userrole TEXT NOT NULL CHECK (
                    userrole IN (
                        'admin',
                        'inventory_manager',
                        'employee'
                    )
                ),
                user_created_at TEXT NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)


    print("Retail inventory database initialized successfully.")

if __name__ == "__main__":
    create_retail_db()
