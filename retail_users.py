
import sqlite3
from pathlib import Path
from getpass import getpass
from retail_security import hash_user_pwd


def create_retail_user():
    db_path = Path(__file__).resolve().parent / "instance" / "retail.db"

    username = input("Enter username: ").strip()
    userrole = input("Enter user role: ").strip().lower()

    if not username or len(username) > 50:
        print("Invalid username.")
        return

    if userrole not in ("admin", "inventory_manager", "employee"):
        print("Invalid role.")
        return

    user_pwd = getpass("Enter password: ")

    if len(user_pwd) < 15 or len(user_pwd) > 128:
        print("Password must contain 15 to 128 characters.")
        return

    if user_pwd != getpass("Confirm password: "):
        print("Passwords does not match.")
        return

    user_pwd_hash = hash_user_pwd(user_pwd)

    try:
        with sqlite3.connect(db_path) as retail_conn:
            retail_cursor = retail_conn.cursor()

            retail_cursor.execute("""
                INSERT INTO retail_users
                (username, user_pwd_hash, userrole)
                VALUES (?, ?, ?)
            """, (username, user_pwd_hash, userrole))

        print("User account successfully created.")

    except sqlite3.IntegrityError:
        print("Failed. Account could not be created. check username and role.")


if __name__ == "__main__":
    create_retail_user()
