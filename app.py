import streamlit as st
import pandas as pd
from datetime import date

# Page Setup
st.set_page_config(
    page_title="Muzaffar Developers | ERP System",
    page_icon="📦",
    layout="wide"
)

# Initialize Session State for ERP Data (In-Memory Database)
if "inventory" not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        {"Item Code": "ITM-001", "Item Name": "Scanner Unit", "Category": "Hardware", "Stock": 45, "Unit Price ($)": 120.0},
        {"Item Code": "ITM-002", "Item Name": "Passbook Printer", "Category": "Hardware", "Stock": 12, "Unit Price ($)": 350.0},
        {"Item Code": "ITM-003", "Item Name": "Thermal Paper Rolls", "Category": "Supplies", "Stock": 200, "Unit Price ($)": 2.5},
    ])

if "sales" not in st.session_state:
    st.session_state.sales = pd.DataFrame([
        {"Date": "2026-10-10", "Invoice No": "INV-1001", "Customer": "Hamzah Sugar Mills", "Amount ($)": 1500.0, "Status": "Paid"},
        {"Date": "2026-10-11", "Invoice No": "INV-1002", "Customer": "Sadiq Logistics", "Amount ($)": 750.0, "Status": "Pending"},
    ])

# Navigation
st.sidebar.title("🏢 Muzaffar ERP System")
st.sidebar.caption("Enterprise Management Suite")
page = st.sidebar.radio("Modules", ["📊 Dashboard", "📦 Inventory Control", "💰 Sales & Billing", "📥 Export & Reports"])

# ----------------------------------------------------
# MODULE 1: DASHBOARD
# ----------------------------------------------------
if page == "📊 Dashboard":
    st.title("Business Overview & Analytics")
    st.markdown("---")
    
    # Key Metrics
    total_items = len(st.session_state.inventory)
    total_stock_qty = st.session_state.inventory["Stock"].sum()
    total_revenue = st.session_state.sales["Amount ($)"].sum()
    pending_sales = len(st.session_state.sales[st.session_state.sales["Status"] == "Pending"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Products", total_items)
    col2.metric("Total Units in Stock", int(total_stock_qty))
    col3.metric("Total Sales Revenue", f"${total_revenue:,.2f}")
    col4.metric("Pending Invoices", pending_sales)

    st.subheader("Inventory Stock Levels")
    st.bar_chart(st.session_state.inventory.set_index("Item Name")["Stock"])

# ----------------------------------------------------
# MODULE 2: INVENTORY CONTROL
# ----------------------------------------------------
elif page == "📦 Inventory Control":
    st.title("Inventory & Stock Management")
    st.markdown("---")

    # Display Current Inventory
    st.subheader("Current Stock Ledger")
    st.dataframe(st.session_state.inventory, use_container_width=True)

    # Form to Add New Item
    st.subheader("Add New Stock Item")
    with st.form("add_item_form"):
        col1, col2 = st.columns(2)
        code = col1.text_input("Item Code", f"ITM-00{len(st.session_state.inventory)+1}")
        name = col2.text_input("Item Name")
        category = col1.selectbox("Category", ["Hardware", "Supplies", "Software License", "Services"])
        stock = col2.number_input("Initial Stock Quantity", min_value=1, value=10)
        price = col1.number_input("Unit Price ($)", min_value=0.0, value=50.0, step=5.0)

        submitted = st.form_submit_button("Add Item to ERP")
        if submitted:
            if name:
                new_row = {"Item Code": code, "Item Name": name, "Category": category, "Stock": stock, "Unit Price ($)": price}
                st.session_state.inventory = pd.concat([st.session_state.inventory, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Item '{name}' successfully added!")
                st.rerun()
            else:
                st.error("Please enter an Item Name.")

# ----------------------------------------------------
# MODULE 3: SALES & BILLING
# ----------------------------------------------------
elif page == "💰 Sales & Billing":
    st.title("Sales Ledger & Invoicing")
    st.markdown("---")

    st.subheader("Recent Sales Transactions")
    st.dataframe(st.session_state.sales, use_container_width=True)

    # Form to Record New Sale
    st.subheader("Create New Sales Invoice")
    with st.form("add_sale_form"):
        col1, col2 = st.columns(2)
        inv_no = col1.text_input("Invoice Number", f"INV-100{len(st.session_state.sales)+1}")
        customer = col2.text_input("Customer Name")
        amount = col1.number_input("Invoice Amount ($)", min_value=1.0, value=250.0)
        status = col2.selectbox("Payment Status", ["Paid", "Pending", "Cancelled"])
        sale_date = st.date_input("Transaction Date", date.today())

        sale_submitted = st.form_submit_button("Record Transaction")
        if sale_submitted:
            if customer:
                new_sale = {"Date": str(sale_date), "Invoice No": inv_no, "Customer": customer, "Amount ($)": amount, "Status": status}
                st.session_state.sales = pd.concat([st.session_state.sales, pd.DataFrame([new_sale])], ignore_index=True)
                st.success(f"Invoice '{inv_no}' recorded for {customer}!")
                st.rerun()
            else:
                st.error("Please enter a Customer Name.")

# ----------------------------------------------------
# MODULE 4: EXPORT & REPORTS
# ----------------------------------------------------
elif page == "📥 Export & Reports":
    st.title("Data Export & Reports")
    st.markdown("---")
    st.write("Download system records as CSV files for spreadsheet auditing:")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Export Inventory Data")
        csv_inv = st.session_state.inventory.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Inventory CSV",
            data=csv_inv,
            file_name="erp_inventory_report.csv",
            mime="text/csv"
        )

    with col2:
        st.subheader("Export Sales Ledger")
        csv_sales = st.session_state.sales.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📄 Download Sales Ledger CSV",
            data=csv_sales,
            file_name="erp_sales_report.csv",
            mime="text/csv"
        )

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>© 2026 Muzaffar Developers | Modular ERP System Powered by Streamlit</p>", unsafe_allow_html=True)
