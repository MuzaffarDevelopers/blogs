from datetime import datetime
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

# Page Configuration
st.set_page_config(page_title="Supply Chain Portal (Supabase Cloud)", layout="wide")

# ---------------------------------------------------------
# DATABASE CONNECTION SETUP (SUPABASE / POSTGRESQL)
# ---------------------------------------------------------
st.sidebar.title("☁️ Supabase Cloud DB")
db_url = st.sidebar.text_input(
    "PostgreSQL Connection URL",
    type="password",
    help="Paste your Supabase database URI here (postgresql://user:pass@host:port/dbname)",
)

if not db_url:
  st.title("📦 Integrated Supply Chain Portal")
  st.warning("⚠️ Please enter your Supabase PostgreSQL Connection URL in the sidebar to connect the database.")
  st.info(
      "**How to get it:** Go to your Supabase Project Settings -> Database -> Connection string -> URI."
  )
  st.stop()


@st.cache_resource
def get_engine(url):

engine =if db_url.startswith("postgresql://") and not "+psycopg2" in db_url:
  db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)
 create_engine(db_url)


try:
  engine = get_engine(db_url)
  # Test connection
  with engine.connect() as conn:
    conn.execute(text("SELECT 1"))
except Exception as e:
  st.error(f"❌ Database Connection Failed: {e}")
  st.stop()


def init_db():
  with engine.begin() as conn:
    # 1. Bulks Table (PostgreSQL syntax)
    conn.execute(text("""
            CREATE TABLE IF NOT EXISTS bulks (
                id SERIAL PRIMARY KEY,
                blk_no TEXT UNIQUE NOT NULL,
                qty INTEGER NOT NULL,
                status TEXT DEFAULT 'SENT',
                decline_reason TEXT,
                created_at TEXT
            )
        """))

    # 2. Purchase Orders Table
    conn.execute(text("""
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id SERIAL PRIMARY KEY,
                po_no TEXT UNIQUE NOT NULL,
                buyer TEXT NOT NULL,
                qty INTEGER NOT NULL,
                sale_status TEXT DEFAULT 'NEW',
                loading_status TEXT DEFAULT 'PENDING',
                allocated_details TEXT,
                created_at TEXT
            )
        """))

    # Seed Demo Data if bulks table is empty
    result = conn.execute(text("SELECT COUNT(*) FROM bulks")).fetchone()[0]
    if result == 0:
      demo_bulks = [
          ("BLK#001", 20, "ACCEPTED", None),
          ("BLK#002", 30, "ACCEPTED", None),
          ("BLK#003", 25, "SENT", None),
      ]
      for b in demo_bulks:
        conn.execute(
            text(
                "INSERT INTO bulks (blk_no, qty, status, decline_reason, created_at) VALUES (:blk, :qty, :status, :reason, :time) ON CONFLICT (blk_no) DO NOTHING"
            ),
            {
                "blk": b[0],
                "qty": b[1],
                "status": b[2],
                "reason": b[3],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        )

    result_po = conn.execute(text("SELECT COUNT(*) FROM purchase_orders")).fetchone()[0]
    if result_po == 0:
      demo_pos = [
          ("1240", "Acme Corp", 10, "ACCEPTED", "PENDING", None),
          ("1241", "Global Traders", 10, "ACCEPTED", "PENDING", None),
          ("1242", "Beta Industries", 15, "NEW", "PENDING", None),
      ]
      for p in demo_pos:
        conn.execute(
            text(
                "INSERT INTO purchase_orders (po_no, buyer, qty, sale_status, loading_status, allocated_details, created_at) VALUES (:po, :buyer, :qty, :sale, :load, :alloc, :time) ON CONFLICT (po_no) DO NOTHING"
            ),
            {
                "po": p[0],
                "buyer": p[1],
                "qty": p[2],
                "sale": p[3],
                "load": p[4],
                "alloc": p[5],
                "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
            },
        )


init_db()

# Session State for Staff Login
if "staff_logged_in" not in st.session_state:
  st.session_state.staff_logged_in = False

# ---------------------------------------------------------
# SIDEBAR - STAFF LOGIN / SESSION CONTROL
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.title("🔐 Staff Portal Access")
if not st.session_state.staff_logged_in:
  st.sidebar.markdown("Buyers do not need to login. Use below for **Sale, Production, Warehouse & Gatekeeper**.")
  with st.sidebar.form("staff_login_form"):
    staff_pass = st.text_input("Staff Password", type="password")
    login_btn = st.form_submit_button("Staff Login")

    if login_btn:
      if staff_pass == "pass123":
        st.session_state.staff_logged_in = True
        st.success("Staff login successful!")
        st.rerun()
      else:
        st.error("Incorrect staff password. (Hint: pass123)")
  st.sidebar.info("Shared Staff Password: `pass123`")
else:
  st.sidebar.success("Logged in as Internal Staff")
  if st.sidebar.button("Staff Logout"):
    st.session_state.staff_logged_in = False
    st.rerun()

# ---------------------------------------------------------
# MAIN APP NAVIGATION & TABS
# ---------------------------------------------------------
st.title("📦 Integrated Supply Chain Portal (Cloud)")

if st.session_state.staff_logged_in:
  tab_buyer, tab_prod, tab_wh, tab_sale, tab_load, tab_admin = st.tabs([
      "🛒 Buyer Portal (Open)",
      "🏭 Production",
      "🏢 Warehouse",
      "💼 Sale Office",
      "🚚 Truck Loading",
      "🛠️ Editable Database",
  ])
else:
  tab_buyer, = st.tabs(["🛒 Buyer Portal (Open)"])

# ---------------------------------------------------------
# 1. BUYER PORTAL (OPEN TO ALL)
# ---------------------------------------------------------
with tab_buyer:
  st.header("🛒 Buyer Order Tracking Portal")
  st.markdown("Welcome! Track your purchase orders and live dispatch status here without logging in.")

  buyer_df = pd.read_sql(
      "SELECT po_no, buyer, qty, sale_status, loading_status, allocated_details FROM purchase_orders",
      engine,
  )

  if not buyer_df.empty:
    display_data = []
    for _, row in buyer_df.iterrows():
      sale = row["sale_status"]
      loading = row["loading_status"]

      if loading == "CLEAR":
        status_display = "CLEAR (Loaded)"
      elif sale == "PENDING":
        status_display = "PENDING"
      elif sale == "ACCEPTED":
        status_display = "LOADING"
      else:
        status_display = "NEW"

      display_data.append({
          "PO#": row["po_no"],
          "Buyer": row["buyer"],
          "Qty": row["qty"],
          "Decision / Status": status_display,
          "Allocation Details": row["allocated_details"] or "Pending Dispatch",
      })

    st.dataframe(pd.DataFrame(display_data), use_container_width=True)
  else:
    st.info("No purchase orders registered in the system.")

# ---------------------------------------------------------
# 2. PRODUCTION TAB (STAFF ONLY)
# ---------------------------------------------------------
if st.session_state.staff_logged_in:
  with tab_prod:
    st.header("Production - Bulk Dispatch")

    with st.form("new_bulk_form"):
      c1, c2 = st.columns(2)
      with c1:
        new_blk_no = st.text_input("Bulk Number (e.g., BLK#004)")
      with c2:
        new_blk_qty = st.number_input("Quantity (Bags)", min_value=1, value=20, step=1)
      submit_bulk = st.form_submit_button("Send Bulk to Warehouse")

      if submit_bulk:
        if new_blk_no.strip() == "":
          st.error("Bulk Number cannot be empty.")
        else:
          try:
            with engine.begin() as conn:
              conn.execute(
                  text(
                      "INSERT INTO bulks (blk_no, qty, status, created_at) VALUES (:blk, :qty, 'SENT', :time)"
                  ),
                  {
                      "blk": new_blk_no.strip(),
                      "qty": new_blk_qty,
                      "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                  },
              )
            st.success(f"Bulk {new_blk_no} sent to Warehouse successfully!")
            st.rerun()
          except Exception as e:
            st.error(f"Error or Bulk Number {new_blk_no} already exists: {e}")

    st.subheader("Dispatched Bulks Status")
    bulks_df = pd.read_sql(
        "SELECT blk_no, qty, status, decline_reason, created_at FROM bulks", engine
    )

    if not bulks_df.empty:
      for idx, row in bulks_df.iterrows():
        with st.container():
          c1, c2, c3, c4 = st.columns([2, 2, 2, 4])
          c1.write(f"**{row['blk_no']}**")
          c2.write(f"Qty: {row['qty']}")

          status = row["status"]
          if status == "ACCEPTED":
            c3.success("ACCEPTED")
          elif status == "DECLINED":
            c3.error("DECLINED")
          else:
            c3.warning("SENT")

          if status == "DECLINED":
            c4.write(f"Reason: *{row['decline_reason'] or 'No reason provided'}*")
            if st.button(f"Re-send {row['blk_no']}", key=f"resend_{row['blk_no']}_{idx}"):
              with engine.begin() as conn:
                conn.execute(
                    text(
                        "UPDATE bulks SET status = 'SENT', decline_reason = NULL WHERE blk_no = :blk"
                    ),
                    {"blk": row["blk_no"]},
                )
              st.success(f"Bulk {row['blk_no']} re-sent to Warehouse!")
              st.rerun()
          elif status == "SENT":
            c4.write("Pending Warehouse Review")
          else:
            c4.write("Stock added to inventory pool.")
    else:
      st.info("No bulks dispatched yet.")

  # ---------------------------------------------------------
  # 3. WAREHOUSE TAB (STAFF ONLY)
  # ---------------------------------------------------------
  with tab_wh:
    st.header("Warehouse - Incoming Bulks & Inventory")

    st.subheader("Incoming Bulks Inspection")
    sent_bulks = pd.read_sql(
        "SELECT id, blk_no, qty, status, decline_reason FROM bulks WHERE status = 'SENT'",
        engine,
    )

    if not sent_bulks.empty:
      for _, row in sent_bulks.iterrows():
        with st.expander(f"Inspect: {row['blk_no']} (Qty: {row['qty']})"):
          col1, col2 = st.columns(2)
          with col1:
            if st.button("Accept Bulk", key=f"acc_{row['id']}"):
              with engine.begin() as conn:
                conn.execute(
                    text("UPDATE bulks SET status = 'ACCEPTED' WHERE id = :id"),
                    {"id": row["id"]},
                )
              st.success(f"Bulk {row['blk_no']} accepted into stock!")
              st.rerun()
          with col2:
            decline_reason = st.text_input("Decline Reason (Optional)", key=f"dec_reason_{row['id']}")
            if st.button("Decline Bulk", key=f"dec_{row['id']}"):
              with engine.begin() as conn:
                conn.execute(
                    text(
                        "UPDATE bulks SET status = 'DECLINED', decline_reason = :reason WHERE id = :id"
                    ),
                    {"reason": decline_reason, "id": row["id"]},
                )
              st.warning(f"Bulk {row['blk_no']} declined.")
              st.rerun()
    else:
      st.info("No incoming bulks waiting for inspection.")

    st.divider()
    st.subheader("Current Accepted Stock (FIFO Pool)")
    accepted_df = pd.read_sql(
        "SELECT blk_no, qty FROM bulks WHERE status = 'ACCEPTED' ORDER BY blk_no ASC",
        engine,
    )
    if not accepted_df.empty:
      st.dataframe(accepted_df, use_container_width=True)
      total_avail = accepted_df["qty"].sum()
      st.metric("Total Available Accepted Stock", f"{total_avail} Bags")
    else:
      st.warning("No accepted stock available in the warehouse.")

  # ---------------------------------------------------------
  # 4. SALE OFFICE TAB (STAFF ONLY)
  # ---------------------------------------------------------
  with tab_sale:
    st.header("Sale Office - Purchase Order Review")

    with st.form("new_po_form"):
      c1, c2, c3 = st.columns(3)
      with c1:
        po_no = st.text_input("PO Number (e.g., 1243)")
      with c2:
        buyer_name = st.text_input("Buyer Name")
      with c3:
        po_qty = st.number_input("Order Quantity (Bags)", min_value=1, value=10, step=1)
      submit_po = st.form_submit_button("Create Purchase Order")

      if submit_po:
        if po_no.strip() == "" or buyer_name.strip() == "":
          st.error("Please fill in all PO details.")
        else:
          try:
            with engine.begin() as conn:
              conn.execute(
                  text(
                      "INSERT INTO purchase_orders (po_no, buyer, qty, sale_status, loading_status, created_at) VALUES (:po, :buyer, :qty, 'NEW', 'PENDING', :time)"
                  ),
                  {
                      "po": po_no.strip(),
                      "buyer": buyer_name.strip(),
                      "qty": po_qty,
                      "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                  },
              )
            st.success(f"PO {po_no} created successfully!")
            st.rerun()
          except Exception as e:
            st.error(f"Error or PO Number {po_no} already exists: {e}")

    st.subheader("Manage Purchase Orders")
    po_df = pd.read_sql(
        "SELECT id, po_no, buyer, qty, sale_status, loading_status FROM purchase_orders",
        engine,
    )

    if not po_df.empty:
      for _, row in po_df.iterrows():
        cols = st.columns([2, 2, 2, 2, 2])
        cols[0].write(f"**PO#{row['po_no']}**")
        cols[1].write(f"Buyer: {row['buyer']}")
        cols[2].write(f"Qty: {row['qty']}")
        cols[3].write(f"Status: **{row['sale_status']}**")

        with cols[4]:
          if row["sale_status"] != "ACCEPTED":
            if st.button("Accept", key=f"po_acc_{row['id']}"):
              with engine.begin() as conn:
                conn.execute(
                    text("UPDATE purchase_orders SET sale_status = 'ACCEPTED' WHERE id = :id"),
                    {"id": row["id"]},
                )
              st.success(f"PO {row['po_no']} accepted and sent to Warehouse!")
              st.rerun()
          if row["sale_status"] != "PENDING":
            if st.button("Pending", key=f"po_pend_{row['id']}"):
              with engine.begin() as conn:
                conn.execute(
                    text("UPDATE purchase_orders SET sale_status = 'PENDING' WHERE id = :id"),
                    {"id": row["id"]},
                )
              st.info(f"PO {row['po_no']} put on Pending hold.")
              st.rerun()
    else:
      st.info("No purchase orders found.")

  # ---------------------------------------------------------
  # 5. TRUCK LOADING TAB (STAFF ONLY)
  # ---------------------------------------------------------
  with tab_load:
    st.header("Truck Loading & OGP Generation (Gatekeeper)")
    st.markdown("Orders accepted by the Sale Office can be loaded. Allocation strictly follows the lowest **BLK#** first.")

    ready_pos = pd.read_sql(
        "SELECT id, po_no, buyer, qty, loading_status FROM purchase_orders WHERE sale_status = 'ACCEPTED' AND loading_status != 'CLEAR'",
        engine,
    )

    if not ready_pos.empty:
      selected_po_no = st.selectbox("Select PO to Load onto Truck", ready_pos["po_no"].tolist())
      po_row = ready_pos[ready_pos["po_no"] == selected_po_no].iloc[0]

      st.write(f"**Buyer:** {po_row['buyer']} | **Required Qty:** {po_row['qty']} Bags")

      if st.button("Attempt Truck Loading"):
        bulks_stock = pd.read_sql(
            "SELECT id, blk_no, qty FROM bulks WHERE status = 'ACCEPTED' ORDER BY blk_no ASC",
            engine,
        )

        needed_qty = po_row["qty"]
        total_available = bulks_stock["qty"].sum()

        if total_available < needed_qty:
          st.error(
              f"❌ Truck cannot be loaded! Accepted stock is not enough. Needed: {needed_qty} bags, Available: {total_available} bags."
          )
        else:
          allocation = []
          remaining_needed = needed_qty
          bulks_to_update = []

          for _, b in bulks_stock.iterrows():
            if remaining_needed <= 0:
              break
            b_id = b["id"]
            b_no = b["blk_no"]
            b_qty = b["qty"]

            if b_qty <= remaining_needed:
              allocation.append(f"{b_qty} from {b_no}")
              remaining_needed -= b_qty
              bulks_to_update.append((0, b_id))
            else:
              allocation.append(f"{remaining_needed} from {b_no}")
              new_b_qty = b_qty - remaining_needed
              remaining_needed = 0
              bulks_to_update.append((new_b_qty, b_id))

          split_str = " + ".join(allocation)

          with engine.begin() as conn:
            for new_qty, b_id in bulks_to_update:
              if new_qty == 0:
                conn.execute(text("DELETE FROM bulks WHERE id = :id"), {"id": b_id})
              else:
                conn.execute(
                    text("UPDATE bulks SET qty = :qty WHERE id = :id"),
                    {"qty": new_qty, "id": b_id},
                )

            conn.execute(
                text(
                    "UPDATE purchase_orders SET loading_status = 'CLEAR', allocated_details = :alloc WHERE id = :id"
                ),
                {"alloc": split_str, "id": po_row["id"]},
            )

          st.success("🚚 Truck Loaded Successfully!")
          st.balloons()
          st.info(f"**Outward Gate Pass (OGP) Split Message:** PO#{po_row['po_no']} loaded with: {split_str}")
          st.rerun()
    else:
      st.info("No approved POs awaiting truck loading.")

    st.divider()
    st.subheader("Loading History & OGP Log")
    loaded_df = pd.read_sql(
        "SELECT po_no, buyer, qty, allocated_details FROM purchase_orders WHERE loading_status = 'CLEAR'",
        engine,
    )
    if not loaded_df.empty:
      st.dataframe(loaded_df, use_container_width=True)
    else:
      st.info("No truck dispatches completed yet.")

  # ---------------------------------------------------------
  # 6. EDITABLE DATABASE TAB (STAFF ONLY)
  # ---------------------------------------------------------
  with tab_admin:
    st.header("Database Administration & Editable Tables")
    st.markdown("Directly view and edit database tables (`bulks`, `purchase_orders`).")

    table_choice = st.selectbox("Select Database Table to Edit", ["bulks", "purchase_orders"])

    table_df = pd.read_sql(f"SELECT * FROM {table_choice}", engine)

    st.markdown(f"**Editing `{table_choice}` table directly:**")
    edited_df = st.data_editor(table_df, num_rows="dynamic", use_container_width=True, key=f"editor_{table_choice}")

    if st.button("Save Changes to Database"):
      try:
        edited_df.to_sql(table_choice, engine, if_exists="replace", index=False)
        st.success(f"Table `{table_choice}` successfully updated and saved to Supabase PostgreSQL!")
        st.rerun()
      except Exception as e:
        st.error(f"Error saving changes: {e}")
