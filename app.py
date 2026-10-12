import streamlit as st
import pandas as pd
import sqlite3
from datetime import date

# Page Setup
st.set_page_config(
    page_title="Muzaffar Developers | ERP System",
    page_icon="📦",
    layout="wide"
)

# --- DATABASE CONNECTION & SETUP ---
def get_connection():
    # Connects to a local SQLite database file named 'erp.db'
    conn = sqlite3.connect('erp.db', check_same_thread=False)
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create Inventory Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS inventory (
            item_code TEXT PRIMARY KEY,
            item_name TEXT,
            category TEXT,
            stock INTEGER,
            unit_price REAL
        )
    ''')
    
    # Create Sales Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            sale_date TEXT,
            invoice_no TEXT PRIMARY KEY,
            customer TEXT,
            amount REAL,
            status TEXT
        )
    ''')
    
    # Insert default sample data if tables are empty
    cursor.execute('SELECT COUNT(*) FROM inventory')
    if cursor.fetchone()[0] == 0:
        default_inventory = [
            ("ITM-001", "Scanner Unit", "Hardware", 45, 120.0),
            ("ITM-002", "Passbook Printer", "Hardware", 12, 350.0),
            ("ITM-003", "Thermal Paper Rolls", "Supplies", 200, 2.5)
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

# Initialize the database on startup
init_db()

# Navigation
st.sidebar.title("🏢 Muzaffar ERP System")
st.sidebar.caption("Connected to SQLite Database")
page = st.sidebar.radio("Modules", ["📊 Dashboard", "📦 Inventory Control", "💰 Sales & Billing", "📥 Export & Reports"])

# ----------------------------------------------------
# MODULE 1: DASHBOARD
# ----------------------------------------------------
if page == "📊 Dashboard":
    st.title("Business Overview & Analytics")
    st.markdown("---")
    
    conn = get_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()
    
    total_items = len(df_inv)
    total_stock_qty = df_inv["stock"].sum() if not df_inv.empty else 0
    total_revenue = df_sales["amount"].sum() if not df_sales.empty else 0.0
    pending_sales = len(df_sales[df_sales["status"] == "Pending"]) if not df_sales.empty else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Products", total_items)
    col2.metric("Total Units in Stock", int(total_stock_qty))
    col3.metric("Total Sales Revenue", f"${total_revenue:,.2f}")
    col4.metric("Pending Invoices", pending_sales)

    if not df_inv.empty:
        st.subheader("Inventory Stock Levels")
        st.bar_chart(df_inv.set_index("item_name")["stock"])

# ----------------------------------------------------
# MODULE 2: INVENTORY CONTROL
# ----------------------------------------------------
elif page == "📦 Inventory Control":
    st.title("Inventory & Stock Management")
    st.markdown("---")

    conn = get_connection()
    df_inv = pd.read_sql('SELECT * FROM inventory', conn)
    conn.close()

    st.subheader("Current Stock Ledger")
    st.dataframe(df_inv, use_container_width=True)

    st.subheader("Add New Stock Item")
    with st.form("add_item_form"):
        col1, col2 = st.columns(2)
        code = col1.text_input("Item Code", f"ITM-00{len(df_inv)+1}")
        name = col2.text_input("Item Name")
        category = col1.selectbox("Category", ["Hardware", "Supplies", "Software License", "Services"])
        stock = col2.number_input("Initial Stock Quantity", min_value=1, value=10)
        price = col1.number_input("Unit Price ($)", min_value=0.0, value=50.0, step=5.0)

        submitted = st.form_submit_button("Save to Database")
        if submitted:
            if name:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO inventory VALUES (?, ?, ?, ?, ?)', (code, name, category, stock, price))
                    conn.commit()
                    conn.close()
                    st.success(f"Item '{name}' successfully saved to database!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Item Code '{code}' already exists.")
            else:
                st.error("Please enter an Item Name.")

# ----------------------------------------------------
# MODULE 3: SALES & BILLING
# ----------------------------------------------------
elif page == "💰 Sales & Billing":
    st.title("Sales Ledger & Invoicing")
    st.markdown("---")

    conn = get_connection()
    df_sales = pd.read_sql('SELECT * FROM sales', conn)
    conn.close()

    st.subheader("Recent Sales Transactions")
    st.dataframe(df_sales, use_container_width=True)

    st.subheader("Create New Sales Invoice")
    with st.form("add_sale_form"):
        col1, col2 = st.columns(2)
        inv_no = col1.text_input("Invoice Number", f"INV-100{len(df_sales)+1}")
        customer = col2.text_input("Customer Name")
        amount = col1.number_input("Invoice Amount ($)", min_value=1.0, value=250.0)
        status = col2.selectbox("Payment Status", ["Paid", "Pending", "Cancelled"])
        sale_date = st.date_input("Transaction Date", date.today())

        sale_submitted = st.form_submit_button("Save Transaction to Database")
        if sale_submitted:
            if customer:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute('INSERT INTO sales VALUES (?, ?, ?, ?, ?)', (str(sale_date), inv_no, customer, amount, status))
                    conn.commit()
                    conn.close()
                    st.success(f"Invoice '{inv_no}' saved to database!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error(f"Error: Invoice Number '{inv_no}' already exists.")
            else:
                st.error("Please enter a Customer Name.")

# ----------------------------------------------------
# MODULE 4: EXPORT & REPORTS
# ----------------------------------------------------
elif page == "📥 Export & Reports":
    st.title("Data Export & Reports")
    st.markdown("---")
    
    conn = get_connection()
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
            file_name="erp_inventory_report.csv",
            mime="text/csv"
        )

    with col2:
        st.subheader("Export Sales Ledger")
        csv_sales = df_sales.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Sales Ledger CSV",
            data=csv_sales,
            file_name="erp_sales_report.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 Muzaffar Developers | SQLite-Powered ERP System</p>", unsafe_allow_html=True)
