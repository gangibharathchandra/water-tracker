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


# ---------- LANGUAGE DATA ----------


LANG = {
    "English": {
        "title": "💧 Water Issue Tracker - Civic System",
        "menu": "Menu",
        "dashboard": "🏠 Dashboard",
        "report": "📢 Report Issue",
        "view": "📋 View Complaints",
        "admin": "🛠 Admin Panel",
        "total": "Total Complaints",
        "pending": "Pending",
        "resolved": "Resolved",
        "report_title": "Report Water Issue",
        "name": "Name",
        "phone": "Phone",
        "issue": "Issue",
        "location": "Location",
        "description": "Description",
        "upload": "Upload Proof Files",
        "submit": "Submit Issue",
        "success": "Complaint Submitted",
        "details": "View Details",
        "citizen": "Citizen Proof",
        "admin_login": "Admin Login",
        "password": "Admin Password",
        "update": "Update Complaint",
        "wrong": "Wrong Password",
    },
    "తెలుగు": {
        "title": "💧 నీటి సమస్య ట్రాకర్",
        "menu": "మెనూ",
        "dashboard": "🏠 డాష్‌బోర్డ్",
        "report": "📢 సమస్య తెలియజేయండి",
        "view": "📋 ఫిర్యాదులు చూడండి",
        "admin": "🛠 అడ్మిన్",
        "total": "మొత్తం ఫిర్యాదులు",
        "pending": "పెండింగ్",
        "resolved": "పరిష్కరించబడింది",
        "report_title": "నీటి సమస్య తెలియజేయండి",
        "name": "పేరు",
        "phone": "ఫోన్",
        "issue": "సమస్య",
        "location": "ప్రదేశం",
        "description": "వివరణ",
        "upload": "ఫైల్స్ అప్లోడ్ చేయండి",
        "submit": "సమర్పించండి",
        "success": "ఫిర్యాదు నమోదు అయింది",
        "details": "వివరాలు చూడండి",
        "citizen": "ఆధార ఫైల్స్",
        "admin_login": "అడ్మిన్ లాగిన్",
        "password": "పాస్వర్డ్",
        "update": "అప్డేట్ చేయండి",
        "wrong": "తప్పు పాస్వర్డ్",
    },
    "हिन्दी": {
        "title": "💧 जल समस्या ट्रैकर",
        "menu": "मेनू",
        "dashboard": "🏠 डैशबोर्ड",
        "report": "📢 शिकायत दर्ज करें",
        "view": "📋 शिकायतें देखें",
        "admin": "🛠 एडमिन",
        "total": "कुल शिकायतें",
        "pending": "बाकी",
        "resolved": "हल किया गया",
        "report_title": "जल समस्या दर्ज करें",
        "name": "नाम",
        "phone": "फोन",
        "issue": "समस्या",
        "location": "स्थान",
        "description": "विवरण",
        "upload": "फाइल अपलोड करें",
        "submit": "जमा करें",
        "success": "शिकायत दर्ज हुई",
        "details": "विवरण देखें",
        "citizen": "प्रमाण फाइल",
        "admin_login": "एडमिन लॉगिन",
        "password": "पासवर्ड",
        "update": "अपडेट करें",
        "wrong": "गलत पासवर्ड",
    },
    "தமிழ்": {
        "title": "💧 நீர் பிரச்சனை கண்காணிப்பு",
        "menu": "மெனு",
        "dashboard": "🏠 முகப்பு",
        "report": "📢 புகார் அளிக்க",
        "view": "📋 புகார்கள்",
        "admin": "🛠 நிர்வாகி",
        "total": "மொத்த புகார்கள்",
        "pending": "நிலுவை",
        "resolved": "தீர்க்கப்பட்டது",
        "report_title": "நீர் பிரச்சனை பதிவு",
        "name": "பெயர்",
        "phone": "தொலைபேசி",
        "issue": "பிரச்சனை",
        "location": "இடம்",
        "description": "விளக்கம்",
        "upload": "கோப்பு பதிவேற்றம்",
        "submit": "சமர்ப்பிக்க",
        "success": "புகார் பதிவு செய்யப்பட்டது",
        "details": "விவரம்",
        "citizen": "ஆதாரம்",
        "admin_login": "நிர்வாகி உள்நுழைவு",
        "password": "கடவுச்சொல்",
        "update": "புதுப்பி",
        "wrong": "தவறான கடவுச்சொல்",
    },
}
# ---------- ADD MORE LANGUAGES ----------


LANG.update(
    {
        "ಕನ್ನಡ": {
            "title": "💧 ನೀರಿನ ಸಮಸ್ಯೆ ಟ್ರ್ಯಾಕರ್",
            "menu": "ಮೆನು",
            "dashboard": "🏠 ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
            "report": "📢 ದೂರು ನೀಡಿ",
            "view": "📋 ದೂರುಗಳು",
            "admin": "🛠 ನಿರ್ವಾಹಕ",
            "total": "ಒಟ್ಟು ದೂರುಗಳು",
            "pending": "ಬಾಕಿ",
            "resolved": "ಪರಿಹರಿಸಲಾಗಿದೆ",
            "report_title": "ನೀರಿನ ಸಮಸ್ಯೆ ತಿಳಿಸಿ",
            "name": "ಹೆಸರು",
            "phone": "ಫೋನ್",
            "issue": "ಸಮಸ್ಯೆ",
            "location": "ಸ್ಥಳ",
            "description": "ವಿವರಣೆ",
            "upload": "ಫೈಲ್ ಅಪ್ಲೋಡ್",
            "submit": "ಸಲ್ಲಿಸಿ",
            "success": "ದೂರು ದಾಖಲಾಗಿದೆ",
            "details": "ವಿವರ ನೋಡಿ",
            "citizen": "ಪುರಾವೆ",
            "admin_login": "ನಿರ್ವಾಹಕ ಲಾಗಿನ್",
            "password": "ಪಾಸ್‌ವರ್ಡ್",
            "update": "ನವೀಕರಿಸಿ",
            "wrong": "ತಪ್ಪು ಪಾಸ್‌ವರ್ಡ್",
        },
        "മലയാളം": {
            "title": "💧 ജല പ്രശ്ന ട്രാക്കർ",
            "menu": "മെനു",
            "dashboard": "🏠 ഡാഷ്ബോർഡ്",
            "report": "📢 പരാതി നൽകുക",
            "view": "📋 പരാതികൾ",
            "admin": "🛠 അഡ്മിൻ",
            "total": "മൊത്തം പരാതികൾ",
            "pending": "ബാക്കി",
            "resolved": "പരിഹരിച്ചു",
            "report_title": "ജല പ്രശ്നം അറിയിക്കുക",
            "name": "പേര്",
            "phone": "ഫോൺ",
            "issue": "പ്രശ്നം",
            "location": "സ്ഥലം",
            "description": "വിവരണം",
            "upload": "ഫയൽ അപ്ലോഡ്",
            "submit": "സമർപ്പിക്കുക",
            "success": "പരാതി രജിസ്റ്റർ ചെയ്തു",
            "details": "വിശദാംശങ്ങൾ",
            "citizen": "തെളിവ്",
            "admin_login": "അഡ്മിൻ ലോഗിൻ",
            "password": "പാസ്‌വേഡ്",
            "update": "അപ്ഡേറ്റ്",
            "wrong": "തെറ്റായ പാസ്‌വേഡ്",
        },
        "मराठी": {
            "title": "💧 पाणी समस्या ट्रॅकर",
            "menu": "मेनू",
            "dashboard": "🏠 डॅशबोर्ड",
            "report": "📢 तक्रार करा",
            "view": "📋 तक्रारी",
            "admin": "🛠 प्रशासक",
            "total": "एकूण तक्रारी",
            "pending": "प्रलंबित",
            "resolved": "सोडवले",
            "report_title": "पाणी समस्या नोंदवा",
            "name": "नाव",
            "phone": "फोन",
            "issue": "समस्या",
            "location": "स्थान",
            "description": "वर्णन",
            "upload": "फाइल अपलोड",
            "submit": "सबमिट",
            "success": "तक्रार नोंदली",
            "details": "तपशील",
            "citizen": "पुरावा",
            "admin_login": "प्रशासक लॉगिन",
            "password": "पासवर्ड",
            "update": "अपडेट",
            "wrong": "चुकीचा पासवर्ड",
        },
        "বাংলা": {
            "title": "💧 জল সমস্যা ট্র্যাকার",
            "menu": "মেনু",
            "dashboard": "🏠 ড্যাশবোর্ড",
            "report": "📢 অভিযোগ করুন",
            "view": "📋 অভিযোগসমূহ",
            "admin": "🛠 অ্যাডমিন",
            "total": "মোট অভিযোগ",
            "pending": "অপেক্ষমান",
            "resolved": "সমাধান হয়েছে",
            "report_title": "জল সমস্যা জানান",
            "name": "নাম",
            "phone": "ফোন",
            "issue": "সমস্যা",
            "location": "অবস্থান",
            "description": "বিবরণ",
            "upload": "ফাইল আপলোড",
            "submit": "জমা দিন",
            "success": "অভিযোগ জমা হয়েছে",
            "details": "বিস্তারিত",
            "citizen": "প্রমাণ",
            "admin_login": "অ্যাডমিন লগইন",
            "password": "পাসওয়ার্ড",
            "update": "আপডেট",
            "wrong": "ভুল পাসওয়ার্ড",
        },
        "ગુજરાતી": {
            "title": "💧 પાણી સમસ્યા ટ્રેકર",
            "menu": "મેનુ",
            "dashboard": "🏠 ડેશબોર્ડ",
            "report": "📢 ફરિયાદ કરો",
            "view": "📋 ફરિયાદો",
            "admin": "🛠 એડમિન",
            "total": "કુલ ફરિયાદો",
            "pending": "બાકી",
            "resolved": "ઉકેલાયું",
            "report_title": "પાણી સમસ્યા નોંધાવો",
            "name": "નામ",
            "phone": "ફોન",
            "issue": "સમસ્યા",
            "location": "સ્થળ",
            "description": "વર્ણન",
            "upload": "ફાઇલ અપલોડ",
            "submit": "સબમિટ",
            "success": "ફરિયાદ નોંધાઈ",
            "details": "વિગતો",
            "citizen": "પુરાવો",
            "admin_login": "એડમિન લોગિન",
            "password": "પાસવર્ડ",
            "update": "અપડેટ",
            "wrong": "ખોટો પાસવર્ડ",
        },
        "ਪੰਜਾਬੀ": {
            "title": "💧 ਪਾਣੀ ਸਮੱਸਿਆ ਟਰੈਕਰ",
            "menu": "ਮੇਨੂ",
            "dashboard": "🏠 ਡੈਸ਼ਬੋਰਡ",
            "report": "📢 ਸ਼ਿਕਾਇਤ ਕਰੋ",
            "view": "📋 ਸ਼ਿਕਾਇਤਾਂ",
            "admin": "🛠 ਐਡਮਿਨ",
            "total": "ਕੁੱਲ ਸ਼ਿਕਾਇਤਾਂ",
            "pending": "ਬਾਕੀ",
            "resolved": "ਹੱਲ ਹੋਇਆ",
            "report_title": "ਪਾਣੀ ਸਮੱਸਿਆ ਦਰਜ ਕਰੋ",
            "name": "ਨਾਮ",
            "phone": "ਫੋਨ",
            "issue": "ਸਮੱਸਿਆ",
            "location": "ਸਥਾਨ",
            "description": "ਵੇਰਵਾ",
            "upload": "ਫਾਈਲ ਅੱਪਲੋਡ",
            "submit": "ਜਮ੍ਹਾਂ ਕਰੋ",
            "success": "ਸ਼ਿਕਾਇਤ ਦਰਜ ਹੋਈ",
            "details": "ਵੇਰਵੇ",
            "citizen": "ਸਬੂਤ",
            "admin_login": "ਐਡਮਿਨ ਲਾਗਇਨ",
            "password": "ਪਾਸਵਰਡ",
            "update": "ਅੱਪਡੇਟ",
            "wrong": "ਗਲਤ ਪਾਸਵਰਡ",
        },
    }
)


# ---------- LANGUAGE SWITCH UI ----------


st.markdown(
    """
<style>

div[data-testid="stSelectbox"]:first-of-type{

position:fixed;
right:20px;
bottom:20px;
width:180px;
z-index:99999;

}

</style>
""",
    unsafe_allow_html=True,
)


language = st.selectbox(
    "🌐 Language",
    list(LANG.keys()),
)


T = LANG[language]


st.title(T["title"])
# ---------- FILE FUNCTIONS ----------


def save_files(files):

    paths = []

    if not files:
        return ""

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
    T["menu"],
    [
        T["dashboard"],
        T["report"],
        T["view"],
        T["admin"],
    ],
)


# ---------- DASHBOARD ----------


if menu == T["dashboard"]:
    df = get_all_complaints()

    total = len(df)

    resolved = len(df[df["Status"] == "Resolved"]) if total else 0

    pending = total - resolved

    st.metric(
        T["total"],
        total,
    )

    st.metric(
        T["pending"],
        pending,
    )

    st.metric(
        T["resolved"],
        resolved,
    )


# ---------- REPORT ISSUE ----------


elif menu == T["report"]:
    st.subheader(T["report_title"])

    name = st.text_input(T["name"])

    phone = st.text_input(
        T["phone"],
        max_chars=10,
    )

    issue = st.selectbox(
        T["issue"],
        [
            "Leakage",
            "No Water",
            "Dirty Water",
            "Low Pressure",
        ],
    )

    location = st.text_input(T["location"])

    description = st.text_area(T["description"])

    files = st.file_uploader(
        T["upload"],
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

    if st.button(T["submit"]):
        if not name or not phone or not location:
            st.error("⚠ Required fields missing")

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

            st.success(T["success"])


# ---------- VIEW COMPLAINTS ----------


elif menu == T["view"]:
    df = get_all_complaints()

    if df.empty:
        st.warning("No complaints available")

    for _, row in df.iterrows():
        if row["Status"] == "Resolved":
            st.success(f"✅ {row['Issue']} - {T['resolved']}")

        else:
            st.error(f"🔴 {row['Issue']} - {T['pending']}")

        with st.expander(T["details"]):
            st.write(
                T["name"],
                ":",
                row["Name"],
            )

            st.write(
                T["phone"],
                ":",
                row["Phone"],
            )

            st.write(
                T["issue"],
                ":",
                row["Issue"],
            )

            st.write(
                T["location"],
                ":",
                row["Location"],
            )

            st.write(
                T["description"],
                ":",
                row["Description"],
            )

            st.subheader(T["citizen"])

            show_files(row["Image"])

            if row["Status"] == "Resolved":
                st.success("✔ Problem Solved")

                st.subheader("Resolution Details")

                st.write(row["Resolution"])

                st.subheader("Resolution Proof")

                show_files(row["Resolution Files"])


# ---------- ADMIN PANEL ----------


elif menu == T["admin"]:
    st.subheader(T["admin_login"])

    password = st.text_input(
        T["password"],
        type="password",
    )

    if password == os.getenv(
        "ADMIN_PASSWORD",
        "admin123",
    ):
        st.success("Admin Login Successful")

        df = get_all_complaints()

        st.dataframe(
            df,
            use_container_width=True,
        )

        st.subheader("Update Complaint Status")

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
                "mov",
                "avi",
                "mp3",
                "wav",
                "m4a",
            ],
            accept_multiple_files=True,
        )

        if st.button(T["update"]):
            proof_files = save_files(proof)

            updated = update_status(
                index,
                status,
                resolution,
                proof_files,
            )

            if updated:
                st.success("Complaint Updated Successfully ✔")

            else:
                st.error("Invalid Complaint Index")

    elif password:
        st.error(T["wrong"])

## ---------- ADMIN PANEL ----------


elif menu == T["admin"]:
    st.subheader(T["admin_login"])

    password = st.text_input(
        T["password"],
        type="password",
    )

    if password == os.getenv(
        "ADMIN_PASSWORD",
        "admin123",
    ):
        st.success("Admin Login Successful")

        df = get_all_complaints()

        st.dataframe(
            df,
            use_container_width=True,
        )

        st.subheader("Update Complaint Status")

        if not df.empty:
            index = st.number_input(
                "Complaint Index",
                min_value=0,
                max_value=len(df) - 1,
            )

            selected = df.iloc[index]

            st.write(
                "Selected Issue:",
                selected["Issue"],
            )

            st.write(
                "Current Status:",
                selected["Status"],
            )

            status = st.selectbox(
                "Change Status",
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
                    "mov",
                    "avi",
                    "mp3",
                    "wav",
                    "m4a",
                ],
                accept_multiple_files=True,
            )

            if st.button(T["update"]):
                proof_files = save_files(proof)

                updated = update_status(
                    index,
                    status,
                    resolution,
                    proof_files,
                )

                if updated:
                    st.success("Complaint Status Updated ✔")

                    st.rerun()

                else:
                    st.error("Invalid Complaint Index")

        else:
            st.warning("No complaints available")

    elif password:
        st.error(T["wrong"])
