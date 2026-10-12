import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ==========================================
# 1. PAGE CONFIGURATION & GEOMETRIC UI
# ==========================================
st.set_page_config(
    page_title="Muzaffar Developers | Poly-Vibrant ERP",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Poly-Vibrant CSS Styling matching your design reference
POLY_CSS = """
<style>
    /* Low-Poly Vibrant Multicolored Background */
    .stApp {
        background: linear-gradient(135deg, rgba(255,182,193,0.35) 0%, rgba(135,206,250,0.35) 50%, rgba(152,251,152,0.35) 100%),
                    url('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?q=80&w=2000&auto=format&fit=crop');
        background-size: cover;
        background-attachment: fixed;
        background-blend-mode: overlay;
        color: #1e293b;
    }
    
    /* High-Contrast Bold Headings */
    h1 {
        color: #0f172a !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(255,255,255,0.8);
    }
    h2, h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }
    
    /* Frosted Glass Sidebar */
    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.75) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(255, 255, 255, 0.6);
    }
    
    /* Frosted Glass Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.15);
        backdrop-filter: blur(4px);
    }
    div[data-testid="stMetricValue"] {
        color: #0284c7 !important;
        font-weight: 800 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #475569 !important;
        font-weight: 600 !important;
    }
    
    /* Frosted Glass Container / Forms */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(255, 255, 255, 1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        backdrop-filter: blur(6px);
    }
    
    /* Vibrant Gradient Action Buttons */
    .stButton > button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 10px !important;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.6) !important;
    }
    
    /* High Contrast Tables */
    div[data-testid="stDataFrame"] {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 1);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
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
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_code TEXT PRIMARY KEY,
            item_name TEXT NOT NULL,
            category TEXT NOT NULL,
            stock INTEGER NOT NULL,
            unit_price REAL NOT NULL
        )
    ''')
    
    # Sales Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            invoice_no TEXT PRIMARY KEY,
            sale_date TEXT NOT NULL,
            customer TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    # Seed Data if Empty
    cursor.execute('SELECT COUNT(*) FROM inventory')
    if cursor.fetchone()[0] == 0:
        sample_inventory = [
            ("M10001", "Inchvok Product", "Product", 35, 1150.0),
            ("M10002", "Product Sharper", "Product", 1250, 270.0),
            ("M10003", "Product Hearper", "Product", 75, 38.0),
            ("M10004", "Black Sheaper", "Product", 60, 100.0),
            ("M10005", "Brant Flay", "Category", 15, 125.0)
        ]
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', sample_inventory)
        
    cursor.execute('SELECT COUNT(*) FROM sales')
    if cursor.fetchone()[0] == 0:
        sample_sales = [
            ("31001", "15/10/2022", "Customer", 1150.0, "Changed"),
            ("31002", "09/10/2022", "Manper", 270.0, "Changed"),
            ("31003", "06/10/2022", "Manper", 38.0, "Pending"),
            ("31004", "17/10/2022", "Customer", 100.0, "Changed"),
            ("31007", "08/10/2022", "Emile", 125.0, "Changed")
        ]
        cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', sample_sales)
        
    conn.commit()
    conn.close()

init_db()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #0f172a;'>🎨 MUZAFFAR</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #0284c7; font-weight: 700; font-size: 13px;'>DEVELOPERS PORTAL</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "NAVIGATION MENU",
    ["📊 Dashboard", "📦 Inventory Control", "💰 Sales Invoicing", "🗄️ Database Inspector", "📥 Reports & Export"]
)

# ==========================================
# 4. MODULE 1: DASHBOARD
# ==========================================
if menu == "📊 Dashboard":
    st.title("⚡ NEON ERP: COMMAND CENTER")
    st.caption("High-contrast analytics and geometric operational overview.")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    sku_count = len(df_inv)
    total_stock = df_inv["stock"].sum() if not df_inv.empty else 0
    total_revenue = df_sales["amount"].sum() if not df_sales.empty else 0.0
    pending_invoices = len(df_sales[df_sales["status"] == "Pending"]) if not df_sales.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("SKU COUNT", sku_count)
    col2.metric("WAREHOUSE STOCK", f"{total_stock:,} units")
    col3.metric("TOTAL REVENUE", f"${total_revenue:,.2f}")
    col4.metric("PENDING INVOICES", pending_invoices)

    st.markdown("<br>", unsafe_allow_html=True)
    
    c_left, c_right = st.columns(2)
    with c_left:
        st.subheader("📦 Stock Ledger (Recently Updated)")
        if not df_inv.empty:
            st.dataframe(df_inv.head(5), use_container_width=True)
            
    with c_right:
        st.subheader("💰 Recent Sales Transactions")
        if not df_sales.empty:
            st.dataframe(df_sales.head(5), use_container_width=True)

# ==========================================
# 5. MODULE 2: INVENTORY CONTROL
# ==========================================
elif menu == "📦 Inventory Control":
    st.title("📦 Inventory Control & SKU Management")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.subheader("Full Stock Database")
    st.dataframe(df_inv, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("➕ Add New Stock Item")
    
    with st.form("add_inv_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        code = col1.text_input("Item Code", f"M1000{len(df_inv)+1}")
        name = col2.text_input("Item Name / Description")
        category = col1.selectbox("Category", ["Product", "Category", "Hardware", "Supplies"])
        stock = col2.number_input("Stock Quantity", min_value=1, value=50)
        price = col1.number_input("Unit Price ($)", min_value=0.1, value=150.0, step=10.0)

        submitted = st.form_submit_button("⚡ Save New SKU")
        if submitted:
            if name:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', (code, name, category, stock, price))
                    conn.commit()
                    conn.close()
                    st.success(f"Item '{name}' successfully stored in SQLite DB!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Item Code '{code}' already exists.")
            else:
                st.error("Please provide an Item Name.")

# ==========================================
# 6. MODULE 3: SALES INVOICING
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
        col1, col2 = st.columns(2)
        inv_no = col1.text_input("Invoice Number", str(3100 + len(df_sales) + 1))
        customer = col2.text_input("Customer Name")
        amount = col1.number_input("Invoice Amount ($)", min_value=1.0, value=350.0, step=25.0)
        status = col2.selectbox("Status", ["Changed", "Pending", "Paid"])
        sale_date = st.date_input("Transaction Date", date.today())

        sale_submitted = st.form_submit_button("⚡ Record Invoice")
        if sale_submitted:
            if customer:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    # Format date to match DD/MM/YYYY or standard YYYY-MM-DD
                    formatted_date = sale_date.strftime("%d/%m/%Y")
                    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', (inv_no, formatted_date, customer, amount, status))
                    conn.commit()
                    conn.close()
                    st.success(f"Invoice '{inv_no}' successfully saved!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Invoice Number '{inv_no}' already exists.")
            else:
                st.error("Please enter a Customer Name.")

# ==========================================
# 7. MODULE 4: DATABASE INSPECTOR
# ==========================================
elif menu == "🗄️ Database Inspector":
    st.title("🗄️ SQLite Raw Database Inspector")
    st.caption(f"Inspection view for `{DB_FILE}`")
    st.markdown("---")

    conn = get_db_connection()
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

    for tbl in tables['name']:
        st.subheader(f"Table: `{tbl}`")
        df_tbl = pd.read_sql(f"SELECT * FROM {tbl}", conn)
        st.dataframe(df_tbl, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
    conn.close()

# ==========================================
# 8. MODULE 5: REPORTS & EXPORT
# ==========================================
elif menu == "📥 Reports & Export":
    st.title("📥 Spreadsheet Auditing & Reports")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Export Inventory Data")
        csv_inv = df_inv.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Inventory CSV",
            data=csv_inv,
            file_name="poly_inventory_report.csv",
            mime="text/csv"
        )

    with col2:
        st.subheader("Export Sales Ledger")
        csv_sales = df_sales.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Sales CSV",
            data=csv_sales,
            file_name="poly_sales_report.csv",
            mime="text/csv"
        )

# ==========================================
# 9. FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #334155; font-weight: 600; font-size: 13px;'>"
    "© 2026 <b>Muzaffar Developers</b> | Poly-Vibrant Design & SQLite Database Core"
    "</p>",
    unsafe_allow_html=True
)
