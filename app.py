import os

import folium
import folium.plugins
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium

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
        "map": "🗺 Complaint Map",
        "status_filter": "Status Filter",
        "issue_filter": "Issue Filter",
        "all": "All",
        "mapped": "Total Complaints Mapped",
        "no_complaints_map": "No complaints available for mapping.",
        "no_locations": "No valid locations could be plotted.",
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
        "map": "🗺 ఫిర్యాదు మ్యాప్",
        "status_filter": "స్థితి ఫిల్టర్",
        "issue_filter": "సమస్య ఫిల్టర్",
        "all": "అన్ని",
        "mapped": "మొత్తం ఫిర్యాదులు మ్యాప్ చేయబడ్డాయి",
        "no_complaints_map": "మ్యాపింగ్ కోసం ఫిర్యాదులు లేవు.",
        "no_locations": "చెల్లని స్థానాలు కనిపించవు.",
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
        "map": "🗺 शिकायत मानचित्र",
        "status_filter": "स्थिति फ़िल्टर",
        "issue_filter": "समस्या फ़िल्टर",
        "all": "सभी",
        "mapped": "कुल मानचित्रित शिकायतें",
        "no_complaints_map": "मानचित्रण के लिए कोई शिकायत उपलब्ध नहीं है।",
        "no_locations": "कोई वैध स्थान नहीं मिल सका।",
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
        "map": "🗺 புகார் வரைபடம்",
        "status_filter": "நிலை வடிகாணம்",
        "issue_filter": "சிக்கல் வடிகாணம்",
        "all": "அனைத்து",
        "mapped": "மொத்த வரைபடிக்கப்பட்ட புகார்கள்",
        "no_complaints_map": "வரைபடிக்கப்படுத்தப்பட்ட புகார்கள் இல்லை.",
        "no_locations": "சரியான இடங்கள் கண்டபடி கிடையாது.",
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
            "map": "🗺 ದೂರು ಮ್ಯಾಪ್",
            "status_filter": "ಸ್ಥಿತಿ ಫಿಲ್ತರ್",
            "issue_filter": "ಸಮಸ್ಯೆ ಫಿಲ್ತರ್",
            "all": "ಎಲ್ಲಾ",
            "mapped": "ಮೊತ್ತದ ಮ್ಯಾಪ್ ಮಾಡಿದ ದೂರುಗಳು",
            "no_complaints_map": "ಮ್ಯಾಪ್ ಮಾಡಲು ಕೋಈಕೂಡಿಸ ದೂರುಗಳು ಇಲ್ಲ.",
            "no_locations": "ಯಥವತ್ತಾದ ಸ್ಥಳಗಳು ಕಂಡುಹಿಡಿಯಲಿಲ್ಲ.",
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
            "map": "🗺 പരാതി മാപ്പ്",
            "status_filter": "സ്ഥിതി ഫിൽറ്റർ",
            "issue_filter": "പ്രശ്നം ഫിൽറ്റർ",
            "all": "എല്ലാം",
            "mapped": "മൊത്തം മാപ്പ് ചെയ്ത പരാതികൾ",
            "no_complaints_map": "മാപ്പിംഗിനായി പരാതികള്‍ ഇല്ല.",
            "no_locations": "യഥാർത്ഥമായ സ്ഥലങ്ങള്‍ കണ്ടെത്തുന്നില്ല.",
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
            "map": "🗺 तक्रारीचा नकाशा",
            "status_filter": "स्थिती फिल्टर",
            "issue_filter": "समस्या फिल्टर",
            "all": "सर्व",
            "mapped": "एकूण नकाशेमध्ये जुडवलेल्या तक्रारी",
            "no_complaints_map": "नकाशासाठी कोणत्याही तक्रारी उपलब्ध नाहीत.",
            "no_locations": "कोणतेही वैध स्थान सापेक्ष आहेत.",
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
            "map": "🗺 অভিযোগ মানচিত্র",
            "status_filter": "স্থিতি ফিল্টার",
            "issue_filter": "সমস্যা ফিল্টার",
            "all": "সব",
            "mapped": "মোট ম্যাপ করা অভিযোগ",
            "no_complaints_map": "ম্যাপ করার জন্য কোন অভিযোগ নেই।",
            "no_locations": "কোনো বৈধ অবস্থান পাওয়া যায়নি।",
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
            "map": "🗺 પક્ષ પર જાહેર કરો",
            "status_filter": "સ્થિતિ ફિલ્ટર",
            "issue_filter": "સમસ્યા ફિલ્ટર",
            "all": "બધા",
            "mapped": "કુલ પક્ષ પર જાહેર કરેલી ફરિયાદો",
            "no_complaints_map": "માપવા માટે કોઈ ફરિયાદો ઉપલબ્ધ નથા.",
            "no_locations": "કોઈ કાયદેસર સ્થાન મલ્યા નથ્યા.",
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
            "map": "🗺 ਪਕਿਸ਼ਾ ਦਾ ਨਕਸ਼ਾ",
            "status_filter": "ਹੁਕਮ ਦਾ ਫਿਲਟਰ",
            "issue_filter": "ਮੁਸ਼ਕਿਲ ਦਾ ਫਿਲਟਰ",
            "all": "ਸਭ",
            "mapped": "ਕੁੱਲ ਮੈਪ ਕੀਤੀਆਂ ਸ਼ਿਕਾਇਤਾਂ",
            "no_complaints_map": "ਮੈਪ ਲਈ ਕੋਈ ਸ਼ਿਕਾਇਤ ਨਹੀਂ।",
            "no_locations": "ਕੋਈ ਵੈਧ ਸਥਾਨ ਨਹੀਂ ਮਿਲਿਆ.",
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
        T["map"],
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


# ---------- COMPLAINT MAP ----------


elif menu == T["map"]:
    st.subheader(T["map"])

    @st.cache_data(ttl=3600)
    def geocode_location(location):
        geolocator = Nominatim(user_agent="water_tracker_map")
        try:
            location_data = geolocator.geocode(location)
            if location_data:
                return (location_data.latitude, location_data.longitude)
        except Exception:
            pass
        return None

    df = get_all_complaints()

    if df.empty:
        st.info(T["no_complaints_map"])
    else:
        status_filter = st.selectbox(
            T["status_filter"],
            [T["all"], T["pending"], T["resolved"]],
        )

        issue_filter = st.selectbox(
            T["issue_filter"],
            [
                T["all"],
                "💧 Leakage",
                "🚱 No Water",
                "🟡 Dirty Water",
                "⚠️ Low Pressure",
            ],
        )

        filtered_df = df.copy()

        if status_filter == T["pending"]:
            filtered_df = filtered_df[filtered_df["Status"] == "Pending"]
        elif status_filter == T["resolved"]:
            filtered_df = filtered_df[filtered_df["Status"] == "Resolved"]

        if issue_filter != T["all"]:
            clean_issue = issue_filter.split(" ", 1)[1] if " " in issue_filter else issue_filter
            filtered_df = filtered_df[
                filtered_df["Issue"].str.contains(clean_issue, case=False, na=False)
            ]

        total_mapped = len(filtered_df)
        pending_mapped = len(filtered_df[filtered_df["Status"] == "Pending"])
        resolved_mapped = len(filtered_df[filtered_df["Status"] == "Resolved"])

        col1, col2, col3 = st.columns(3)
        col1.metric(T["mapped"], total_mapped)
        col2.metric(T["pending"], pending_mapped)
        col3.metric(T["resolved"], resolved_mapped)

        if total_mapped == 0:
            st.info(T["no_complaints_map"])
        else:
            m = folium.Map(
                location=[20.5937, 78.9629],
                zoom_start=5,
            )

            valid_coords = []
            marker_cluster = folium.plugins.MarkerCluster().add_to(m)

            for _, row in filtered_df.iterrows():
                coords = geocode_location(row["Location"])
                if coords:
                    valid_coords.append(coords)
                    status_color = (
                        "orange"
                        if row["Status"] == "Pending"
                        else "green"
                        if row["Status"] == "Resolved"
                        else "blue"
                    )

                    popup_html = f"""
                    <b>Tracking ID:</b> {row['ID']}<br>
                    <b>Citizen Name:</b> {row['Name']}<br>
                    <b>Issue Type:</b> {row['Issue']}<br>
                    <b>Status:</b> {row['Status']}<br>
                    <b>Location:</b> {row['Location']}<br>
                    <b>Reported Time:</b> {row['Time']}
                    """

                    folium.Marker(
                        location=coords,
                        icon=folium.Icon(color=status_color),
                        popup=folium.Popup(popup_html, max_width=300),
                    ).add_to(marker_cluster)

            if valid_coords:
                m.fit_bounds(valid_coords, max_zoom=8, padding=(30, 30))

            st_folium(m, width="100%", height=600)

            if not valid_coords and total_mapped > 0:
                st.info(T["no_locations"])


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
