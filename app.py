import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ==========================================
# 1. PAGE CONFIGURATION & GEOMETRIC UI
# ==========================================
st.set_page_config(
    page_title="Muzaffar Developers | Grocery SaaS ERP",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Poly-Vibrant SaaS CSS Styling
SAAS_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, rgba(255,182,193,0.3) 0%, rgba(135,206,250,0.3) 50%, rgba(152,251,152,0.3) 100%),
                    url('https://images.unsplash.com/photo-1542838132-92c53300491e?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-attachment: fixed;
        background-blend-mode: overlay;
        color: #1e293b;
    }
    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 800 !important;
    }
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.85) !important;
        backdrop-filter: blur(12px);
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
    }
    div[data-testid="stMetricValue"] {
        color: #0284c7 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }
    .stButton > button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #10b981 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
    }
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 8px;
    }
</style>
"""
st.markdown(SAAS_CSS, unsafe_allow_html=True)

# ==========================================
# 2. DATABASE ENGINE & INITIALIZATION
# ==========================================
DB_FILE = "grocery_saas.db"

def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_grocery_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')
    
    # 2. Grocery Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_code TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            stock_qty INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            expiry_date TEXT
        )
    ''')
    
    # 3. POS Sales Transactions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            invoice_no TEXT PRIMARY KEY,
            sale_date TEXT NOT NULL,
            cashier TEXT NOT NULL,
            customer_name TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_mode TEXT NOT NULL
        )
    ''')
    
    # 4. Customers Credit/Debit Ledger
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            credit_balance REAL NOT NULL
        )
    ''')
    
    # Seed Default Users if empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', [
            ("admin", "muzaffar123", "Admin", "Muzaffar (Owner)"),
            ("cashier1", "cashier123", "Cashier", "Store Cashier")
        ])
        
    # Seed Default Grocery Items if empty
    cursor.execute('SELECT COUNT(*) FROM inventory')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?)', [
            ("GRO-101", "Basmati Rice (5kg)", "Grains", 45, 12.50, "2027-12-31"),
            ("GRO-102", "Cooking Oil (1L)", "Pantry", 80, 4.20, "2026-10-15"),
            ("GRO-103", "Whole Wheat Flour (10kg)", "Grains", 30, 9.80, "2027-06-30"),
            ("GRO-104", "Sugar White (1kg)", "Pantry", 120, 1.50, "2028-01-01"),
            ("GRO-105", "Fresh Whole Milk (1L)", "Dairy", 15, 1.20, "2026-10-14")
        ])
        
    # Seed Default Customers if empty
    cursor.execute('SELECT COUNT(*) FROM customers')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', [
            ("CUST-001", "Ali Khan", "+92 300 1234567", 0.0),
            ("CUST-002", "Ahmed Raza", "+92 321 7654321", 25.50)
        ])
        
    conn.commit()
    conn.close()

init_grocery_db()

# ==========================================
# 3. SECURE USER AUTHENTICATION
# ==========================================
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.user:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h2 style='text-align: center;'>🛒 Grocery SaaS Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569;'>Sign in to access your store terminal.</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username_input = st.text_input("Username")
            password_input = st.text_input("Password", type="password")
            login_submit = st.form_submit_button("Sign In to POS")
            
            if login_submit:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT role, full_name FROM users WHERE username = ? AND password = ?', (username_input, password_input))
                user_record = cursor.fetchone()
                conn.close()
                
                if user_record:
                    st.session_state.user = user_record[1]
                    st.session_state.role = user_record[0]
                    st.success(f"Welcome back, {user_record[1]}!")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password! (Hint: admin / muzaffar123)")
        st.stop()

# ==========================================
# 4. SIDEBAR NAVIGATION & USER INFO
# ==========================================
st.sidebar.markdown(f"<h3 style='color: #0f172a;'>👤 {st.session_state.user}</h3>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color: #0284c7; font-weight: bold;'>Role: {st.session_state.role}</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu_options = ["📊 Dashboard", "🛒 POS Billing Terminal", "📦 Inventory Manager", "👥 Customer Accounts", "📥 Sales Reports"]
if st.session_state.role == "Admin":
    menu_options.append("⚙️ Database Editor & Users")

nav = st.sidebar.radio("NAVIGATION", menu_options)

if st.sidebar.button("🔒 Logout"):
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# ==========================================
# 5. MODULE 1: DASHBOARD
# ==========================================
if nav == "📊 Dashboard":
    st.title("🛒 Grocery Store Overview")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    df_cust = pd.read_sql('SELECT * FROM customers', conn)
    conn.close()

    total_products = len(df_inv)
    low_stock = len(df_inv[df_inv["stock_qty"] <= 15])
    total_revenue = df_sales["total_amount"].sum() if not df_sales.empty else 0.0
    total_customers = len(df_cust)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active SKUs", total_products)
    c2.metric("Low Stock Items ⚠️", low_stock, delta_color="inverse")
    c3.metric("Total Store Revenue", f"${total_revenue:,.2f}")
    c4.metric("Registered Customers", total_customers)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📦 Inventory Stock Overview")
        if not df_inv.empty:
            st.dataframe(df_inv[["item_code", "item_name", "stock_qty", "unit_price"]], use_container_width=True)
    with col_b:
        st.subheader("💰 Recent Transactions")
        if not df_sales.empty:
            st.dataframe(df_sales.head(5), use_container_width=True)

# ==========================================
# 6. MODULE 2: POS BILLING TERMINAL
# ==========================================
elif nav == "🛒 POS Billing Terminal":
    st.title("🛒 Point of Sale (POS) Terminal")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_cust = pd.read_sql('SELECT * FROM customers', conn)
    conn.close()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Select Products to Bill")
        selected_item = st.selectbox("Search & Choose Grocery Item", df_inv['item_name'].tolist())
        item_row = df_inv[df_inv['item_name'] == selected_item].iloc[0]
        
        st.info(f"**Code:** {item_row['item_code']} | **Price:** ${item_row['unit_price']} | **Available Stock:** {item_row['stock_qty']} units")
        
        qty = st.number_input("Quantity", min_value=1, max_value=int(item_row['stock_qty']) if item_row['stock_qty'] > 0 else 1, value=1)
        
        if "cart" not in st.session_state:
            st.session_state.cart = []

        if st.button("➕ Add to Cart"):
            st.session_state.cart.append({
                "item_code": item_row['item_code'],
                "item_name": selected_item,
                "price": item_row['unit_price'],
                "qty": qty,
                "subtotal": item_row['unit_price'] * qty
            })
            st.success(f"Added {qty}x {selected_item} to cart!")

    with col2:
        st.subheader("🧾 Current Bill Cart")
        if st.session_state.cart:
            cart_df = pd.DataFrame(st.session_state.cart)
            st.dataframe(cart_df[["item_name", "qty", "subtotal"]], use_container_width=True)
            
            grand_total = cart_df["subtotal"].sum()
            st.markdown(f"### **Grand Total: ${grand_total:,.2f}**")
            
            customer_name = st.selectbox("Customer Account", df_cust['name'].tolist())
            payment_mode = st.radio("Payment Method", ["Cash", "Credit Card", "Store Credit"])

            if st.button("💳 Complete Checkout & Print"):
                invoice_no = f"INV-{int(date.today().strftime('%Y%m%d'))}-{len(df_sales)+1 if 'df_sales' in locals() else 1001}"
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    # Save Sale Transaction
                    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)', 
                                   (invoice_no, str(date.today()), st.session_state.user, customer_name, grand_total, payment_mode))
                    
                    # Deduct Stock Quantities
                    for item in st.session_state.cart:
                        cursor.execute('UPDATE inventory SET stock_qty = stock_qty - ? WHERE item_code = ?', 
                                       (item['qty'], item['item_code']))
                        
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Checkout Successful! Invoice `{invoice_no}` generated.")
                    st.session_state.cart = []
                except Exception as e:
                    st.error(f"Checkout Error: {e}")
            
            if st.button("🗑️ Clear Cart"):
                st.session_state.cart = []
                st.rerun()
        else:
            st.write("Cart is empty.")

# ==========================================
# 7. MODULE 3: INVENTORY MANAGER
# ==========================================
elif nav == "📦 Inventory Manager":
    st.title("📦 Grocery Inventory Control")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.subheader("Current Stock Catalog")
    st.dataframe(df_inv, use_container_width=True)

    st.subheader("➕ Add New Grocery Item")
    with st.form("add_grocery_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        code = c1.text_input("Item Code", f"GRO-10{len(df_inv)+1}")
        name = c2.text_input("Item Name")
        category = c1.selectbox("Category", ["Grains", "Pantry", "Dairy", "Beverages", "Snacks", "Household"])
        qty = c2.number_input("Stock Quantity", min_value=1, value=50)
        price = c1.number_input("Unit Price ($)", min_value=0.1, value=5.00, step=0.5)
        expiry = c2.date_input("Expiry Date")

        if st.form_submit_button("Save Item to Inventory"):
            if name:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?)', 
                                   (code, name, category, qty, price, str(expiry)))
                    conn.commit()
                    conn.close()
                    st.success(f"Item '{name}' added successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Item code '{code}' already exists.")
            else:
                st.error("Please provide an item name.")

# ==========================================
# 8. MODULE 4: CUSTOMER ACCOUNTS
# ==========================================
elif nav == "👥 Customer Accounts":
    st.title("👥 Customer Ledgers & Accounts")
    st.markdown("---")

    conn = get_db_connection()
    df_cust = pd.read_sql('SELECT * FROM customers', conn)
    conn.close()

    st.subheader("Registered Store Customers")
    st.dataframe(df_cust, use_container_width=True)

    st.subheader("➕ Register New Customer")
    with st.form("add_customer_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        cid = c1.text_input("Customer ID", f"CUST-00{len(df_cust)+1}")
        name = c2.text_input("Full Name")
        phone = c1.text_input("Phone Number")
        credit = c2.number_input("Initial Credit Balance ($)", value=0.0)

        if st.form_submit_button("Save Customer"):
            if name:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?)', (cid, name, phone, credit))
                    conn.commit()
                    conn.close()
                    st.success(f"Customer '{name}' registered successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Customer ID already exists.")
            else:
                st.error("Please enter a customer name.")

# ==========================================
# 9. MODULE 5: SALES REPORTS & EXPORT
# ==========================================
elif nav == "📥 Sales Reports":
    st.title("📥 Sales & Audit Reports")
    st.markdown("---")

    conn = get_db_connection()
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Export Sales Ledger")
        st.download_button("📄 Download Sales CSV", df_sales.to_csv(index=False).encode('utf-8'), "grocery_sales_report.csv", "text/csv")
    with c2:
        st.subheader("Export Inventory Catalog")
        st.download_button("📄 Download Inventory CSV", df_inv.to_csv(index=False).encode('utf-8'), "grocery_inventory_report.csv", "text/csv")

# ==========================================
# 10. MODULE 6: ADMIN DATABASE & USERS EDITOR
# ==========================================
elif nav == "⚙️ Database Editor & Users" and st.session_state.role == "Admin":
    st.title("⚙️ Secure Database & User Management")
    st.caption("Admin control panel for live table editing and user credentials.")
    st.markdown("---")

    table_choice = st.selectbox("Select Database Table to Edit", ["inventory", "customers", "users", "sales"])

    conn = get_db_connection()
    df_current = pd.read_sql(f"SELECT * FROM {table_choice}", conn)
    conn.close()

    st.info("💡 **Editable Grid:** Double click any cell below to update records or delete rows directly, then click **Save Database Changes**.")
    
    edited_df = st.data_editor(df_current, use_container_width=True, num_rows="dynamic")

    if st.button("💾 Save Database Changes"):
        try:
            conn = get_db_connection()
            edited_df.to_sql(table_choice, conn, if_exists='replace', index=False)
            conn.close()
            st.success(f"Table `{table_choice}` successfully updated in SQLite!")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating database: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #334155; font-weight: 600; font-size: 13px;'>© 2026 Muzaffar Developers | Grocery Store SaaS & POS System</p>", unsafe_allow_html=True)
