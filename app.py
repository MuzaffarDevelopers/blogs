import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# ----------------------------------------------------
# 1. PAGE CONFIGURATION & NEON STYLING
# ----------------------------------------------------
st.set_page_config(
    page_title="Muzaffar Developers | Neon ERP Suite",
    page_icon="⚡",
    layout="wide"
)

# Custom Neon CSS Injection
st.markdown("""
    <style>
    /* Dark Theme Core */
    .stApp {
        background-color: #0b0f19;
        color: #e2e8f0;
    }
    
    /* Neon Text Glows */
    .neon-title {
        font-weight: 800;
        color: #00f3ff;
        text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff;
        font-family: 'Courier New', Courier, monospace;
    }
    
    .neon-subtitle {
        color: #ff007f;
        text-shadow: 0 0 8px #ff007f;
        font-family: 'Courier New', Courier, monospace;
    }

    /* Glowing Neon Cards */
    div[data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.8);
        border: 1px solid #00f3ff;
        box-shadow: 0 0 12px rgba(0, 243, 255, 0.3);
        border-radius: 10px;
        padding: 15px;
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.6);
    }
    
    /* Neon Sidebar Customization */
    section[data-testid="stSidebar"] {
        background-color: #050811;
        border-right: 1px solid #ff007f;
        box-shadow: 5px 0 15px rgba(255, 0, 127, 0.2);
    }

    /* Custom Neon Form Inputs & Buttons */
    div[st-element="stForm"] {
        background: #0f172a;
        border: 1px solid #7928ca;
        box-shadow: 0 0 15px rgba(121, 40, 202, 0.4);
        border-radius: 12px;
        padding: 20px;
    }

    .stButton>button {
        background: linear-gradient(135deg, #00f3ff 0%, #7928ca 100%);
        color: #000;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        color: #fff;
        box-shadow: 0 0 20px rgba(0, 243, 255, 0.9);
        transform: scale(1.02);
    }
    
    /* Dataframe Glowing Wrapper */
    div[data-testid="stDataFrame"] {
        border: 1px solid #00f3ff;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.2);
    }
    </style>
""", unsafe_allow_html=True)


# ----------------------------------------------------
# 2. SQLITE DATABASE SETUP
# ----------------------------------------------------
def get_connection():
    return sqlite3.connect('neon_erp.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_code TEXT PRIMARY KEY,
            item_name TEXT,
            category TEXT,
            stock INTEGER,
            unit_price REAL
        )
    ''')
    
    # Sales Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_date TEXT,
            invoice_no TEXT PRIMARY KEY,
            customer TEXT,
            amount REAL,
            status TEXT
        )
    ''')
    
    # Populate Default Data if empty
    cursor.execute('SELECT COUNT(*) FROM inventory')
    if cursor.fetchone()[0] == 0:
        default_inventory = [
            ("ITM-001", "Barcode Scanner Unit", "Hardware", 45, 120.0),
            ("ITM-002", "Passbook Printer", "Hardware", 12, 350.0),
            ("ITM-003", "Thermal Paper Roll Box", "Supplies", 200, 25.0)
        ]
        cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', default_inventory)
        
    cursor.execute('SELECT COUNT(*) FROM sales')
    if cursor.fetchone()[0] == 0:
        default_sales = [
            ("2026-10-10", "INV-1001", "Hamzah Sugar Mills", 1500.0, "Paid"),
            ("2026-10-11", "INV-1002", "Sadiq Logistics", 750.0, "Pending")
        ]
        cursor.executemany('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', default_sales)
        
    conn.commit()
    conn.close()

init_db()


# ----------------------------------------------------
# 3. SIDEBAR NAVIGATION
# ----------------------------------------------------
st.sidebar.markdown("<h1 class='neon-title'>⚡ MUZAFFAR ERP</h1>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='color: #00f3ff; font-size: 12px;'>NEON EDITION v2.0</p>", unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    "NAVIGATION MODULES",
    ["📊 Dashboard", "📦 Inventory Control", "💰 Sales & Billing", "🗄️ Database Inspector", "📥 Data Export"]
)


# ----------------------------------------------------
# MODULE 1: DASHBOARD
# ----------------------------------------------------
if menu == "📊 Dashboard":
    st.markdown("<h1 class='neon-title'>SYSTEM DASHBOARD & ANALYTICS</h1>", unsafe_allow_html=True)
    st.markdown("<p class='neon-subtitle'>Real-time performance metrics</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    conn = get_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    total_items = len(df_inv)
    total_stock = df_inv["stock"].sum() if not df_inv.empty else 0
    total_rev = df_sales["amount"].sum() if not df_sales.empty else 0.0
    pending_count = len(df_sales[df_sales["status"] == "Pending"]) if not df_sales.empty else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📦 Active Items", total_items)
    c2.metric("⚡ Stock Quantity", f"{total_stock:,}")
    c3.metric("💰 Total Revenue", f"${total_rev:,.2f}")
    c4.metric("🚨 Pending Invoices", pending_count)

    st.markdown("<h3 class='neon-subtitle'>Inventory Levels Chart</h3>", unsafe_allow_html=True)
    if not df_inv.empty:
        st.bar_chart(df_inv.set_index("item_name")["stock"])


# ----------------------------------------------------
# MODULE 2: INVENTORY CONTROL
# ----------------------------------------------------
elif menu == "📦 Inventory Control":
    st.markdown("<h1 class='neon-title'>INVENTORY & STOCK CONTROL</h1>", unsafe_allow_html=True)
    st.markdown("---")

    conn = get_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.markdown("<h3 class='neon-subtitle'>Current Stock Records</h3>", unsafe_allow_html=True)
    st.dataframe(df_inv, use_container_width=True)

    st.markdown("<h3 class='neon-subtitle'>Add Stock Record</h3>", unsafe_allow_html=True)
    with st.form("add_item_neon"):
        col1, col2 = st.columns(2)
        code = col1.text_input("Item Code", f"ITM-00{len(df_inv)+1}")
        name = col2.text_input("Item Name")
        category = col1.selectbox("Category", ["Hardware", "Supplies", "Software License", "Services"])
        stock = col2.number_input("Stock Quantity", min_value=1, value=10)
        price = col1.number_input("Unit Price ($)", min_value=0.0, value=50.0, step=5.0)

        submitted = st.form_submit_button("⚡ Save to Database")
        if submitted:
            if name:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', (code, name, category, stock, price))
                    conn.commit()
                    conn.close()
                    st.success(f"Item '{name}' saved to SQLite database successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Item Code '{code}' already exists.")
            else:
                st.error("Item Name cannot be empty.")


# ----------------------------------------------------
# MODULE 3: SALES & BILLING
# ----------------------------------------------------
elif menu == "💰 Sales & Billing":
    st.markdown("<h1 class='neon-title'>SALES LEDGER & INVOICING</h1>", unsafe_allow_html=True)
    st.markdown("---")

    conn = get_connection()
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    st.markdown("<h3 class='neon-subtitle'>Sales Transactions</h3>", unsafe_allow_html=True)
    st.dataframe(df_sales, use_container_width=True)

    st.markdown("<h3 class='neon-subtitle'>Create New Invoice</h3>", unsafe_allow_html=True)
    with st.form("add_sale_neon"):
        col1, col2 = st.columns(2)
        inv_no = col1.text_input("Invoice Number", f"INV-100{len(df_sales)+1}")
        customer = col2.text_input("Customer Name")
        amount = col1.number_input("Amount ($)", min_value=1.0, value=250.0)
        status = col2.selectbox("Payment Status", ["Paid", "Pending", "Cancelled"])
        sale_date = st.date_input("Transaction Date", date.today())

        sale_submitted = st.form_submit_button("⚡ Record Invoice")
        if sale_submitted:
            if customer:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', (str(sale_date), inv_no, customer, amount, status))
                    conn.commit()
                    conn.close()
                    st.success(f"Invoice '{inv_no}' recorded for {customer}!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Invoice Number '{inv_no}' already exists.")
            else:
                st.error("Customer Name cannot be empty.")


# ----------------------------------------------------
# MODULE 4: DATABASE INSPECTOR
# ----------------------------------------------------
elif menu == "🗄️ Database Inspector":
    st.markdown("<h1 class='neon-title'>DATABASE TABLE INSPECTOR</h1>", unsafe_allow_html=True)
    st.markdown("<p class='neon-subtitle'>Direct SQLite `neon_erp.db` inspection</p>", unsafe_allow_html=True)
    st.markdown("---")

    conn = get_connection()
    tables = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
    
    for table_name in tables['name']:
        st.markdown(f"<h3 class='neon-subtitle'>Table: <code>{table_name}</code></h3>", unsafe_allow_html=True)
        df_table = pd.read_sql(f"SELECT * FROM {table_name}", conn)
        st.dataframe(df_table, use_container_width=True)
        
    conn.close()


# ----------------------------------------------------
# MODULE 5: DATA EXPORT
# ----------------------------------------------------
elif menu == "📥 Data Export":
    st.markdown("<h1 class='neon-title'>REPORTS & EXPORTS</h1>", unsafe_allow_html=True)
    st.markdown("---")

    conn = get_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("<h3 class='neon-subtitle'>Export Inventory</h3>", unsafe_allow_html=True)
        csv_inv = df_inv.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⚡ Download Inventory CSV",
            data=csv_inv,
            file_name="neon_erp_inventory.csv",
            mime="text/csv"
        )

    with col2:
        st.markdown("<h3 class='neon-subtitle'>Export Sales Ledger</h3>", unsafe_allow_html=True)
        csv_sales = df_sales.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="⚡ Download Sales CSV",
            data=csv_sales,
            file_name="neon_erp_sales.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: #00f3ff;'>© 2026 Muzaffar Developers | Powered by Neon SQLite Engine</p>", unsafe_allow_html=True)
