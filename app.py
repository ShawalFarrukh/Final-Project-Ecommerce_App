from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
from helpers import db_connection



app = Flask(__name__)

# Configure server-side sessions
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # stores sessions on disk
Session(app)



@app.route('/')
def index():
    conn = db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template('index.html',products=products)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    # Checking if cart exists in session
    if 'cart' not in session:
        session['cart'] = []

    # Add product to cart
    session['cart'].append(product_id)

    return redirect(url_for('cart'))