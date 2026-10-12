import sqlite3
from datetime import datetime
import pandas as pd
import streamlit as st

DB_NAME = "supply_chain.db"


def get_connection():
  return sqlite3.connect(DB_NAME, check_same_thread=False)


def init_db():
  conn = get_connection()
  cursor = conn.cursor()

  # 1. Users Table for Secure Login & Roles
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )
    """)

  # 2. Bulks Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS bulks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            blk_no TEXT UNIQUE NOT NULL,
            qty INTEGER NOT NULL,
            status TEXT DEFAULT 'SENT',
            decline_reason TEXT,
            created_at TEXT
        )
    """)

  # 3. Purchase Orders Table
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            po_no TEXT UNIQUE NOT NULL,
            buyer TEXT NOT NULL,
            qty INTEGER NOT NULL,
            sale_status TEXT DEFAULT 'NEW',
            loading_status TEXT DEFAULT 'PENDING',
            allocated_details TEXT,
            created_at TEXT
        )
    """)

  # Auto-migration / Schema checks for old databases
  cursor.execute("PRAGMA table_info(bulks)")
  bulk_cols = [col[1] for col in cursor.fetchall()]
  if "status" not in bulk_cols:
    cursor.execute("ALTER TABLE bulks ADD COLUMN status TEXT DEFAULT 'ACCEPTED'")
  if "decline_reason" not in bulk_cols:
    cursor.execute("ALTER TABLE bulks ADD COLUMN decline_reason TEXT")

  cursor.execute("PRAGMA table_info(purchase_orders)")
  po_cols = [col[1] for col in cursor.fetchall()]
  if "sale_status" not in po_cols:
    cursor.execute("ALTER TABLE purchase_orders ADD COLUMN sale_status TEXT DEFAULT 'NEW'")
  if "loading_status" not in po_cols:
    cursor.execute("ALTER TABLE purchase_orders ADD COLUMN loading_status TEXT DEFAULT 'PENDING'")
  if "allocated_details" not in po_cols:
    cursor.execute("ALTER TABLE purchase_orders ADD COLUMN allocated_details TEXT")

  # Seed Default Users if empty (Passwords are stored plainly for demo simplicity; use hashing for production)
  cursor.execute("SELECT COUNT(*) FROM users")
  if cursor.fetchone()[0] == 0:
    default_users = [
        ("buyer1", "pass123", "Buyer"),
        ("sale1", "pass123", "Sale Office"),
        ("prod1", "pass123", "Production"),
        ("wh1", "pass123", "Warehouse"),
        ("gate1", "pass123", "Gatekeeper"),
        ("admin", "admin123", "Admin"),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
        default_users,
    )

  # Seed Demo Data if bulks/POs are empty
  cursor.execute("SELECT COUNT(*) FROM bulks")
  if cursor.fetchone()[0] == 0:
    demo_bulks = [
        ("BLK#001", 20, "ACCEPTED", None),
        ("BLK#002", 30, "ACCEPTED", None),
        ("BLK#003", 25, "SENT", None),
    ]
    cursor.executemany(
        "INSERT OR IGNORE INTO bulks (blk_no, qty, status, decline_reason, created_at) VALUES (?, ?, ?, ?, ?)",
        [(b[0], b[1], b[2], b[3], datetime.now().strftime("%Y-%m-%d %H:%M")) for b in demo_bulks],
    )

  cursor.execute("SELECT COUNT(*) FROM purchase_orders")
  if cursor.fetchone()[0] == 0:
    demo_pos = [
        ("1240", "Acme Corp", 10, "ACCEPTED", "PENDING", None),
        ("1241", "Global Traders", 10, "ACCEPTED", "PENDING", None),
        ("1242", "Beta Industries", 15, "NEW", "PENDING", None),
    ]
    cursor.executemany(
        """INSERT OR IGNORE INTO purchase_orders 
           (po_no, buyer, qty, sale_status, loading_status, allocated_details, created_at) 
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        [(p[0], p[1], p[2], p[3], p[4], p[5], datetime.now().strftime("%Y-%m-%d %H:%M")) for p in demo_pos],
    )

  conn.commit()
  conn.close()


init_db()

st.set_page_config(page_title="Secure Supply Chain Portal", layout="wide")

# Session State Initialization for Authentication
if "authenticated" not in st.session_state:
  st.session_state.authenticated = False
  st.session_state.username = ""
  st.session_state.role = ""

# ---------------------------------------------------------
# AUTHENTICATION LOGIN / LOGOUT SCREEN
# ---------------------------------------------------------
if not st.session_state.authenticated:
  st.title("🔐 Supply Chain Portal - Secure Login")
  with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submit_login = st.form_submit_button("Login")

    if submit_login:
      conn = get_connection()
      cursor = conn.cursor()
      cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username.strip(), password))
      user = cursor.fetchone()
      conn.close()

      if user:
        st.session_state.authenticated = True
        st.session_state.username = username
        st.session_state.role = user[0]
        st.success(f"Welcome back, {username} ({user[0]})!")
        st.rerun()
      else:
        st.error("Invalid username or password.")

  st.info(
      "**Demo Credentials:**\n"
      "- Buyer: `buyer1` / `pass123`\n"
      "- Sale Office: `sale1` / `pass123`\n"
      "- Production: `prod1` / `pass123`\n"
      "- Warehouse: `wh1` / `pass123`\n"
      "- Gatekeeper (Truck Loading): `gate1` / `pass123`\n"
      "- Admin (Editable DB): `admin` / `admin123`"
  )
  st.stop()

# ---------------------------------------------------------
# MAIN APP (AUTHENTICATED VIEWS)
# ---------------------------------------------------------
st.sidebar.title("👤 User Session")
st.sidebar.write(f"**User:** {st.session_state.username}")
st.sidebar.write(f"**Role:** {st.session_state.role}")
if st.sidebar.button("Logout"):
  st.session_state.authenticated = False
  st.session_state.username = ""
  st.session_state.role = ""
  st.rerun()

st.title("📦 Integrated Supply Chain Portal")
current_role = st.session_state.role

# Determine accessible tabs based on role
tabs_list = []
role_to_tab_index = 0

if current_role == "Buyer":
  tabs_list = ["🛒 Buyer Portal"]
elif current_role == "Sale Office":
  tabs_list = ["💼 Sale Office", "🛒 Buyer Portal"]
elif current_role == "Production":
  tabs_list = ["🏭 Production", "🏢 Warehouse"]
elif current_role == "Warehouse":
  tabs_list = ["🏢 Warehouse", "🏭 Production"]
elif current_role == "Gatekeeper":
  tabs_list = ["🚚 Truck Loading"]
elif current_role == "Admin":
  tabs_list = [
      "🏭 Production",
      "🏢 Warehouse",
      "💼 Sale Office",
      "🚚 Truck Loading",
      "🛒 Buyer Portal",
      "🛠️ Editable Database",
  ]
else:
  tabs_list = ["🛒 Buyer Portal"]

# Create Dynamic Tabs
created_tabs = st.tabs(tabs_list)

# Map tabs content based on names in tabs_list
for tab_name, tab_ui in zip(tabs_list, created_tabs):

  # ---------------------------------------------------------
  # 1. PRODUCTION TAB
  # ---------------------------------------------------------
  if tab_name == "🏭 Production":
    with tab_ui:
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
            conn = get_connection()
            cursor = conn.cursor()
            try:
              cursor.execute(
                  "INSERT INTO bulks (blk_no, qty, status, created_at) VALUES (?, ?, 'SENT', ?)",
                  (new_blk_no.strip(), new_blk_qty, datetime.now().strftime("%Y-%m-%d %H:%M")),
              )
              conn.commit()
              st.success(f"Bulk {new_blk_no} sent to Warehouse successfully!")
              st.rerun()
            except sqlite3.IntegrityError:
              st.error(f"Bulk Number {new_blk_no} already exists.")
            finally:
              conn.close()

      st.subheader("Dispatched Bulks Status")
      conn = get_connection()
      bulks_df = pd.read_sql("SELECT blk_no, qty, status, decline_reason, created_at FROM bulks", conn)
      conn.close()

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
                conn = get_connection()
                conn.execute(
                    "UPDATE bulks SET status = 'SENT', decline_reason = NULL WHERE blk_no = ?",
                    (row["blk_no"],),
                )
                conn.commit()
                conn.close()
                st.success(f"Bulk {row['blk_no']} re-sent to Warehouse!")
                st.rerun()
            elif status == "SENT":
              c4.write("Pending Warehouse Review")
            else:
              c4.write("Stock added to inventory pool.")
      else:
        st.info("No bulks dispatched yet.")

  # ---------------------------------------------------------
  # 2. WAREHOUSE TAB
  # ---------------------------------------------------------
  elif tab_name == "🏢 Warehouse":
    with tab_ui:
      st.header("Warehouse - Incoming Bulks & Inventory")

      st.subheader("Incoming Bulks Inspection")
      conn = get_connection()
      sent_bulks = pd.read_sql(
          "SELECT id, blk_no, qty, status, decline_reason FROM bulks WHERE status = 'SENT'",
          conn,
      )
      conn.close()

      if not sent_bulks.empty:
        for _, row in sent_bulks.iterrows():
          with st.expander(f"Inspect: {row['blk_no']} (Qty: {row['qty']})"):
            col1, col2 = st.columns(2)
            with col1:
              if st.button("Accept Bulk", key=f"acc_{row['id']}"):
                conn = get_connection()
                conn.execute("UPDATE bulks SET status = 'ACCEPTED' WHERE id = ?", (row["id"],))
                conn.commit()
                conn.close()
                st.success(f"Bulk {row['blk_no']} accepted into stock!")
                st.rerun()
            with col2:
              decline_reason = st.text_input("Decline Reason (Optional)", key=f"dec_reason_{row['id']}")
              if st.button("Decline Bulk", key=f"dec_{row['id']}"):
                conn = get_connection()
                conn.execute(
                    "UPDATE bulks SET status = 'DECLINED', decline_reason = ? WHERE id = ?",
                    (decline_reason, row["id"]),
                )
                conn.commit()
                conn.close()
                st.warning(f"Bulk {row['blk_no']} declined.")
                st.rerun()
      else:
        st.info("No incoming bulks waiting for inspection.")

      st.divider()
      st.subheader("Current Accepted Stock (FIFO Pool)")
      conn = get_connection()
      accepted_df = pd.read_sql("SELECT blk_no, qty FROM bulks WHERE status = 'ACCEPTED' ORDER BY blk_no ASC", conn)
      conn.close()
      if not accepted_df.empty:
        st.dataframe(accepted_df, use_container_width=True)
        total_avail = accepted_df["qty"].sum()
        st.metric("Total Available Accepted Stock", f"{total_avail} Bags")
      else:
        st.warning("No accepted stock available in the warehouse.")

  # ---------------------------------------------------------
  # 3. SALE OFFICE TAB
  # ---------------------------------------------------------
  elif tab_name == "💼 Sale Office":
    with tab_ui:
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
            conn = get_connection()
            cursor = conn.cursor()
            try:
              cursor.execute(
                  """INSERT INTO purchase_orders (po_no, buyer, qty, sale_status, loading_status, created_at) 
                     VALUES (?, ?, ?, 'NEW', 'PENDING', ?)""",
                  (
                      po_no.strip(),
                      buyer_name.strip(),
                      po_qty,
                      datetime.now().strftime("%Y-%m-%d %H:%M"),
                  ),
              )
              conn.commit()
              st.success(f"PO {po_no} created successfully!")
              st.rerun()
            except sqlite3.IntegrityError:
              st.error(f"PO Number {po_no} already exists.")
            finally:
              conn.close()

      st.subheader("Manage Purchase Orders")
      conn = get_connection()
      po_df = pd.read_sql("SELECT id, po_no, buyer, qty, sale_status, loading_status FROM purchase_orders", conn)
      conn.close()

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
                conn = get_connection()
                conn.execute("UPDATE purchase_orders SET sale_status = 'ACCEPTED' WHERE id = ?", (row["id"],))
                conn.commit()
                conn.close()
                st.success(f"PO {row['po_no']} accepted and sent to Warehouse!")
                st.rerun()
            if row["sale_status"] != "PENDING":
              if st.button("Pending", key=f"po_pend_{row['id']}"):
                conn = get_connection()
                conn.execute("UPDATE purchase_orders SET sale_status = 'PENDING' WHERE id = ?", (row["id"],))
                conn.commit()
                conn.close()
                st.info(f"PO {row['po_no']} put on Pending hold.")
                st.rerun()
      else:
        st.info("No purchase orders found.")

  # ---------------------------------------------------------
  # 4. TRUCK LOADING TAB
  # ---------------------------------------------------------
  elif tab_name == "🚚 Truck Loading":
    with tab_ui:
      st.header("Truck Loading & OGP Generation (Gatekeeper)")
      st.markdown("Orders accepted by the Sale Office can be loaded. Allocation strictly follows the lowest **BLK#** first.")

      conn = get_connection()
      ready_pos = pd.read_sql(
          "SELECT id, po_no, buyer, qty, loading_status FROM purchase_orders WHERE sale_status = 'ACCEPTED' AND loading_status != 'CLEAR'",
          conn,
      )
      conn.close()

      if not ready_pos.empty:
        selected_po_no = st.selectbox("Select PO to Load onto Truck", ready_pos["po_no"].tolist())
        po_row = ready_pos[ready_pos["po_no"] == selected_po_no].iloc[0]

        st.write(f"**Buyer:** {po_row['buyer']} | **Required Qty:** {po_row['qty']} Bags")

        if st.button("Attempt Truck Loading"):
          conn = get_connection()
          bulks_stock = pd.read_sql(
              "SELECT id, blk_no, qty FROM bulks WHERE status = 'ACCEPTED' ORDER BY blk_no ASC",
              conn,
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

            cursor = conn.cursor()
            for new_qty, b_id in bulks_to_update:
              if new_qty == 0:
                cursor.execute("DELETE FROM bulks WHERE id = ?", (b_id,))
              else:
                cursor.execute("UPDATE bulks SET qty = ? WHERE id = ?", (new_qty, b_id))

            cursor.execute(
                "UPDATE purchase_orders SET loading_status = 'CLEAR', allocated_details = ? WHERE id = ?",
                (split_str, po_row["id"]),
            )
            conn.commit()
            conn.close()

            st.success("🚚 Truck Loaded Successfully!")
            st.balloons()
            st.info(f"**Outward Gate Pass (OGP) Split Message:** PO#{po_row['po_no']} loaded with: {split_str}")
            st.rerun()
      else:
        st.info("No approved POs awaiting truck loading.")

      st.divider()
      st.subheader("Loading History & OGP Log")
      conn = get_connection()
      loaded_df = pd.read_sql(
          "SELECT po_no, buyer, qty, allocated_details FROM purchase_orders WHERE loading_status = 'CLEAR'",
          conn,
      )
      conn.close()
      if not loaded_df.empty:
        st.dataframe(loaded_df, use_container_width=True)
      else:
        st.info("No truck dispatches completed yet.")

  # ---------------------------------------------------------
  # 5. BUYER PORTAL TAB
  # ---------------------------------------------------------
  elif tab_name == "🛒 Buyer Portal":
    with tab_ui:
      st.header("Buyer Order Tracking Portal")
      st.markdown("Check live updates on your orders and Sale Office decisions.")

      conn = get_connection()
      buyer_df = pd.read_sql(
          "SELECT po_no, buyer, qty, sale_status, loading_status, allocated_details FROM purchase_orders",
          conn,
      )
      conn.close()

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
  # 6. EDITABLE DATABASE TAB (Admin Only)
  # ---------------------------------------------------------
  elif tab_name == "🛠️ Editable Database":
    with tab_ui:
      st.header("Database Administration & Editable Tables")
      st.markdown("Directly view and edit SQLite database tables (`bulks`, `purchase_orders`, `users`).")

      table_choice = st.selectbox("Select Database Table to Edit", ["bulks", "purchase_orders", "users"])

      conn = get_connection()
      table_df = pd.read_sql(f"SELECT * FROM {table_choice}", conn)
      conn.close()

      st.markdown(f"**Editing `{table_choice}` table directly:**")
      edited_df = st.data_editor(table_df, num_rows="dynamic", use_container_width=True, key=f"editor_{table_choice}")

      if st.button("Save Changes to Database"):
        conn = get_connection()
        try:
          # Replace table content with edited dataframe
          edited_df.to_sql(table_choice, conn, if_exists="replace", index=False)
          st.success(f"Table `{table_choice}` successfully updated and saved to SQLite DB!")
          st.rerun()
        except Exception as e:
          st.error(f"Error saving changes: {e}")
        finally:
          conn.close()
