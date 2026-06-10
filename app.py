import os

import streamlit as st
from dotenv import load_dotenv

from database import add_complaint, get_all_complaints, update_status
from utils import format_issue, get_time, is_valid_phone


load_dotenv()


UPLOAD_FOLDER = "uploads"

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True,
)


st.set_page_config(
    page_title="Water Issue Tracker",
    page_icon="💧",
    layout="wide",
)


st.title("💧 Water Issue Tracker - Civic System")


# ---------- FUNCTIONS ----------


def save_files(files):

    paths = []

    for file in files:
        path = os.path.join(
            UPLOAD_FOLDER,
            file.name,
        )

        with open(
            path,
            "wb",
        ) as f:
            f.write(file.read())

        paths.append(path)

    return ",".join(paths)


def show_files(files):

    if not files:
        return

    for file in files.split(","):
        if not os.path.exists(file):
            continue

        ext = file.split(".")[-1].lower()

        if ext in [
            "png",
            "jpg",
            "jpeg",
        ]:
            st.image(file)

        elif ext in [
            "mp4",
            "mov",
            "avi",
        ]:
            st.video(file)

        elif ext in [
            "mp3",
            "wav",
            "m4a",
        ]:
            st.audio(file)


# ---------- MENU ----------


menu = st.sidebar.radio(
    "Menu",
    [
        "🏠 Dashboard",
        "📢 Report Issue",
        "📋 View Complaints",
        "🛠 Admin Panel",
    ],
)


# ---------- DASHBOARD ----------


if menu == "🏠 Dashboard":
    df = get_all_complaints()

    total = len(df)

    resolved = len(df[df["Status"] == "Resolved"]) if total else 0

    pending = total - resolved

    st.metric(
        "Total Complaints",
        total,
    )

    st.metric(
        "Pending",
        pending,
    )

    st.metric(
        "Resolved",
        resolved,
    )


# ---------- REPORT ----------


elif menu == "📢 Report Issue":
    st.subheader("Report Water Issue")

    name = st.text_input("Name")

    phone = st.text_input(
        "Phone",
        max_chars=10,
    )

    if phone and not phone.isdigit():
        st.error("Only numbers allowed")

        phone = ""

    issue = st.selectbox(
        "Issue",
        [
            "Leakage",
            "No Water",
            "Dirty Water",
            "Low Pressure",
        ],
    )

    location = st.text_input("Location")

    description = st.text_area("Description")

    files = st.file_uploader(
        "Upload Proof Files",
        type=[
            "png",
            "jpg",
            "jpeg",
            "mp4",
            "mov",
            "avi",
            "mp3",
            "wav",
            "m4a",
        ],
        accept_multiple_files=True,
    )

    if st.button("Submit Issue"):
        if not name or not phone or not location:
            st.error("Fill required fields")

        elif not is_valid_phone(phone):
            st.error("Invalid Phone")

        else:
            uploaded = save_files(files)

            add_complaint(
                {
                    "Name": name,
                    "Phone": phone,
                    "Issue": format_issue(issue),
                    "Location": location,
                    "Description": description,
                    "Image": uploaded,
                    "Time": get_time(),
                    "Status": "Pending",
                }
            )

            st.success("Complaint Submitted")


# ---------- VIEW ----------


elif menu == "📋 View Complaints":
    df = get_all_complaints()

    for i, row in df.iterrows():
        if row["Status"] == "Resolved":
            st.success(f"✅ {row['Issue']} - Resolved")

        else:
            st.warning(f"🟡 {row['Issue']} - Pending")

        with st.expander("View Details"):
            st.write(
                "Name:",
                row["Name"],
            )

            st.write(
                "Location:",
                row["Location"],
            )

            st.write(row["Description"])

            st.subheader("Citizen Proof")

            show_files(row["Image"])

            if row["Status"] == "Resolved":
                st.subheader("Resolution Details")

                st.write(row["Resolution"])

                show_files(row["Resolution Files"])


# ---------- ADMIN ----------


elif menu == "🛠 Admin Panel":
    password = st.text_input(
        "Admin Password",
        type="password",
    )

    if password == os.getenv(
        "ADMIN_PASSWORD",
        "admin123",
    ):
        df = get_all_complaints()

        st.dataframe(
            df,
            use_container_width=True,
        )

        index = st.number_input(
            "Complaint Index",
            min_value=0,
        )

        status = st.selectbox(
            "Status",
            [
                "Pending",
                "Resolved",
            ],
        )

        resolution = st.text_area("Resolution Details")

        proof = st.file_uploader(
            "Upload Resolution Proof",
            type=[
                "png",
                "jpg",
                "jpeg",
                "mp4",
                "mp3",
                "wav",
            ],
            accept_multiple_files=True,
        )

        if st.button("Update"):
            proof_files = save_files(proof)

            update_status(
                index,
                status,
                resolution,
                proof_files,
            )

            st.success("Updated Successfully")

    elif password:
        st.error("Wrong Password")
