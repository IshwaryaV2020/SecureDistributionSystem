import os
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect
from retail_access import retail_role_required
from flask import Flask, render_template, request, session, redirect, url_for
import sqlite3
from pathlib import Path
from retail_security import verify_user_pwd
from retail_products import view_products, add_product, retail_categories


app = Flask(__name__, static_folder="style")
app.config["SECRET_KEY"] = os.environ["RETAIL_SECRET_KEY"]
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=15)

retail_csrf = CSRFProtect(app)

@app.route("/")
@retail_role_required("admin", "inventory_manager", "employee")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("userid"):
        return redirect(url_for("home"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        user_pwd = request.form.get("user_pwd", "")

        db_path = Path(__file__).resolve().parent / "instance" / "retail.db"

        with sqlite3.connect(db_path) as retail_conn:
            retail_cursor = retail_conn.cursor()

            retail_cursor.execute("""
                SELECT userid, username, user_pwd_hash, userrole
                FROM retail_users
                WHERE username = ?
            """, (username,))

            user = retail_cursor.fetchone()

        if user and verify_user_pwd(user_pwd, user[2]):
            session.clear()
            session.permanent = True
            session["userid"] = user[0]
            session["username"] = user[1]
            session["userrole"] = user[3]

            return redirect(url_for("home"))

        return render_template(
            "login.html", error="Invalid username or password."
        ), 401

    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/securitymonitoring")
@retail_role_required("admin")
def security_monitoring():
    return "Security Monitoring (Admin Access Only)"


@app.route("/products")
@retail_role_required("admin", "inventory_manager", "employee")
def products():
    retail_items = view_products()
    return render_template("products.html", retail_items=retail_items)

@app.route("/products/add", methods=["GET", "POST"])
@retail_role_required("admin", "inventory_manager")
def product_add():

    if request.method == "POST":

        validation_error = add_product(
            request.form.get("p_name", ""),
            request.form.get("p_category", ""),
            request.form.get("p_price", ""),
            request.form.get("p_quantity", ""),
            request.form.get("p_desc", ""),
            request.form.get("p_sku", "")
        )

        if validation_error:
            return render_template(
                "add_product.html",
                error=validation_error,
                retail_categories=retail_categories
            ), 400

        return redirect(url_for("products"))

    return render_template(
        "add_product.html",
        retail_categories=retail_categories
    )

if __name__ == "__main__":
    app.run(debug=True)
