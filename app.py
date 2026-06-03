import streamlit as st
from database import add_complaint, get_all_complaints, update_status
from utils import get_time, format_issue, is_valid_phone

st.set_page_config(page_title="Water Issue Tracker", page_icon="💧", layout="wide")

st.title("💧 Water Issue Tracker - Civic Hackathon Project")

# Sidebar menu
menu = st.sidebar.radio(
    "Menu",
    ["🏠 Home", "📢 Report Issue", "📋 View Issues", "🛠 Admin Panel"]
)

# ---------------- HOME ----------------
if menu == "🏠 Home":
    st.markdown("""
    ## 🌍 Water Issue Tracker

    Report civic water problems easily:

    - 💧 Leakage  
    - 🚱 No Water Supply  
    - 🟡 Dirty Water  
    - ⚠️ Low Pressure  

    📌 Helps municipalities respond faster.
    """)

    st.success("Built for Civic Hackathon 🚀")

# ---------------- REPORT ISSUE ----------------
elif menu == "📢 Report Issue":
    st.subheader("📢 Report Water Issue")

    name = st.text_input("Your Name")
    phone = st.text_input("Phone Number")

    issue = st.selectbox("Issue Type", [
        "Leakage", "No Water", "Dirty Water", "Low Pressure"
    ])

    location = st.text_input("Location")
    description = st.text_area("Description")

    if st.button("Submit Complaint"):

        if not name or not phone or not location:
            st.error("⚠️ Please fill all required fields")

        elif not is_valid_phone(phone):
            st.error("⚠️ Invalid phone number")

        else:
            data = {
                "Name": name,
                "Phone": phone,
                "Issue": format_issue(issue),
                "Location": location,
                "Description": description,
                "Time": get_time(),
                "Status": "Pending"
            }

            add_complaint(data)
            st.success("✅ Complaint Submitted Successfully!")

# ---------------- VIEW ISSUES ----------------
elif menu == "📋 View Issues":
    st.subheader("📋 All Reported Issues")

    df = get_all_complaints()

    if df.empty:
        st.warning("No complaints yet.")
    else:
        filter_issue = st.selectbox(
            "Filter by Issue",
            ["All", "Leakage", "No Water", "Dirty Water", "Low Pressure"]
        )

        if filter_issue != "All":
            df = df[df["Issue"].str.contains(filter_issue, na=False)]

        st.dataframe(df, use_container_width=True)

# ---------------- ADMIN PANEL ----------------
elif menu == "🛠 Admin Panel":
    st.subheader("🛠 Admin Dashboard")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":

        st.success("Logged in as Admin")

        df = get_all_complaints()
        st.dataframe(df, use_container_width=True)

        st.markdown("### Update Complaint Status")

        index = st.number_input("Enter Complaint Index", min_value=0, step=1)
        status = st.selectbox("Set Status", ["Pending", "Resolved"])

        if st.button("Update Status"):

            if update_status(index, status):
                st.success("Status Updated Successfully ✔")
            else:
                st.error("Invalid Index")

    elif password:
        st.error("Wrong Password ❌")