import streamlit as st
import pandas as pd
from database import add_complaint, get_all_complaints, update_status
from utils import get_time, format_issue, is_valid_phone

st.set_page_config(page_title="Water Issue Tracker", page_icon="💧", layout="wide")

st.title("💧 Water Issue Tracker - Civic System")

# ---------------- MENU ----------------
menu = st.sidebar.radio(
    "Menu",
    ["🏠 Dashboard", "📢 Report Issue", "📋 View Complaints", "🛠 Admin Panel"]
)

# ---------------- DASHBOARD ----------------
if menu == "🏠 Dashboard":

    df = get_all_complaints()

    total = len(df)
    resolved = len(df[df["Status"] == "Resolved"]) if total > 0 else 0
    pending = total - resolved

    st.metric("Total Complaints", total)
    st.metric("Pending", pending)
    st.metric("Resolved", resolved)

# ---------------- REPORT ISSUE ----------------
elif menu == "📢 Report Issue":

    st.subheader("📢 Report Water Issue")

    name = st.text_input("Name")
    phone = st.text_input("Phone")

    issue = st.selectbox(
        "Issue Type",
        ["Leakage", "No Water", "Dirty Water", "Low Pressure"]
    )

    location = st.text_input("Location")
    description = st.text_area("Description")

    # 🆕 IMAGE UPLOAD (OPTIONAL)
    image = st.file_uploader("Upload Image (Optional)", type=["png", "jpg", "jpeg"])

    if st.button("Submit Issue"):

        if not name or not phone or not location:
            st.error("Please fill required fields")

        elif not is_valid_phone(phone):
            st.error("Invalid phone number")

        else:
            image_path = ""

            if image is not None:
                image_path = image.name
                with open(image_path, "wb") as f:
                    f.write(image.read())

            data = {
                "Name": name,
                "Phone": phone,
                "Issue": format_issue(issue),
                "Location": location,
                "Description": description,
                "Image": image_path,
                "Time": get_time(),
                "Status": "Pending",
                "Resolution": ""
            }

            add_complaint(data)
            st.success("Issue Submitted Successfully!")

# ---------------- VIEW COMPLAINTS ----------------
elif menu == "📋 View Complaints":

    df = get_all_complaints()

    st.subheader("All Complaints")

    if df.empty:
        st.warning("No complaints yet")
    else:
        st.dataframe(df, use_container_width=True)

# ---------------- ADMIN PANEL ----------------
elif menu == "🛠 Admin Panel":

    st.subheader("Admin Dashboard")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":

        df = get_all_complaints()
        st.dataframe(df, use_container_width=True)

        st.subheader("Update Complaint")

        index = st.number_input("Complaint Index", min_value=0)

        status = st.selectbox("Status", ["Pending", "Resolved"])

        resolution = st.text_area("How was it resolved? (Write details)")

        if st.button("Update Complaint"):

            if update_status(index, status, resolution):
                st.success("Updated Successfully ✔")
            else:
                st.error("Invalid Index")

    elif password:
        st.error("Wrong Password")
