import streamlit as st
from database import add_complaint, get_all_complaints, update_status
from utils import get_time, format_issue, is_valid_phone

st.set_page_config(
    page_title="Water Issue Tracker",
    page_icon="💧",
    layout="wide"
)

# ---------------- HEADER ----------------
st.markdown(
    """
    <h1 style='text-align: center; color: #1f77b4;'>
    💧 Water Issue Tracker
    </h1>
    <h4 style='text-align: center; color: gray;'>
    Civic Complaint & Resolution System
    </h4>
    <hr>
    """,
    unsafe_allow_html=True
)

# ---------------- SIDEBAR ----------------
menu = st.sidebar.radio(
    "📌 Navigate",
    ["🏠 Dashboard", "📢 Report Issue", "📋 View Complaints", "🛠 Admin Panel"]
)

# ---------------- DASHBOARD ----------------
st.markdown("""
<style>
.card {
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    color: #ffffff;
    font-weight: bold;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

.card h2 {
    font-size: 32px;
    margin: 0;
}

.card p {
    font-size: 16px;
    margin: 5px 0 0 0;
    opacity: 0.9;
}

/* Strong contrast colors */
.total {
    background: linear-gradient(135deg, #1f77b4, #4da3ff);
}

.pending {
    background: linear-gradient(135deg, #ff9800, #ffb74d);
}

.resolved {
    background: linear-gradient(135deg, #2e7d32, #66bb6a);
}
</style>
""", unsafe_allow_html=True)

df = get_all_complaints()

total = len(df)
resolved = len(df[df["Status"] == "Resolved"]) if total > 0 else 0
pending = total - resolved

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="card total">
        <h2>{total}</h2>
        <p>Total Complaints</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="card pending">
        <h2>{pending}</h2>
        <p>Pending</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="card resolved">
        <h2>{resolved}</h2>
        <p>Resolved</p>
    </div>
    """, unsafe_allow_html=True)
# ---------------- REPORT ISSUE ----------------
elif menu == "📢 Report Issue":

    st.subheader("📢 Report Water Issue")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("👤 Name")
        phone = st.text_input("📞 Phone Number")

    with col2:
        issue = st.selectbox(
            "⚠️ Issue Type",
            ["Leakage", "No Water", "Dirty Water", "Low Pressure"]
        )
        location = st.text_input("📍 Location")

    description = st.text_area("📝 Description")

    if st.button("🚀 Submit Complaint"):

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

# ---------------- VIEW COMPLAINTS ----------------
elif menu == "📋 View Complaints":

    st.subheader("📋 All Complaints")

    df = get_all_complaints()

    if df.empty:
        st.warning("No complaints yet.")
    else:
        filter_issue = st.selectbox(
            "Filter Issues",
            ["All", "Leakage", "No Water", "Dirty Water", "Low Pressure"]
        )

        if filter_issue != "All":
            df = df[df["Issue"].str.contains(filter_issue)]

        st.dataframe(df, use_container_width=True)

# ---------------- ADMIN PANEL ----------------
elif menu == "🛠 Admin Panel":

    st.subheader("🛠 Admin Dashboard")

    password = st.text_input("Enter Admin Password", type="password")

    if password == "admin123":

        st.success("Admin Access Granted ✔")

        df = get_all_complaints()
        st.dataframe(df, use_container_width=True)

        index = st.number_input("Complaint Index", min_value=0, step=1)
        status = st.selectbox("Update Status", ["Pending", "Resolved"])

        if st.button("Update"):
            if update_status(index, status):
                st.success("Status Updated ✔")
            else:
                st.error("Invalid Index")

    elif password:
        st.error("Wrong Password ❌")