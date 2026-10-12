"""Grocery Store SaaS - Flask + SQLAlchemy.
Multi-tenant: every store has its own users/products/sales, isolated by store_id.
Run:  pip install -r requirements.txt && python app.py
"""
import os
import shutil
import secrets
import time
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from functools import wraps

from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin, login_user, logout_user,
                         login_required, current_user)
from flask_wtf.csrf import CSRFProtect
from jinja2 import DictLoader
from werkzeug.security import generate_password_hash, check_password_hash

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE = os.path.join(BASE_DIR, "instance")
os.makedirs(INSTANCE, exist_ok=True)


def load_secret():
    key = os.getenv("SECRET_KEY")
    if key:
        return key
    path = os.path.join(INSTANCE, "secret.key")
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(secrets.token_hex(32))
        os.chmod(path, 0o600)
    return open(path).read().strip()


app = Flask(__name__)
app.config.update(
    SECRET_KEY=load_secret(),
    SQLALCHEMY_DATABASE_URI=os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(INSTANCE, "grocery.db")),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("HTTPS", "0") == "1",  # set HTTPS=1 behind TLS
    PERMANENT_SESSION_LIFETIME=60 * 60 * 8,
    MAX_CONTENT_LENGTH=1 * 1024 * 1024,
)
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# ---------------------------------------------------------------- models
class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False, index=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="cashier")  # owner | cashier
    active = db.Column(db.Boolean, default=True)
    store = db.relationship("Store")

    @property
    def is_active(self):
        return self.active


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    barcode = db.Column(db.String(50))
    category = db.Column(db.String(60))
    unit = db.Column(db.String(20), default="pc")
    price_cents = db.Column(db.Integer, nullable=False, default=0)
    stock = db.Column(db.Integer, nullable=False, default=0)
    low_stock = db.Column(db.Integer, nullable=False, default=5)
    active = db.Column(db.Boolean, default=True)


class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    store_id = db.Column(db.Integer, db.ForeignKey("store.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    total_cents = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    items = db.relationship("SaleItem", backref="sale", cascade="all, delete-orphan")
    user = db.relationship("User")


class SaleItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sale_id = db.Column(db.Integer, db.ForeignKey("sale.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)  # snapshot
    price_cents = db.Column(db.Integer, nullable=False)
    qty = db.Column(db.Integer, nullable=False)


@login_manager.user_loader
def load_user(uid):
    return db.session.get(User, int(uid))


# ---------------------------------------------------------------- helpers
@app.template_filter("money")
def money(c):
    return "{:,.2f}".format((c or 0) / 100)


def to_cents(s):
    try:
        d = Decimal(s.strip())
    except (InvalidOperation, AttributeError):
        raise ValueError("Invalid price")
    if d < 0 or d > Decimal("10000000"):
        raise ValueError("Invalid price")
    return int((d * 100).quantize(Decimal("1")))


def to_int(s, lo=0, hi=10_000_000):
    try:
        n = int(s)
    except (TypeError, ValueError):
        raise ValueError("Invalid number")
    if not lo <= n <= hi:
        raise ValueError("Number out of range")
    return n


def owner_required(f):
    @wraps(f)
    @login_required
    def wrapper(*a, **kw):
        if current_user.role != "owner":
            abort(403)
        return f(*a, **kw)
    return wrapper


def store_product_or_404(pid):
    p = Product.query.filter_by(id=pid, store_id=current_user.store_id, active=True).first()
    if not p:
        abort(404)
    return p


# simple login throttle (per IP+username); use Redis/Flask-Limiter when scaling out
FAILS = {}
MAX_FAILS, LOCK_SECS = 5, 300


def throttled(key):
    n, t = FAILS.get(key, (0, 0))
    if n >= MAX_FAILS and time.time() - t < LOCK_SECS:
        return True
    if time.time() - t >= LOCK_SECS:
        FAILS.pop(key, None)
    return False


@app.after_request
def security_headers(resp):
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "DENY"
    resp.headers["Referrer-Policy"] = "same-origin"
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline'")
    if request.endpoint != "static":
        resp.headers["Cache-Control"] = "no-store"
    return resp


# ---------------------------------------------------------------- auth
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        store_name = request.form.get("store_name", "").strip()
        username = request.form.get("username", "").strip().lower()
        pw = request.form.get("password", "")
        if not store_name or len(username) < 3:
            flash("Store name and a username (3+ chars) are required.", "err")
        elif len(pw) < 10:
            flash("Password must be at least 10 characters.", "err")
        elif User.query.filter_by(username=username).first():
            flash("Username already taken.", "err")
        else:
            store = Store(name=store_name)
            db.session.add(store)
            db.session.flush()
            db.session.add(User(store_id=store.id, username=username, role="owner",
                                password_hash=generate_password_hash(pw)))
            db.session.commit()
            flash("Store created. Please log in.", "ok")
            return redirect(url_for("login"))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        key = f"{request.remote_addr}|{username}"
        if throttled(key):
            flash("Too many attempts. Try again in a few minutes.", "err")
            return render_template("login.html"), 429
        user = User.query.filter_by(username=username).first()
        if user and user.active and check_password_hash(user.password_hash, request.form.get("password", "")):
            FAILS.pop(key, None)
            login_user(user)
            return redirect(url_for("dashboard"))
        n, _ = FAILS.get(key, (0, 0))
        FAILS[key] = (n + 1, time.time())
        flash("Invalid username or password.", "err")
    return render_template("login.html")


@app.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# ---------------------------------------------------------------- dashboard
@app.route("/")
@login_required
def dashboard():
    sid = current_user.store_id
    start = datetime.combine(date.today(), datetime.min.time())
    today = Sale.query.filter(Sale.store_id == sid, Sale.created >= start).all()
    low = (Product.query.filter(Product.store_id == sid, Product.active.is_(True),
                                Product.stock <= Product.low_stock)
           .order_by(Product.stock).limit(20).all())
    return render_template("dashboard.html", count=len(today),
                           total=sum(s.total_cents for s in today), low=low)


# ---------------------------------------------------------------- products
def save_product(p):
    p.name = request.form.get("name", "").strip()
    if not p.name:
        raise ValueError("Name is required")
    p.barcode = request.form.get("barcode", "").strip()[:50] or None
    p.category = request.form.get("category", "").strip()[:60] or None
    p.unit = request.form.get("unit", "pc").strip()[:20] or "pc"
    p.price_cents = to_cents(request.form.get("price", ""))
    p.stock = to_int(request.form.get("stock"))
    p.low_stock = to_int(request.form.get("low_stock", "5"))


@app.route("/products")
@login_required
def products():
    q = request.args.get("q", "").strip()
    query = Product.query.filter_by(store_id=current_user.store_id, active=True)
    if q:
        like = f"%{q}%"
        query = query.filter(db.or_(Product.name.ilike(like), Product.barcode.ilike(like),
                                    Product.category.ilike(like)))
    return render_template("products.html", items=query.order_by(Product.name).all(), q=q)


@app.route("/products/new", methods=["GET", "POST"])
@owner_required
def product_new():
    if request.method == "POST":
        p = Product(store_id=current_user.store_id)
        try:
            save_product(p)
            db.session.add(p)
            db.session.commit()
            flash("Product added.", "ok")
            return redirect(url_for("products"))
        except ValueError as e:
            flash(str(e), "err")
    return render_template("product_form.html", p=None)


@app.route("/products/<int:pid>/edit", methods=["GET", "POST"])
@owner_required
def product_edit(pid):
    p = store_product_or_404(pid)
    if request.method == "POST":
        try:
            save_product(p)
            db.session.commit()
            flash("Product updated.", "ok")
            return redirect(url_for("products"))
        except ValueError as e:
            db.session.rollback()
            flash(str(e), "err")
    return render_template("product_form.html", p=p)


@app.route("/products/<int:pid>/delete", methods=["POST"])
@owner_required
def product_delete(pid):
    p = store_product_or_404(pid)
    p.active = False  # soft delete keeps sales history intact
    db.session.commit()
    flash("Product removed.", "ok")
    return redirect(url_for("products"))


# ---------------------------------------------------------------- POS / sales
@app.route("/pos", methods=["GET", "POST"])
@login_required
def pos():
    items = (Product.query.filter_by(store_id=current_user.store_id, active=True)
             .order_by(Product.name).all())
    if request.method == "POST":
        lines, total = [], 0
        try:
            for p in items:
                raw = request.form.get(f"qty_{p.id}", "").strip()
                if not raw or raw == "0":
                    continue
                qty = to_int(raw, 1, 100000)
                if qty > p.stock:
                    raise ValueError(f"Not enough stock for {p.name} (have {p.stock})")
                lines.append((p, qty))
                total += p.price_cents * qty
            if not lines:
                raise ValueError("Enter a quantity for at least one product")
        except ValueError as e:
            flash(str(e), "err")
            return render_template("pos.html", items=items)
        sale = Sale(store_id=current_user.store_id, user_id=current_user.id, total_cents=total)
        for p, qty in lines:
            p.stock -= qty
            sale.items.append(SaleItem(name=p.name, price_cents=p.price_cents, qty=qty))
        db.session.add(sale)
        db.session.commit()
        flash(f"Sale #{sale.id} saved. Total: {money(total)}", "ok")
        return redirect(url_for("pos"))
    return render_template("pos.html", items=items)


@app.route("/sales")
@login_required
def sales():
    rows = (Sale.query.filter_by(store_id=current_user.store_id)
            .order_by(Sale.created.desc()).limit(200).all())
    return render_template("sales.html", rows=rows)


# ---------------------------------------------------------------- users
@app.route("/users", methods=["GET", "POST"])
@owner_required
def users():
    if request.method == "POST":
        username = request.form.get("username", "").strip().lower()
        pw = request.form.get("password", "")
        role = request.form.get("role", "cashier")
        if role not in ("owner", "cashier"):
            role = "cashier"
        if len(username) < 3 or len(pw) < 10:
            flash("Username 3+ chars and password 10+ chars required.", "err")
        elif User.query.filter_by(username=username).first():
            flash("Username already taken.", "err")
        else:
            db.session.add(User(store_id=current_user.store_id, username=username,
                                role=role, password_hash=generate_password_hash(pw)))
            db.session.commit()
            flash("User added.", "ok")
    rows = User.query.filter_by(store_id=current_user.store_id).order_by(User.username).all()
    return render_template("users.html", rows=rows)


@app.route("/users/<int:uid>/toggle", methods=["POST"])
@owner_required
def user_toggle(uid):
    u = User.query.filter_by(id=uid, store_id=current_user.store_id).first_or_404()
    if u.id == current_user.id:
        flash("You can't disable yourself.", "err")
    else:
        u.active = not u.active
        db.session.commit()
    return redirect(url_for("users"))


@app.route("/users/<int:uid>/password", methods=["POST"])
@owner_required
def user_password(uid):
    u = User.query.filter_by(id=uid, store_id=current_user.store_id).first_or_404()
    pw = request.form.get("password", "")
    if len(pw) < 10:
        flash("Password must be at least 10 characters.", "err")
    else:
        u.password_hash = generate_password_hash(pw)
        db.session.commit()
        flash("Password changed.", "ok")
    return redirect(url_for("users"))


# ---------------------------------------------------------------- CLI
@app.cli.command("backup")
def backup():
    """flask --app app backup  -> copies the SQLite file with a timestamp."""
    src = os.path.join(INSTANCE, "grocery.db")
    dst = os.path.join(INSTANCE, f"backup-{datetime.now():%Y%m%d-%H%M%S}.db")
    shutil.copy2(src, dst)
    print("Saved", dst)


# ---------------------------------------------------------------- templates
BASE = """<!doctype html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{{ title or 'Grocery SaaS' }}</title>
<style>
body{font-family:system-ui,sans-serif;margin:0;background:#f4f6f8;color:#222}
nav{background:#14532d;color:#fff;padding:10px 20px;display:flex;gap:16px;align-items:center;flex-wrap:wrap}
nav a,nav button{color:#fff;text-decoration:none;background:none;border:0;font:inherit;cursor:pointer}
nav .sp{flex:1}
main{max-width:980px;margin:20px auto;padding:0 16px}
.card{background:#fff;border-radius:8px;padding:16px;margin-bottom:16px;box-shadow:0 1px 3px #0002}
table{width:100%;border-collapse:collapse}th,td{padding:8px;border-bottom:1px solid #eee;text-align:left}
input,select{padding:8px;border:1px solid #ccc;border-radius:6px;width:100%;box-sizing:border-box;margin:4px 0 10px}
td input{margin:0;width:80px}
.btn{background:#16a34a;color:#fff;border:0;padding:8px 14px;border-radius:6px;cursor:pointer;text-decoration:none;display:inline-block;font:inherit}
.btn.red{background:#dc2626}.btn.gray{background:#6b7280}
.msg{padding:10px;border-radius:6px;margin-bottom:10px}.ok{background:#dcfce7}.err{background:#fee2e2}
.stats{display:flex;gap:16px;flex-wrap:wrap}.stats .card{flex:1;min-width:180px}
.big{font-size:28px;font-weight:700}form.inline{display:inline}
</style></head><body>
<nav><b>🛒 {{ current_user.store.name if current_user.is_authenticated else 'Grocery SaaS' }}</b>
{% if current_user.is_authenticated %}
<a href="{{ url_for('dashboard') }}">Dashboard</a><a href="{{ url_for('pos') }}">New Sale</a>
<a href="{{ url_for('products') }}">Products</a><a href="{{ url_for('sales') }}">Sales</a>
{% if current_user.role == 'owner' %}<a href="{{ url_for('users') }}">Users</a>{% endif %}
<span class="sp"></span><span>{{ current_user.username }}</span>
<form class="inline" method="post" action="{{ url_for('logout') }}">
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><button>Logout</button></form>
{% endif %}</nav><main>
{% for cat, m in get_flashed_messages(with_categories=true) %}<div class="msg {{ cat }}">{{ m }}</div>{% endfor %}
{% block content %}{% endblock %}</main></body></html>"""

LOGIN = """{% extends 'base' %}{% block content %}<div class="card" style="max-width:380px;margin:40px auto">
<h2>Login</h2><form method="post"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
Username<input name="username" required autofocus>Password<input type="password" name="password" required>
<button class="btn">Login</button> <a href="{{ url_for('register') }}">Create a store</a></form></div>{% endblock %}"""

REGISTER = """{% extends 'base' %}{% block content %}<div class="card" style="max-width:380px;margin:40px auto">
<h2>Create your store</h2><form method="post"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
Store name<input name="store_name" required>Owner username<input name="username" required>
Password (10+ chars)<input type="password" name="password" required minlength="10">
<button class="btn">Create</button> <a href="{{ url_for('login') }}">Login</a></form></div>{% endblock %}"""

DASHBOARD = """{% extends 'base' %}{% block content %}
<div class="stats"><div class="card"><div>Today's sales</div><div class="big">{{ total|money }}</div></div>
<div class="card"><div>Transactions today</div><div class="big">{{ count }}</div></div></div>
<div class="card"><h3>Low stock</h3>{% if low %}<table><tr><th>Product</th><th>Stock</th></tr>
{% for p in low %}<tr><td>{{ p.name }}</td><td>{{ p.stock }} {{ p.unit }}</td></tr>{% endfor %}</table>
{% else %}All good.{% endif %}</div>{% endblock %}"""

PRODUCTS = """{% extends 'base' %}{% block content %}<div class="card">
<form method="get" style="display:flex;gap:8px"><input name="q" value="{{ q }}" placeholder="Search name / barcode / category">
<button class="btn" style="margin:4px 0 10px">Search</button>
{% if current_user.role == 'owner' %}<a class="btn" style="margin:4px 0 10px" href="{{ url_for('product_new') }}">+ Add</a>{% endif %}</form>
<table><tr><th>Name</th><th>Category</th><th>Barcode</th><th>Price</th><th>Stock</th><th></th></tr>
{% for p in items %}<tr><td>{{ p.name }}</td><td>{{ p.category or '' }}</td><td>{{ p.barcode or '' }}</td>
<td>{{ p.price_cents|money }}</td><td>{{ p.stock }} {{ p.unit }}</td><td>
{% if current_user.role == 'owner' %}<a class="btn gray" href="{{ url_for('product_edit', pid=p.id) }}">Edit</a>
<form class="inline" method="post" action="{{ url_for('product_delete', pid=p.id) }}" onsubmit="return confirm('Remove?')">
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"><button class="btn red">Delete</button></form>{% endif %}
</td></tr>{% endfor %}</table></div>{% endblock %}"""

PRODUCT_FORM = """{% extends 'base' %}{% block content %}<div class="card" style="max-width:480px">
<h2>{{ 'Edit' if p else 'New' }} product</h2><form method="post"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
Name<input name="name" required value="{{ p.name if p else '' }}">
Barcode<input name="barcode" value="{{ p.barcode or '' if p else '' }}">
Category<input name="category" value="{{ p.category or '' if p else '' }}">
Unit (pc, kg, ltr)<input name="unit" value="{{ p.unit if p else 'pc' }}">
Price<input name="price" required value="{{ '%.2f' % (p.price_cents/100) if p else '' }}">
Stock<input name="stock" type="number" min="0" required value="{{ p.stock if p else 0 }}">
Low-stock alert at<input name="low_stock" type="number" min="0" value="{{ p.low_stock if p else 5 }}">
<button class="btn">Save</button> <a class="btn gray" href="{{ url_for('products') }}">Cancel</a></form></div>{% endblock %}"""

POS = """{% extends 'base' %}{% block content %}<div class="card"><h3>New sale</h3>
<input id="f" placeholder="Filter products..." oninput="flt()">
<form method="post"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
<table id="t"><tr><th>Product</th><th>Price</th><th>Stock</th><th>Qty</th></tr>
{% for p in items %}<tr data-n="{{ (p.name ~ ' ' ~ (p.barcode or ''))|lower }}"><td>{{ p.name }}</td>
<td>{{ p.price_cents|money }}</td><td>{{ p.stock }}</td>
<td><input type="number" min="0" max="{{ p.stock }}" name="qty_{{ p.id }}"></td></tr>{% endfor %}</table>
<br><button class="btn">Complete sale</button></form></div>
<script>function flt(){var v=document.getElementById('f').value.toLowerCase();
document.querySelectorAll('#t tr[data-n]').forEach(function(r){r.style.display=r.dataset.n.includes(v)?'':'none'})}</script>
{% endblock %}"""

SALES = """{% extends 'base' %}{% block content %}<div class="card"><h3>Recent sales</h3>
<table><tr><th>#</th><th>Date (UTC)</th><th>Cashier</th><th>Items</th><th>Total</th></tr>
{% for s in rows %}<tr><td>{{ s.id }}</td><td>{{ s.created.strftime('%Y-%m-%d %H:%M') }}</td>
<td>{{ s.user.username if s.user else '' }}</td>
<td>{% for i in s.items %}{{ i.qty }}× {{ i.name }}{% if not loop.last %}, {% endif %}{% endfor %}</td>
<td>{{ s.total_cents|money }}</td></tr>{% endfor %}</table></div>{% endblock %}"""

USERS = """{% extends 'base' %}{% block content %}<div class="card"><h3>Staff</h3>
<table><tr><th>User</th><th>Role</th><th>Status</th><th>Actions</th></tr>
{% for u in rows %}<tr><td>{{ u.username }}</td><td>{{ u.role }}</td><td>{{ 'active' if u.active else 'disabled' }}</td><td>
<form class="inline" method="post" action="{{ url_for('user_toggle', uid=u.id) }}"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
<button class="btn gray">{{ 'Disable' if u.active else 'Enable' }}</button></form>
<form class="inline" method="post" action="{{ url_for('user_password', uid=u.id) }}"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
<input type="password" name="password" placeholder="new password" minlength="10" required><button class="btn">Set</button></form>
</td></tr>{% endfor %}</table></div>
<div class="card" style="max-width:420px"><h3>Add user</h3><form method="post"><input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
Username<input name="username" required>Password (10+ chars)<input type="password" name="password" minlength="10" required>
Role<select name="role"><option value="cashier">Cashier</option><option value="owner">Owner</option></select>
<button class="btn">Add</button></form></div>{% endblock %}"""

app.jinja_loader = DictLoader({
    "base": BASE, "login.html": LOGIN, "register.html": REGISTER,
    "dashboard.html": DASHBOARD, "products.html": PRODUCTS,
    "product_form.html": PRODUCT_FORM, "pos.html": POS,
    "sales.html": SALES, "users.html": USERS,
})

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
