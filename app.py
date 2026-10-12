import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ==========================================
# 1. PAGE CONFIGURATION & POLYGON LIGHT THEME
# ==========================================
st.set_page_config(
    page_title="Muzaffar Developers | Poly-Vibrant ERP",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Low-Poly Vibrant Light Theme CSS
POLY_CSS = """
<style>
    /* Clean Light Polygon Background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #edf2f7 50%, #fef2f2 100%);
        color: #1e293b;
    }
    
    /* Vibrant Gradient Headers */
    h1 {
        background: linear-gradient(90deg, #2563eb, #9333ea, #db2777);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }
    h2, h3 {
        color: #0f172a !important;
    }
    
    /* Frosted Glass Cards / Metrics */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.85);
        border: 1px solid rgba(147, 51, 234, 0.2);
        border-radius: 14px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(147, 51, 234, 0.15);
        border-color: #9333ea;
    }
    div[data-testid="stMetricValue"] {
        color: #2563eb !important;
        font-weight: 700;
    }
    
    /* Forms Styling */
    div[data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.9);
        border: 1px solid rgba(37, 99, 235, 0.2);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 25px rgba(0, 0, 0, 0.06);
    }
    
    /* Vibrant Multi-Color Action Buttons */
    .stButton > button, div[data-testid="stForm"] button {
        background: linear-gradient(135deg, #2563eb 0%, #9333ea 50%, #db2777 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(147, 51, 234, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    .stButton > button:hover, div[data-testid="stForm"] button:hover {
        opacity: 0.95;
        box-shadow: 0 6px 20px rgba(219, 39, 119, 0.4) !important;
        transform: scale(1.01);
    }
    
    /* Sidebar Light Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid rgba(226, 232, 240, 1);
    }
    
    /* Dataframes Theming */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(203, 213, 225, 1);
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
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

def init_poly_db():
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
            ("ITM-201", "Polygon Scanner Unit", "Hardware", 40, 130.0),
            ("ITM-202", "Executive Passbook Printer", "Hardware", 10, 400.0),
            ("ITM-203", "Thermal Receipt Rolls", "Supplies", 180, 3.0),
            ("ITM-204", "ERP Enterprise License", "Software", 6, 750.0)
        ]
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', sample_inventory)
        
    cursor.execute('SELECT COUNT(*) FROM sales')
    if cursor.fetchone()[0] == 0:
        sample_sales = [
            ("INV-8001", "2026-10-10", "Hamzah Sugar Mills", 2600.0, "Paid"),
            ("INV-8002", "2026-10-11", "Bahawalpur Logistics", 900.0, "Pending"),
            ("INV-8003", "2026-10-12", "Sadiq Industries", 1350.0, "Paid")
        ]
        cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', sample_sales)
        
    conn.commit()
    conn.close()

# Initialize DB
init_poly_db()

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.markdown("<h2 style='text-align: center; background: linear-gradient(90deg, #2563eb, #db2777); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🎨 POLY ERP</h2>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center; color: #64748b; font-size: 12px; font-weight: 600;'>MUZAFFAR DEVELOPERS</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "NAVIGATION MODULES",
    ["📊 Dashboard & Analytics", "📦 Stock & Inventory", "💰 Sales & Invoicing", "🗄️ DB Inspector", "📥 Reports & Export"]
)

# ==========================================
# 4. MODULE 1: DASHBOARD & ANALYTICS
# ==========================================
if menu == "📊 Dashboard & Analytics":
    st.title("📊 Enterprise Overview")
    st.caption("Live polygon-styled analytical command center.")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

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
        st.subheader("📦 Inventory Stock Levels")
        if not df_inv.empty:
            st.bar_chart(df_inv.set_index("item_name")["stock"])
    with col_b:
        st.subheader("💰 Revenue Trend")
        if not df_sales.empty:
            st.line_chart(df_sales.set_index("sale_date")["amount"])

# ==========================================
# 5. MODULE 2: INVENTORY MANAGEMENT
# ==========================================
elif menu == "📦 Stock & Inventory":
    st.title("📦 Inventory Management")
    st.caption("Track and update stock items stored in SQLite.")
    st.markdown("---")

    conn = get_db_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.subheader("Current Stock Ledger")
    st.dataframe(df_inv, use_container_width=True)

    st.markdown("<br>", unsafe_allow
