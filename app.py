import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ==========================================
# 1. PAGE CONFIGURATION & NEON ABSTRACT UI
# ==========================================
st.set_page_config(
    page_title="Muzaffar Developers | Neon ERP",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk / Neon CSS Design
NEON_CSS = """
<style>
    /* Dark Cyber Background Styling */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Neon Glow Headers */
    h1 {
        color: #00f0ff !important;
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.5), 0 0 20px rgba(0, 240, 255, 0.3);
        font-weight: 700 !important;
    }
    h2, h3 {
        color: #ff007f !important;
        text-shadow: 0 0 8px rgba(255, 0, 127, 0.4);
    }
    
    /* Neon Metric Cards */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.75);
        border: 1px solid rgba(0, 240, 255, 0.3);
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 0 15px rgba(0, 240, 255, 0.15);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 0 20px rgba(0, 240, 255, 0.35);
        border-color: #00f0ff;
    }
    div[data-testid="stMetricValue"] {
        color: #00f0ff !important;
        font-weight: bold;
    }
    
    /* Abstract Glass Form Styling */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 0, 127, 0.3);
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(255, 0, 127, 0.1);
    }
    
    /* Custom Neon Buttons */
    .stButton > button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #00f0ff 0%, #ff007f 100%) !important;
        color: #000000 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover, div[data-testid="stForm"] button:hover {
        box-shadow: 0 0 25px rgba(255, 0, 127, 0.8) !important;
        transform: scale(1.02);
    }
    
    /* Sidebar Aesthetics */
    section[data-testid="stSidebar"] {
        background-color: #05070e;
        border-right: 1px solid rgba(0, 240, 255, 0.2);
    }
    
    /* Dataframes Dark Theming */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 10px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
    }
</style>
"""
st.markdown(NEON_CSS, unsafe_allow_html=True)

# ==========================================
# 2. DATABASE ENGINE & INITIALIZATION
# ==========================================
DB_FILE = "neon_erp.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    return conn

def init_neon_db():
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
    
    # Seed Initial Data if Tables are Empty
    cursor.execute('SELECT COUNT(*) FROM inventory')
    if cursor.fetchone()[0] == 0:
        sample_inventory = [
            ("ITM-101", "Barcode Laser Scanner", "Hardware", 35, 120.0),
            ("ITM-102", "Heavy Passbook Printer", "Hardware", 8, 450.0),
            ("ITM-103", "Thermal Receipt Rolls", "Supplies", 150, 3.5),
            ("ITM-104", "ERP Software License", "Software", 5, 800.0)
        ]
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', sample_inventory)
        
    cursor.execute('SELECT COUNT(*) FROM sales')
    if cursor.fetchone()[0] == 0:
        sample_sales = [
            ("INV-5001", "2026-10-10", "Hamzah Sugar Mills", 2400.0, "Paid"),
            ("INV-5002", "2026-10-11", "Bahawalpur Logistics", 850.0, "Pending"),
            ("INV-5003", "2026-10-12", "Sadiq Industries", 1200.0, "Paid")
        ]
        cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', sample_sales)
        
    conn.commit()
    conn.close()

# Run DB setup
init_neon_db()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; color: #00f0ff;'>⚡ NEON ERP</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #ff007f; font-size: 12px;'>MUZAFFAR DEVELOPERS</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "NAVIGATION MODULES",
    ["⚡ Dashboard & Analytics", "📦 Stock & Inventory", "💰 Sales & Invoicing", "🗄️ DB Inspector", "📥 Reports & Export"]
)

# ==========================================
# 4. MODULE 1: DASHBOARD & ANALYTICS
# ==========================================
if menu == "⚡ Dashboard & Analytics":
    st.title("⚡ Enterprise Command Center")
    st.caption("Real-time telemetry and database operational metrics.")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    # Metric Calculations
    total_items = len(df_inv)
    total_stock = df_inv["stock"].sum() if not df_inv.empty else 0
    total_revenue = df_sales["amount"].sum() if not df_sales.empty else 0.0
    pending_bills = len(df_sales[df_sales["status"] == "Pending"]) if not df_sales.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("SKU Catalog Count", total_items)
    col2.metric("Total Warehouse Units", f"{total_stock:,}")
    col3.metric("Total Revenue Ledger", f"${total_revenue:,.2f}")
    col4.metric("Pending Invoices", pending_bills)

    st.markdown("<br>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📦 Inventory Stock Visualizer")
        if not df_inv.empty:
            st.bar_chart(df_inv.set_index("item_name")["stock"])
    with col_b:
        st.subheader("💰 Revenue Stream Breakdown")
        if not df_sales.empty:
            st.line_chart(df_sales.set_index("sale_date")["amount"])

# ==========================================
# 5. MODULE 2: INVENTORY MANAGEMENT
# ==========================================
elif menu == "📦 Stock & Inventory":
    st.title("📦 Inventory Control Ledger")
    st.caption("Manage catalog items with persistent SQLite updates.")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.subheader("Current Stock Records")
    st.dataframe(df_inv, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("➕ Register New SKU Item")
    
    with st.form("add_stock_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        code = c1.text_input("Item Code", f"ITM-{100 + len(df_inv) + 1}")
        name = c2.text_input("Item Name / Description")
        category = c1.selectbox("Category", ["Hardware", "Supplies", "Software", "Services"])
        stock = c2.number_input("Initial Stock Quantity", min_value=1, value=25)
        price = c1.number_input("Unit Price ($)", min_value=0.1, value=49.99, step=5.0)

        submitted = st.form_submit_button("⚡ Save SKU to Database")
        if submitted:
            if name:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', (code, name, category, stock, price))
                    conn.commit()
                    conn.close()
                    st.success(f"Item '{name}' [{code}] inserted into database!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Integrity Error: Item Code '{code}' already exists.")
            else:
                st.error("Please enter a valid Item Name.")

# ==========================================
# 6. MODULE 3: SALES & INVOICING
# ==========================================
elif menu == "💰 Sales & Invoicing":
    st.title("💰 Sales & Revenue Ledger")
    st.caption("Record transactions directly into the database.")
    st.markdown("---")

    conn = get_db_connection()
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    st.subheader("Sales Transaction History")
    st.dataframe(df_sales, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📄 Generate Sales Invoice")
    
    with st.form("add_sales_form", clear_on_submit=True):
        c1, c2 = st.columns(2)
        inv_no = c1.text_input("Invoice Number", f"INV-{5000 + len(df_sales) + 1}")
        customer = c2.text_input("Customer / Business Name")
        amount = c1.number_input("Invoice Amount ($)", min_value=1.0, value=250.0, step=10.0)
        status = c2.selectbox("Payment Status", ["Paid", "Pending", "Cancelled"])
        sale_date = st.date_input("Transaction Date", date.today())

        sale_submitted = st.form_submit_button("⚡ Save Transaction")
        if sale_submitted:
            if customer:
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', (inv_no, str(sale_date), customer, amount, status))
                    conn.commit()
                    conn.close()
                    st.success(f"Invoice '{inv_no}' recorded for {customer}!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Integrity Error: Invoice '{inv_no}' already exists.")
            else:
                st.error("Please enter a valid Customer Name.")

# ==========================================
# 7. MODULE 4: DB INSPECTOR
# ==========================================
elif menu == "🗄️ DB Inspector":
    st.title("🗄️ SQLite Database Inspector")
    st.caption("Direct view of raw SQLite tables stored in `neon_erp.db`.")
    st.markdown("---")

    conn = get_db_connection()
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)

    st.info(f"Connected Database File: **`{DB_FILE}`**")
    
    for table_name in tables['name']:
        st.subheader(f"Table Name: `{table_name}`")
        df_table = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        st.dataframe(df_table, use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
    conn.close()

# ==========================================
# 8. MODULE 5: REPORTS & EXPORT
# ==========================================
elif menu == "📥 Reports & Export":
    st.title("📥 System Auditing & Reports")
    st.caption("Export live database records into structured CSV spreadsheets.")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Export Inventory Catalog")
        csv_inv = df_inv.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⚡ Download Inventory CSV",
            data=csv_inv,
            file_name="neon_inventory_report.csv",
            mime="text/csv"
        )

    with col2:
        st.subheader("Export Sales Ledger")
        csv_sales = df_sales.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⚡ Download Sales CSV",
            data=csv_sales,
            file_name="neon_sales_report.csv",
            mime="text/csv"
        )

# ==========================================
# 9. FOOTER
# ==========================================
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #00f0ff; font-size: 13px;'>"
    "© 2026 <b>Muzaffar Developers</b> | Neon Abstract ERP System | SQLite Embedded Core"
    "</p>",
    unsafe_allow_html=True
)
