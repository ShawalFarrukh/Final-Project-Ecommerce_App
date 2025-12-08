from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from helpers import db_connection,login_required
from collections import Counter
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3  

# I have used Chatgpt to help me with my code but the essesence of the code is my own work.

app = Flask(__name__)

# Configure server-side sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # stores sessions on disk
Session(app)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/support")
def support():
    return render_template("support.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    password = request.form.get("password")
    confirmation = request.form.get("confirmation")

    if not username or not password or not confirmation:
        return "must provide username and password", 400
    if password != confirmation:
        return "passwords must match", 400

    conn = db_connection()
    try:
        cur = conn.execute(
            "INSERT INTO users (username, hash) VALUES (?, ?)",
            (username, generate_password_hash(password))
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError:
        return "username already exists", 400
    finally:
        if conn:
            try:
                conn.close()
            except Exception as e:
                print(f"Warning: could not close connection ({e})")

    session["user_id"] = user_id
    return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()

    if request.method == "GET":
        return render_template("login.html")

    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "must provide username and password", 400

    conn = db_connection()
    row = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()
    conn.close()

    if row is None or not check_password_hash(row["hash"], password):
        return "invalid username and/or password", 400

    session["user_id"] = row["id"]
    return redirect("/")



@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('login')


@app.route('/')
@login_required
def index():
    conn = db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('index.html',products=products)

@app.route('/cart')
@login_required
def cart():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        return render_template('cart.html', products=[], total=0)
    qty = Counter(cart_ids)

    # Get product ids from cart
    conn = db_connection()
    placeholders = ",".join("?" for _ in qty)
    rows = conn.execute(f"SELECT * FROM products WHERE id IN ({placeholders})",list(qty.keys())).fetchall()
    conn.close()
    # extract all info for html template
    products = []
    total = 0
    for r in rows:
        q = qty[r["id"]]
        subtotal = q * r["price"]
        total += subtotal
        products.append({
            "id" : r["id"],
            "name" : r["name"],
            "price" : r["price"],
            "quantity" : q,
            "subtotal" : subtotal,
            "image_url": r["image_url"]
        })

    return render_template('cart.html',products=products,total=total)

@app.route('/add_to_cart/<int:product_id>')
@login_required
def add_to_cart(product_id):
    # Checking if cart exists in session
    if 'cart' not in session:
        session['cart'] = []

    # Add product to cart
    session['cart'].append(product_id)

    return redirect(url_for('cart'))

# --- CHECKOUT ---
@app.route("/checkout", methods=["POST"])
@login_required
def checkout():
    """Create order, store items, clear cart (simple version)"""

    # 1. Get cart from session
    cart_ids = session.get("cart", [])
    if not cart_ids:
        return "cart is empty", 400

    # 2. Count quantity of each product id
    qty = Counter(cart_ids)  # e.g. {3: 2, 4: 1}

    # 3. Get product prices from database
    conn = db_connection()
    try:
        placeholders = ",".join("?" for _ in qty)
        rows = conn.execute(
            f"SELECT id, price FROM products WHERE id IN ({placeholders})",
            list(qty.keys())
        ).fetchall()

        # 4. Build a simple list of items + calculate total
        items = []   # will hold (product_id, quantity, price)
        total = 0

        for row in rows:
            product_id = row["id"]
            price = row["price"]

            # quantity comes from the Counter
            quantity = qty[product_id]

            items.append((product_id, quantity, price))
            total += price * quantity

        # 5. Insert into orders table
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (user_id, total) VALUES (?, ?)",
            (session["user_id"], total)
        )
        order_id = cur.lastrowid

        # 6. Insert each order_item one by one
        for product_id, quantity, price in items:
            cur.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )

        # 7. Save changes
        conn.commit()

    except Exception as e:
        conn.rollback()
        conn.close()
        return f"checkout failed: {e}", 500
    finally:
        conn.close()

    # 8. Clear cart in session
    session["cart"] = []

    # 9. Redirect to order detail page
    return redirect(f"/orders/{order_id}")

# --- ORDERS LIST ---
@app.route("/orders")
@login_required
def orders():
    conn = db_connection()
    rows = conn.execute(
        "SELECT id, total, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()
    conn.close()
    return render_template("orders.html", orders=rows)

# --- SINGLE ORDER DETAIL ---
@app.route("/orders/<int:order_id>")
@login_required
def order_detail(order_id):
    conn = db_connection()
    order = conn.execute(
        "SELECT id, total, created_at FROM orders WHERE id = ? AND user_id = ?",
        (order_id, session["user_id"])
    ).fetchone()
    if not order:
        conn.close()
        return "not found", 404

    items = conn.execute(
        """
        SELECT p.name, oi.quantity, oi.price
        FROM order_items oi
        JOIN products p ON p.id = oi.product_id
        WHERE oi.order_id = ?
        """,
        (order_id,)
    ).fetchall()
    conn.close()
    return render_template("order_detail.html", order=order, items=items)