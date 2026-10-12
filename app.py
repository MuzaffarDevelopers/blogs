import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ==========================================
# 1. PAGE CONFIGURATION & GEOMETRIC UI
# ==========================================
st.set_page_config(
    page_title="Muzaffar Developers | Secure ERP",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Poly-Vibrant CSS Styling
POLY_CSS = """
<style>
    .stApp {
        background: linear-gradient(135deg, rgba(255,182,193,0.35) 0%, rgba(135,206,250,0.35) 50%, rgba(152,251,152,0.35) 100%),
                    url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2000&auto=format&fit=crop');
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
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: blur(12px);
    }
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.85);
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
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
    }
    .stButton > button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
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
st.markdown(POLY_CSS, unsafe_allow_html=True)

# ==========================================
# 2. DATABASE ENGINE & INITIALIZATION
# ==========================================
DB_FILE = "poly_erp.db"

def get_db_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_code TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL,
            unit_price REAL NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            invoice_no TEXT PRIMARY KEY,
            sale_date TEXT NOT NULL,
            customer TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    cursor.execute('SELECT COUNT(*) FROM inventory')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', [
            ("M10001", "Inchvok Product", "Product", 35, 1150.0),
            ("M10002", "Product Sharper", "Product", 1250, 270.0),
            ("M10003", "Product Hearper", "Product", 75, 38.0)
        ])
        
    cursor.execute('SELECT COUNT(*) FROM sales')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', [
            ("31001", "15/10/2022", "Customer", 1150.0, "Changed"),
            ("31002", "09/10/2022", "Manper", 270.0, "Changed")
        ])
        
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. PASSWORD AUTHENTICATION SYSTEM
# ==========================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h2 style='text-align: center;'>🔐 Secure ERP Login</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569;'>Enter your credentials to unlock database access.</p>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            login_btn = st.form_submit_button("Login to ERP")
            
            if login_btn:
                # Default Login: Username = admin, Password = muzaffar123
                if username == "admin" and password == "muzaffar123":
                    st.session_state.authenticated = True
                    st.success("Access Granted! Loading system...")
                    st.rerun()
                else:
                    st.error("Invalid Username or Password! (Hint: admin / muzaffar123)")
    st.stop()

# ==========================================
# 4. SIDEBAR NAVIGATION (Unlocked)
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #0f172a;'>🎨 MUZAFFAR</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #0284c7; font-weight: 700; font-size: 13px;'>DEVELOPERS PORTAL</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "NAVIGATION MENU",
    ["📊 Dashboard", "📦 Inventory Control", "💰 Sales Invoicing", "✏️ Editable Database Manager", "📥 Reports & Export"]
)

if st.sidebar.button("🔒 Lock / Logout"):
    st.session_state.authenticated = False
    st.rerun()

# ==========================================
# 5. MODULE 1: DASHBOARD
# ==========================================
if menu == "📊 Dashboard":
    st.title("⚡ NEON ERP: COMMAND CENTER")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("SKU COUNT", len(df_inv))
    col2.metric("WAREHOUSE STOCK", f"{df_inv['stock'].sum():,} units" if not df_inv.empty else 0)
    col3.metric("TOTAL REVENUE", f"${df_sales['amount'].sum():,.2f}" if not df_sales.empty else "$0.00")
    col4.metric("PENDING INVOICES", len(df_sales[df_sales["status"] == "Pending"]) if not df_sales.empty else 0)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("📦 Recent Inventory")
        st.dataframe(df_inv.head(5), use_container_width=True)
    with c2:
        st.subheader("💰 Recent Sales")
        st.dataframe(df_sales.head(5), use_container_width=True)

# ==========================================
# 6. MODULE 2: INVENTORY CONTROL
# ==========================================
elif menu == "📦 Inventory Control":
    st.title("📦 Inventory Control & SKU Management")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.subheader("Current Stock Database")
    st.dataframe(df_inv, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("➕ Add New Stock Item")
    with st.form("add_inv_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        code = c1.text_input("Item Code", f"M1000{len(df_inv)+1}")
        name = c2.text_input("Item Name / Description")
        category = c1.selectbox("Category", ["Product", "Category", "Hardware", "Supplies"])
        stock = c2.number_input("Stock Quantity", min_value=1, value=50)
        price = c1.number_input("Unit Price ($)", min_value=0.1, value=150.0, step=10.0)

        if st.form_submit_button("⚡ Save New SKU"):
            if name:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', (code, name, category, stock, price))
                    conn.commit()
                    conn.close()
                    st.success(f"Item '{name}' added successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Item Code '{code}' already exists.")
            else:
                st.error("Please provide an Item Name.")

# ==========================================
# 7. MODULE 3: SALES INVOICING
# ==========================================
elif menu == "💰 Sales Invoicing":
    st.title("💰 Sales Ledger & Invoices")
    st.markdown("---")

    conn = get_db_connection()
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    st.subheader("All Sales Records")
    st.dataframe(df_sales, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📄 Create New Invoice")
    with st.form("add_sale_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        inv_no = c1.text_input("Invoice Number", str(3100 + len(df_sales) + 1))
        customer = c2.text_input("Customer Name")
        amount = c1.number_input("Invoice Amount ($)", min_value=1.0, value=350.0, step=25.0)
        status = c2.selectbox("Status", ["Changed", "Pending", "Paid"])
        sale_date = st.date_input("Transaction Date", date.today())

        if st.form_submit_button("⚡ Record Invoice"):
            if customer:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', (inv_no, sale_date.strftime("%d/%m/%Y"), customer, amount, status))
                    conn.commit()
                    conn.close()
                    st.success(f"Invoice '{inv_no}' saved!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Invoice Number '{inv_no}' already exists.")
            else:
                st.error("Please enter a Customer Name.")

# ==========================================
# 8. MODULE 4: EDITABLE DATABASE MANAGER
# ==========================================
elif menu == "✏️ Editable Database Manager":
    st.title("✏️ Interactive Database Editor")
    st.caption("Directly edit table values or delete obsolete rows from SQLite.")
    st.markdown("---")

    table_choice = st.selectbox("Select Table to Edit", ["inventory", "sales"])

    conn = get_db_connection()
    df_current = pd.read_sql(f"SELECT * FROM {table_choice}", conn)
    conn.close()

    st.info("💡 **Tip:** Double click any cell in the table below to edit its value directly. Click **Save Database Changes** when you're done.")

    # Streamlit Data Editor component
    edited_df = st.data_editor(df_current, use_container_width=True, num_rows="dynamic")

    if st.button("💾 Save Database Changes"):
        try:
            conn = get_db_connection()
            # Overwrite the table with edited dataframe values
            edited_df.to_sql(table_choice, conn, if_exists='replace', index=False)
            conn.close()
            st.success(f"Table `{table_choice}` successfully updated and saved to database!")
            st.rerun()
        except Exception as e:
            st.error(f"Error saving changes: {e}")

# ==========================================
# 9. MODULE 5: REPORTS & EXPORT
# ==========================================
elif menu == "📥 Reports & Export":
    st.title("📥 Spreadsheet Auditing & Reports")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Export Inventory Data")
        st.download_button("📄 Download Inventory CSV", df_inv.to_csv(index=False).encode('utf-8'), "inventory_report.csv", "text/csv")
    with c2:
        st.subheader("Export Sales Ledger")
        st.download_button("📄 Download Sales CSV", df_sales.to_csv(index=False).encode('utf-8'), "sales_report.csv", "text/csv")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #334155; font-weight: 600; font-size: 13px;'>© 2026 Muzaffar Developers | Secure Editable ERP System</p>", unsafe_allow_html=True)
