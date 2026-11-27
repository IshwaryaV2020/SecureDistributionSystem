import sqlite3
from pathlib import Path
from decimal import Decimal, InvalidOperation

retail_categories = (
    "Clothing",
    "Bags & accessories",
    "Electronics & accessories"
)

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

def validate_product(p_name, p_category, p_price,
                     p_quantity, p_desc, p_sku):

    if not p_name.strip() or len(p_name) > 100:
        return "Enter a valid product name."

    if p_category not in retail_categories:
        return "Invalid product category."

    try:
        price_euro = Decimal(p_price)

        if not price_euro.is_finite():
            return "Invalid product price"

        if price_euro < 0:
            return "Product price cannot be negative"

        if price_euro.as_tuple().exponent < -2:
            return "Price must have a maximum of two decimal places"

        if price_euro > Decimal("999999.99"):
            return "Product price exceeds the allowed limit"

    except InvalidOperation:
        return "Enter a valid product price"

    try:
        if int(p_quantity) < 0 or int(p_quantity) > 1000000:
            return "Invalid product quantity."

    except ValueError:
        return "Quantity must be a whole number."

    if len(p_desc) > 500:
        return "Product description is too long."

    if not p_sku.strip() or len(p_sku) > 30:
        return "Enter a valid SKU."

    return None

def add_product(p_name, p_category, p_price,
                p_quantity, p_desc, p_sku):

    validation_error = validate_product(
        p_name, p_category, p_price,
        p_quantity, p_desc, p_sku
    )

    if validation_error:
        return validation_error

    price_euro = Decimal(p_price)

    db_path = Path(__file__).resolve().parent / "instance" / "retail.db"

    try:
        with sqlite3.connect(db_path) as retail_conn:
            retail_cursor = retail_conn.cursor()

            retail_cursor.execute("""
                INSERT INTO retail_inventory
                (p_name, p_category, p_price,
                 p_quantity, p_desc, p_sku)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                p_name.strip(),
                p_category,
                int(price_euro * 100),
                int(p_quantity),
                p_desc.strip(),
                p_sku.strip()
            ))

        return None

    except sqlite3.IntegrityError:
        return "Product could not be added. Check SKU and product details."

        