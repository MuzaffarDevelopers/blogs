import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ==========================================
# 1. PAGE CONFIGURATION & MATURE ANIMATED UI
# ==========================================
st.set_page_config(
    page_title="Muzaffar Developers | Enterprise Grocery SaaS",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mature SaaS CSS with subtle hover/fade transition animations
MATURE_SAAS_CSS = """
<style>
    /* Professional Slate Background & Typography */
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    h1, h2, h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }
    
    /* Smooth Animated Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0;
        transition: all 0.3s ease-in-out;
    }
    
    /* Mature Card Containers with Subtle Hover Lift Animation */
    div[data-testid="stMetric"], div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }
    
    div[data-testid="stMetricValue"] {
        color: #2563eb !important;
        font-weight: 700 !important;
    }
    
    /* Professional Action Buttons with Fade Animation */
    .stButton > button, div[data-testid="stForm"] button {
        background-color: #2563eb !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: background-color 0.2s ease, transform 0.1s ease !important;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
        transform: scale(1.01);
    }
    
    /* Clean Dataframes */
    div[data-testid="stDataFrame"] {
        background: #ffffff;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        padding: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
</style>
"""
st.markdown(MATURE_SAAS_CSS, unsafe_allow_html=True)

# ==========================================
# 2. SECURE DATABASE ENGINE & SEEDING
# ==========================================
DB_FILE = "grocery_mature_saas.db"

def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
    ''')
    
    # Inventory Table
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
    
    # Sales Table
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
    
    # Customers Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            credit_balance REAL NOT NULL
        )
    ''')
    
    # Seed Admin User if empty
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO users VALUES (?, ?, ?, ?)', [
            ("admin", "muzaffar123", "Admin", "Muzaffar (Administrator)"),
            ("cashier", "cashier123", "Cashier", "Store Cashier")
        ])
        
    # Seed Inventory if empty
    cursor.execute('SELECT COUNT(*) FROM inventory')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?)', [
            ("G-101", "Basmati Rice (5kg)", "Grains", 50, 14.00, "2027-12-31"),
            ("G-102", "Cooking Canola Oil (1L)", "Pantry", 75, 4.50, "2026-11-15"),
            ("G-103", "Whole Wheat Flour (10kg)", "Grains", 40, 10.50, "2027-06-30"),
            ("G-104", "Refined White Sugar (1kg)", "Pantry", 100, 1.60, "2028-01-01"),
            ("G-105", "Pasteurized Milk (1L)", "Dairy", 20, 1.30, "2026-10-15")
        ])
        
    # Seed Customers if empty
    cursor.execute('SELECT COUNT(*) FROM customers')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?)', [
            ("C-001", "General Walk-in Customer", "N/A", 0.0),
            ("C-002", "Tariq Mahmood", "+92 300 9876543", 15.00)
        ])
        
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. AUTHENTICATION GATEWAY
# ==========================================
if "user" not in st.session_state:
    st.session_state.user = None
if "role" not in st.session_state:
    st.session_state.role = None

if not st.session_state.user:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h2 style='text-align: center;'>🏪 Enterprise SaaS Portal</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #64748b;'>Enter credentials to access secure terminal.</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            u_input = st.text_input("Username")
            p_input = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Sign In")
            
            if login_btn:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT role, full_name FROM users WHERE username = ? AND password = ?', (u_input, p_input))
                record = cursor.fetchone()
                conn.close()
                
                if record:
                    st.session_state.user = record[1]
                    st.session_state.role = record[0]
                    st.success(f"Authenticated as {record[1]}")
                    st.rerun()
                else:
                    st.error("Invalid login credentials. (Default: admin / muzaffar123)")
        st.stop()

# ==========================================
# 4. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown(f"<h3 style='color: #1e293b; font-size: 1.1rem;'>👤 {st.session_state.user}</h3>", unsafe_allow_html=True)
st.sidebar.markdown(f"<p style='color: #2563eb; font-weight: 600; font-size: 0.85rem;'>Access Level: {st.session_state.role}</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

nav_items = ["📊 Overview Dashboard", "🛒 POS Checkout", "📦 Inventory Stock", "👥 Customers", "📥 Sales Reports"]
if st.session_state.role == "Admin":
    nav_items.append("⚙️ Secure Database Editor")

choice = st.sidebar.radio("NAVIGATION", nav_items)

if st.sidebar.button("🔒 Secure Logout"):
    st.session_state.user = None
    st.session_state.role = None
    st.rerun()

# ==========================================
# 5. MODULE 1: DASHBOARD
# ==========================================
if choice == "📊 Overview Dashboard":
    st.title("📊 Store Performance Dashboard")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    df_cust = pd.read_sql('SELECT * FROM customers', conn)
    conn.close()

    total_skus = len(df_inv)
    low_stock = len(df_inv[df_inv["stock_qty"] <= 10])
    revenue = df_sales["total_amount"].sum() if not df_sales.empty else 0.0
    customers_count = len(df_cust)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total SKUs", total_skus)
    c2.metric("Low Stock Alerts", low_stock)
    c3.metric("Gross Revenue", f"${revenue:,.2f}")
    c4.metric("Client Accounts", customers_count)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📦 Inventory Snapshot")
        if not df_inv.empty:
            st.dataframe(df_inv[["item_code", "item_name", "stock_qty", "unit_price"]], use_container_width=True)
    with col2:
        st.subheader("💰 Recent Sales Log")
        if not df_sales.empty:
            st.dataframe(df_sales.head(5), use_container_width=True)

# ==========================================
# 6. MODULE 2: POS CHECKOUT TERMINAL
# ==========================================
elif choice == "🛒 POS Checkout":
    st.title("🛒 Point of Sale Terminal")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_cust = pd.read_sql('SELECT * FROM customers', conn)
    conn.close()

    col_pos1, col_pos2 = st.columns([1.5, 1])

    with col_pos1:
        st.subheader("Catalog Selection")
        selected_prod = st.selectbox("Select Product", df_inv['item_name'].tolist())
        p_row = df_inv[df_inv['item_name'] == selected_prod].iloc[0]

        st.write(f"**Code:** {p_row['item_code']} | **Price:** ${p_row['unit_price']} | **In Stock:** {p_row['stock_qty']}")
        qty = st.number_input("Quantity", min_value=1, max_value=int(p_row['stock_qty']) if p_row['stock_qty'] > 0 else 1, value=1)

        if "pos_cart" not in st.session_state:
            st.session_state.pos_cart = []

        if st.button("Add Item to Cart"):
            st.session_state.pos_cart.append({
                "item_code": p_row['item_code'],
                "item_name": selected_prod,
                "price": p_row['unit_price'],
                "qty": qty,
                "subtotal": p_row['unit_price'] * qty
            })
            st.success(f"Added {qty}x {selected_prod}")

    with col_pos2:
        st.subheader("Current Order Cart")
        if st.session_state.pos_cart:
            cart_df = pd.DataFrame(st.session_state.pos_cart)
            st.dataframe(cart_df[["item_name", "qty", "subtotal"]], use_container_width=True)
            
            grand_total = cart_df["subtotal"].sum()
            st.markdown(f"### **Total: ${grand_total:,.2f}**")

            client = st.selectbox("Customer", df_cust['name'].tolist())
            mode = st.selectbox("Payment Mode", ["Cash", "Credit Card", "Store Credit"])

            if st.button("Finalize Checkout"):
                invoice_id = f"INV-{date.today().strftime('%Y%m%d')}-{len(pd.read_sql('SELECT * FROM sales', get_db_connection()))+1}"
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?)', 
                                   (invoice_id, str(date.today()), st.session_state.user, client, grand_total, mode))
                    
                    for item in st.session_state.pos_cart:
                        cursor.execute('UPDATE inventory SET stock_qty = stock_qty - ? WHERE item_code = ?', 
                                       (item['qty'], item['item_code']))
                    conn.commit()
                    conn.close()
                    
                    st.success(f"Transaction successful! Invoice: {invoice_id}")
                    st.session_state.pos_cart = []
                except Exception as e:
                    st.error(f"Error processing transaction: {e}")

            if st.button("Clear Cart"):
                st.session_state.pos_cart = []
                st.rerun()
        else:
            st.write("Cart is empty.")

# ==========================================
# 7. MODULE 3: INVENTORY MANAGER
# ==========================================
elif choice == "📦 Inventory Stock":
    st.title("📦 Inventory Management")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.subheader("Active Inventory Stock")
    st.dataframe(df_inv, use_container_width=True)

    st.subheader("Add New Stock SKU")
    with st.form("add_inv", clear_on_submit=True):
        c1, c2 = st.columns(2)
        code = c1.text_input("Item Code", f"G-10{len(df_inv)+1}")
        name = c2.text_input("Item Name")
        cat = c1.selectbox("Category", ["Grains", "Pantry", "Dairy", "Beverages", "Household"])
        stock = c2.number_input("Initial Quantity", min_value=1, value=50)
        price = c1.number_input("Unit Price ($)", min_value=0.1, value=5.00)
        exp = c2.date_input("Expiry Date")

        if st.form_submit_button("Save Item"):
            if name:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?)', 
                                   (code, name, cat, stock, price, str(exp)))
                    conn.commit()
                    conn.close()
                    st.success("Item saved successfully.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Item code already exists.")
            else:
                st.error("Provide an item name.")

# ==========================================
# 8. MODULE 4: CUSTOMERS
# ==========================================
elif choice == "👥 Customers":
    st.title("👥 Customer Accounts")
    st.markdown("---")

    conn = get_db_connection()
    df_cust = pd.read_sql('SELECT * FROM customers', conn)
    conn.close()

    st.dataframe(df_cust, use_container_width=True)

    st.subheader("Register Customer")
    with st.form("add_cust", clear_on_submit=True):
        c1, c2 = st.columns(2)
        cid = c1.text_input("Customer ID", f"C-00{len(df_cust)+1}")
        cname = c2.text_input("Full Name")
        phone = c1.text_input("Phone Number")
        credit = c2.number_input("Credit Balance ($)", value=0.0)

        if st.form_submit_button("Save Customer"):
            if cname:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO customers VALUES (?, ?, ?, ?)', (cid, cname, phone, credit))
                    conn.commit()
                    conn.close()
                    st.success("Customer added.")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("Customer ID exists.")
            else:
                st.error("Enter customer name.")

# ==========================================
# 9. MODULE 5: REPORTS & EXPORTS
# ==========================================
elif choice == "📥 Sales Reports":
    st.title("📥 Reports & Data Export")
    st.markdown("---")

    conn = get_db_connection()
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    c1, c2 = st.columns(2)
    with c1:
        st.download_button("Download Sales CSV", df_sales.to_csv(index=False).encode('utf-8'), "sales_report.csv", "text/csv")
    with c2:
        st.download_button("Download Inventory CSV", df_inv.to_csv(index=False).encode('utf-8'), "inventory_report.csv", "text/csv")

# ==========================================
# 10. MODULE 6: ADMIN SECURE DATABASE EDITOR
# ==========================================
elif choice == "⚙️ Secure Database Editor" and st.session_state.role == "Admin":
    st.title("⚙️ Database Table Editor")
    st.caption("Direct secure administrative CRUD operations for SQLite tables.")
    st.markdown("---")

    tbl = st.selectbox("Select Table", ["inventory", "customers", "users", "sales"])

    conn = get_db_connection()
    df_tbl = pd.read_sql(f"SELECT * FROM {tbl}", conn)
    conn.close()

    st.info("Edit table cells directly below, then click **Commit Changes** to write updates to the database.")
    edited_df = st.data_editor(df_tbl, use_container_width=True, num_rows="dynamic")

    if st.button("Commit Changes"):
        try:
            conn = get_db_connection()
            edited_df.to_sql(tbl, conn, if_exists='replace', index=False)
            conn.close()
            st.success(f"Table `{tbl}` updated successfully.")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating table: {e}")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748b; font-size: 0.85rem;'>© 2026 Muzaffar Developers | Enterprise Grocery SaaS</p>", unsafe_allow_html=True)
