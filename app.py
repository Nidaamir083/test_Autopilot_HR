import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd
import os

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Autopilot HR", layout="wide")
if "page" not in st.session_state:
    st.session_state.page = "login"

# ---------------- STYLES ----------------
st.markdown("""
    <style>
    /* Remove Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    .logo {
        text-align: center;
        margin-bottom: 20px;
    }
    .logo img {
        width: 120px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- DB FUNCTIONS ----------------
def init_db():
    conn = sqlite3.connect("hr_system.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT,
                    last_name TEXT,
                    email TEXT,
                    phone TEXT,
                    role TEXT,
                    department TEXT,
                    hire_date TEXT,
                    salary REAL
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS leave_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    employee_id INTEGER,
                    start_date TEXT,
                    end_date TEXT,
                    reason TEXT,
                    status TEXT
                )""")
    conn.commit()
    conn.close()

def get_employees():
    conn = sqlite3.connect("hr_system.db")
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    rows = c.fetchall()
    conn.close()
    return rows

def add_leave(employee_id, start_date, end_date, reason):
    conn = sqlite3.connect("hr_system.db")
    c = conn.cursor()
    c.execute("INSERT INTO leave_requests (employee_id, start_date, end_date, reason, status) VALUES (?, ?, ?, ?, ?)",
              (employee_id, start_date, end_date, reason, "Pending"))
    conn.commit()
    conn.close()

def get_leave_requests():
    conn = sqlite3.connect("hr_system.db")
    c = conn.cursor()
    c.execute("""SELECT lr.id, e.first_name, e.last_name, lr.start_date, lr.end_date, lr.reason, lr.status
                 FROM leave_requests lr
                 JOIN employees e ON lr.employee_id = e.id""")
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# ---------------- LOGIN PAGE ----------------
if st.session_state.page == "login":
    with st.sidebar:
        st.markdown('<div class="logo"><img src="https://i.imgur.com/6RK0zvN.png"></div>', unsafe_allow_html=True)
    st.title("🔑 Login to Autopilot HR")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        if email and password:
            if email.endswith("@admin.com"):
                st.session_state.page = "admin_panel"
            else:
                st.session_state.page = "dashboard"
        else:
            st.error("Enter both email and password")

# ---------------- EMPLOYEE DASHBOARD ----------------
elif st.session_state.page == "dashboard":
    with st.sidebar:
        st.markdown('<div class="logo"><img src="https://i.imgur.com/6RK0zvN.png"></div>', unsafe_allow_html=True)
        if st.button("Logout"):
            st.session_state.page = "login"

    st.title("📊 Employee Dashboard")
    tabs = st.tabs(["💬 Chatbot", "📌 Request Leave", "✅ Status"])

    with tabs[0]:
        st.subheader("Chatbot")
        st.info("Chatbot integration goes here (Gemini/OpenAI).")

    with tabs[1]:
        st.subheader("Request Leave")
        emp_id = st.number_input("Employee ID", min_value=1)
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        reason = st.text_area("Reason")
        if st.button("Submit Leave Request"):
            add_leave(emp_id, str(start_date), str(end_date), reason)
            st.success("Leave request submitted!")

    with tabs[2]:
        st.subheader("Leave Status")
        leaves = get_leave_requests()
        if leaves:
            df = pd.DataFrame(leaves, columns=["ID", "First Name", "Last Name", "Start", "End", "Reason", "Status"])
            st.dataframe(df)
        else:
            st.info("No leave requests yet.")

# ---------------- ADMIN PANEL ----------------
elif st.session_state.page == "admin_panel":
    with st.sidebar:
        st.markdown('<div class="logo"><img src="https://i.imgur.com/6RK0zvN.png"></div>', unsafe_allow_html=True)
        menu = st.radio("📌 Admin Menu", ["Attendance", "Leave Requests", "Employee Records", "Promotions", "Reports", "QnA", "Chatbot"])
        if st.button("Logout"):
            st.session_state.page = "login"

    st.title("🛠️ Admin Panel")

    if menu == "Attendance":
        st.subheader("📅 Attendance")
        st.info("Attendance tracking feature to be implemented.")

    elif menu == "Leave Requests":
        st.subheader("📌 Leave Requests")
        leaves = get_leave_requests()
        if leaves:
            df = pd.DataFrame(leaves, columns=["ID", "First Name", "Last Name", "Start", "End", "Reason", "Status"])
            st.dataframe(df)
        else:
            st.info("No leave requests found.")

    elif menu == "Employee Records":
        st.subheader("👥 Employee Records")
        rows = get_employees()
        if rows:
            for r in rows:
                st.markdown(f"### {r[1]} {r[2]} ({r[5]} - {r[6]})")
                st.write(f"📧 {r[3]} | 📱 {r[4]} | Hired: {r[7]} | 💰 {r[8]}")
                st.divider()
        else:
            st.info("No employees yet.")

    elif menu == "Promotions":
        st.subheader("🎖️ Promotions")
        st.info("Promotion management feature to be implemented.")

    elif menu == "Reports":
        st.subheader("📊 Reports")
        st.info("Reports & analytics to be implemented.")

    elif menu == "QnA":
        st.subheader("💡 QnA")
        st.info("QnA with Gemini/OpenAI to be integrated.")

    elif menu == "Chatbot":
        st.subheader("🤖 Chatbot")
        st.info("Admin chatbot integration goes here.")
