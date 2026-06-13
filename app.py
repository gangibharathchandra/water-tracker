import os

import streamlit as st

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        return False

from ai_service import (
    _chat_json,
    analyze_complaint_byok,
    analyze_complaint_local,
    analyze_admin_solution,
    analyze_admin_solution_local,
    ask_admin_ollama,
    ask_help_desk,
    ask_help_desk_local,
    generate_status_update,
    verify_final_resolution,
)
from database import add_complaint, get_all_complaints, update_status
from languages import LANG
from utils import format_issue, get_time, is_valid_phone


load_dotenv()


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


st.set_page_config(page_title="Water Issue Tracker", page_icon="\U0001f4a7", layout="wide")

language = st.sidebar.selectbox("\U0001f310 Language", list(LANG.keys()), index=0, key="language_selector")
T = LANG.get(language, LANG["English"])

st.title(T["title"])

# ---------- GLOBAL DARK MODE FIX CSS ----------
st.markdown(
    """
    <style>
    :root {
        --bg-primary: #f8fbff;
        --bg-card: rgba(255, 255, 255, 0.76);
        --text-primary: #1e293b;
        --text-secondary: #334155;
        --border-color: rgba(15, 23, 42, 0.08);
        --sidebar-bg: linear-gradient(180deg, #0f172a 0%, #164e63 100%);
        --metric-bg: rgba(255, 255, 255, 0.72);
        --chat-user-bg: #dcfce7;
        --chat-user-text: #166534;
        --chat-ai-bg: #e0f2fe;
        --chat-ai-text: #075985;
        --ai-card-bg: rgba(255, 255, 255, 0.76);
        --badge-bg: #0891b2;
        --badge-text: #ffffff;
        --input-bg: #ffffff;
        --input-text: #1e293b;
        --button-bg: #0891b2;
        --button-text: #ffffff;
        --success-bg: #dcfce7;
        --success-text: #166534;
        --error-bg: #fee2e2;
        --error-text: #991b1b;
        --info-bg: #e0f2fe;
        --info-text: #075985;
        --warning-bg: #fef3c7;
        --warning-text: #92400e;
        --table-header-bg: #f1f5f9;
        --table-header-text: #1e293b;
        --table-row-bg: #ffffff;
        --table-row-text: #1e293b;
        --table-alt-bg: #f8fafc;
        --expander-bg: #f8fafc;
        --expander-text: #1e293b;
    }

    /* Dark mode detection via data-theme */
    .stApp[data-theme="dark"],
    .stApp:has([data-testid="stAppViewContainer"] .st-emotion-cache-1v7f65g) {
        --bg-primary: #0f172a !important;
        --bg-card: rgba(30, 41, 59, 0.85) !important;
        --text-primary: #f1f5f9 !important;
        --text-secondary: #cbd5e1 !important;
        --border-color: rgba(148, 163, 184, 0.12) !important;
        --metric-bg: rgba(30, 41, 59, 0.8) !important;
        --chat-user-bg: #14532d !important;
        --chat-user-text: #bbf7d0 !important;
        --chat-ai-bg: #1e3a5f !important;
        --chat-ai-text: #bae6fd !important;
        --ai-card-bg: rgba(30, 41, 59, 0.85) !important;
        --input-bg: #1e293b !important;
        --input-text: #f1f5f9 !important;
        --button-bg: #0e7490 !important;
        --button-text: #ffffff !important;
        --success-bg: #14532d !important;
        --success-text: #bbf7d0 !important;
        --error-bg: #7f1d1d !important;
        --error-text: #fca5a5 !important;
        --info-bg: #1e3a5f !important;
        --info-text: #bae6fd !important;
        --warning-bg: #78350f !important;
        --warning-text: #fde68a !important;
        --table-header-bg: #1e293b !important;
        --table-header-text: #f1f5f9 !important;
        --table-row-bg: #1e293b !important;
        --table-row-text: #e2e8f0 !important;
        --table-alt-bg: #334155 !important;
        --expander-bg: #1e293b !important;
        --expander-text: #e2e8f0 !important;
    }

    .stApp {
        background: radial-gradient(circle at top left, rgba(52, 211, 153, 0.18), transparent 32rem),
                    linear-gradient(135deg, var(--bg-primary) 0%, #eef7f4 52%, #fffaf0 100%);
        color: var(--text-primary);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #164e63 100%);
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    h1, h2, h3, h4, h5, h6, p, span, div, label, .stMarkdown, .stText {
        color: var(--text-primary);
    }

    div[data-testid="stMetric"] {
        background: var(--metric-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 14px 35px rgba(15, 23, 42, 0.08);
        backdrop-filter: blur(10px);
    }
    div[data-testid="stMetric"] label,
    div[data-testid="stMetric"] .stMetricLabel {
        color: var(--text-secondary) !important;
    }
    div[data-testid="stMetric"] .stMetricValue {
        color: var(--text-primary) !important;
    }

    .stTextInput input, .stTextArea textarea, .stSelectbox select {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
        border-color: var(--border-color) !important;
    }

    .stButton button {
        background: var(--button-bg) !important;
        color: var(--button-text) !important;
        border: none !important;
    }
    .stButton button:hover {
        opacity: 0.9;
    }

    .stSuccess {
        background-color: var(--success-bg) !important;
        color: var(--success-text) !important;
    }
    .stError {
        background-color: var(--error-bg) !important;
        color: var(--error-text) !important;
    }
    .stInfo {
        background-color: var(--info-bg) !important;
        color: var(--info-text) !important;
    }
    .stWarning {
        background-color: var(--warning-bg) !important;
        color: var(--warning-text) !important;
    }

    .streamlit-expanderHeader {
        background-color: var(--expander-bg) !important;
        color: var(--expander-text) !important;
    }

    .stDataFrame table {
        background: var(--table-row-bg) !important;
        color: var(--table-row-text) !important;
    }
    .stDataFrame thead tr th {
        background: var(--table-header-bg) !important;
        color: var(--table-header-text) !important;
    }
    .stDataFrame tbody tr:nth-child(even) {
        background: var(--table-alt-bg) !important;
    }
    .stDataFrame tbody tr:nth-child(odd) {
        background: var(--table-row-bg) !important;
    }

    .stSlider label, .stRadio label {
        color: var(--text-secondary) !important;
    }

    .stNumberInput input {
        background-color: var(--input-bg) !important;
        color: var(--input-text) !important;
    }

    .stFileUploader {
        color: var(--text-primary) !important;
    }

    .ai-card {
        background: var(--ai-card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin: 0.75rem 0;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.10);
        backdrop-filter: blur(12px);
    }
    .ai-thinking {
        display: inline-block;
        animation: pulseGlow 1.4s infinite ease-in-out;
        color: var(--text-primary);
    }
    .floating-ai {
        position: fixed;
        right: 1.25rem;
        bottom: 1.25rem;
        z-index: 999;
        width: 3.2rem;
        height: 3.2rem;
        border-radius: 999px;
        display: grid;
        place-items: center;
        background: var(--badge-bg);
        color: var(--badge-text);
        font-size: 1.4rem;
        box-shadow: 0 14px 30px rgba(8, 145, 178, 0.32);
        animation: pulseGlow 1.8s infinite ease-in-out;
    }
    @keyframes pulseGlow {
        0%, 100% { transform: scale(1); opacity: 1; }
        50% { transform: scale(1.04); opacity: 0.82; }
    }

    .chat-bubble-user {
        background: var(--chat-user-bg);
        color: var(--chat-user-text);
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 4px 18px;
        margin: 0.4rem 0;
        max-width: 80%;
        margin-left: auto;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }
    .chat-bubble-ai {
        background: var(--chat-ai-bg);
        color: var(--chat-ai-text);
        padding: 0.75rem 1rem;
        border-radius: 18px 18px 18px 4px;
        margin: 0.4rem 0;
        max-width: 80%;
        margin-right: auto;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        word-wrap: break-word;
    }
    .chat-container {
        max-height: 480px;
        overflow-y: auto;
        padding: 0.5rem;
        border: 1px solid var(--border-color);
        border-radius: 12px;
        background: var(--bg-card);
        margin: 0.75rem 0;
    }
    .chat-avatar-user {
        display: inline-block;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #10b981;
        color: white;
        text-align: center;
        line-height: 28px;
        font-size: 14px;
        margin-right: 6px;
        vertical-align: middle;
    }
    .chat-avatar-ai {
        display: inline-block;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        background: #0891b2;
        color: white;
        text-align: center;
        line-height: 28px;
        font-size: 14px;
        margin-right: 6px;
        vertical-align: middle;
    }
    .chat-timestamp {
        font-size: 0.7rem;
        opacity: 0.6;
        margin-top: 2px;
    }

    .ai-loading-dots::after {
        content: '...';
        animation: dots 1.5s steps(4, end) infinite;
    }
    @keyframes dots {
        0% { content: ''; }
        25% { content: '.'; }
        50% { content: '..'; }
        75% { content: '...'; }
    }

    .groq-link {
        display: inline-block;
        margin-top: 0.25rem;
        font-size: 0.85rem;
    }
    .groq-link a {
        color: #0891b2 !important;
        text-decoration: underline;
        font-weight: 500;
    }
    .groq-link a:hover {
        color: #0e7490 !important;
    }

    .json-result {
        background: var(--ai-card-bg);
        border: 1px solid var(--border-color);
        border-radius: 10px;
        padding: 1.2rem;
        margin: 0.75rem 0;
        box-shadow: 0 18px 45px rgba(15, 23, 42, 0.10);
    }
    .json-result table {
        width: 100%;
        border-collapse: collapse;
    }
    .json-result td {
        padding: 0.5rem 0.75rem;
        border-bottom: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    .json-result td:first-child {
        font-weight: 600;
        color: var(--text-secondary);
        width: 200px;
    }
    </style>
    <div class="floating-ai">AI</div>
    """,
    unsafe_allow_html=True,
)


# ---------- HELPERS ----------

def save_files(files):
    paths = []
    if not files:
        return ""

    for file in files:
        path = os.path.join(UPLOAD_FOLDER, file.name)
        with open(path, "wb") as f:
            f.write(file.read())
        paths.append(path)

    return ",".join(paths)


def show_files(files):
    if not files:
        return

    for file in files.split(","):
        if not file or not os.path.exists(file):
            continue

        ext = file.split(".")[-1].lower()
        if ext in ["png", "jpg", "jpeg"]:
            st.image(file)
        elif ext in ["mp4", "mov", "avi"]:
            st.video(file)
        elif ext in ["mp3", "wav", "m4a"]:
            st.audio(file)


def estimate_completion(priority):
    priority = (priority or "Medium").strip().lower()
    mapping = {
        "emergency": "Within 12 hours",
        "high": "1 business day",
        "medium": "3 business days",
        "low": "5 business days",
    }
    return mapping.get(priority, "3 business days")


def normalize_ai_analysis(ai_result, problem_text=""):
    ai_result = ai_result or {}
    issue = ai_result.get("issue_type") or ai_result.get("issue") or "Water issue"
    solution = ai_result.get("solution_steps") or ai_result.get("solution") or ""
    priority = ai_result.get("priority") or "Medium"
    estimated = ai_result.get("estimated_resolution_date") or estimate_completion(priority)
    return {
        "issue_type": issue,
        "issue": issue,
        "location": ai_result.get("location") or "Not mentioned",
        "priority": priority,
        "department": ai_result.get("department") or "Water Maintenance",
        "description": ai_result.get("description") or problem_text,
        "estimated_resolution_date": estimated,
        "solution_steps": solution,
        "solution": solution,
    }


def complaint_context(row):
    return (
        f"Citizen: {row.get('Name', '')}\n"
        f"Phone: {row.get('Phone', '')}\n"
        f"Issue: {row.get('Issue', '')}\n"
        f"Location: {row.get('Location', '')}\n"
        f"Priority: {row.get('Priority', '')}\n"
        f"Description: {row.get('Description', '')}\n"
        f"Current status: {row.get('AI Status', '')}\n"
        f"Progress: {row.get('Progress', 0)}%"
    )


def fallback_status_update(stage, progress, estimate):
    messages = {
        "Complaint submitted": "Your complaint has been submitted and AI triage has started.",
        "Complaint viewed by department": "Your complaint has been reviewed by the department.",
        "Team assigned": "Team assigned for inspection and repair.",
        "Repair work started": "Repair work has started.",
        "50% Completed": "Repair is 50% completed.",
        "Final checking": "Final checking is in progress.",
        "Issue resolved": "Issue resolved and marked complete.",
    }
    return {
        "ai_status": stage,
        "progress_percentage": progress,
        "estimated_completion": estimate,
        "ai_updates": messages.get(stage, f"{stage}. Expected completion date: {estimate}"),
    }


def groq_api_key_ui(key_suffix="", show_link=True):
    """Render Groq API key input with helpful link."""
    api_key = st.text_input(
        T["api_key"],
        type="password",
        key=f"groq_api_key_{key_suffix}",
    )
    if show_link:
        st.markdown(
            '<div class="groq-link">\U0001f511 <a href="https://console.groq.com/keys" target="_blank" rel="noopener noreferrer">Get your free Groq API key here</a></div>',
            unsafe_allow_html=True,
        )
    return api_key


def render_chat_message(role, content, timestamp=None):
    """Render a chat bubble."""
    if role == "user":
        avatar = '<span class="chat-avatar-user">\U0001f464</span>'
        bubble_class = "chat-bubble-user"
    else:
        avatar = '<span class="chat-avatar-ai">\U0001f916</span>'
        bubble_class = "chat-bubble-ai"

    ts = f'<div class="chat-timestamp">{timestamp or ""}</div>' if timestamp else ""

    return f'<div class="{bubble_class}">{avatar}{content}{ts}</div>'


# ---------- MENU ----------

menu = st.sidebar.radio(
    T["menu"],
    [
        f"Home - {T['dashboard']}",
        f"Citizen AI - {T['report']}",
        f"Track Complaint - {T['view']}",
        f"Admin - {T['admin']}",
        f"Help Desk - {T['help']}",
    ],
    key="main_menu_radio",
)


# ---------- DASHBOARD ----------

if menu.startswith("Home"):
    df = get_all_complaints()
    total = len(df)
    resolved = len(df[df["Status"] == "Resolved"]) if total else 0
    pending = total - resolved

    col1, col2, col3 = st.columns(3)
    col1.metric(T["total"], total)
    col2.metric(T["pending"], pending)
    col3.metric(T["resolved"], resolved)


# ---------- CITIZEN AI ----------

elif menu.startswith("Citizen AI"):
    st.subheader(T["report_title"])

    st.markdown("---")

    # BYOK Groq API Key only
    citizen_api_key = groq_api_key_ui("citizen")

    col1, col2 = st.columns(2)
    with col1:
        citizen_name = st.text_input(T["name"], key="citizen_name_input")
    with col2:
        citizen_phone = st.text_input(T["phone"], max_chars=10, key="citizen_phone_input")

    citizen_problem = st.text_area(T["problem_explain"], key="citizen_problem_text", height=160)

    # Optional media upload
    st.markdown(f"**{T['upload_evidence']}** *(optional)*")
    files = st.file_uploader(
        "Upload images or videos",
        type=["jpg", "png", "mp4", "mp3", "wav"],
        accept_multiple_files=True,
        key="citizen_files_uploader",
        label_visibility="collapsed",
    )

    analyze_clicked = st.button("\U0001f916 Analyze Complaint", key="citizen_analyze_btn", type="primary")

    if analyze_clicked:
        # Validation - ONLY check: API key, name, phone, problem
        errors = []
        if not citizen_api_key.strip():
            errors.append("Groq API key is required")
        if not citizen_name.strip():
            errors.append(T["name"])
        if not citizen_phone.strip():
            errors.append(T["phone"])
        elif not is_valid_phone(citizen_phone):
            errors.append(T["invalid_phone"])
        if not citizen_problem.strip():
            errors.append("Problem description is required")

        if errors:
            for err in errors:
                st.error(f"\u274c {err}")
        else:
            try:
                with st.spinner("\U0001f9e0 AI is analyzing your complaint..."):
                    citizen_prompt = f"""Analyze this citizen water complaint and return a structured JSON response.

Citizen Name: {citizen_name}
Phone: {citizen_phone}
Problem: {citizen_problem}

Based on the problem description, determine and return:
1. citizen_name: The citizen's name
2. phone: The citizen's phone number
3. issue_type: A short category e.g. Water leakage, No water, Dirty water, Low pressure, Contamination, Pipe burst, Billing issue, or Other water issue
4. description: A properly formatted, clean description of the problem
5. location: Detect any location mentioned (street, area, city, landmark). If none found, return "Not specified"
6. priority: Determine automatically based on severity:
   - EMERGENCY: Health risk, contamination, no water, burst pipe flooding, hospital/school impact
   - HIGH: Active leakage, dirty water, severe pressure loss, repeated outage, large area affected
   - MEDIUM: Normal maintenance, intermittent supply, localized inconvenience
   - LOW: Small issue, minor or informational
7. department: The responsible department - Water Supply, Water Maintenance, Water Quality, Emergency Response, or Customer Support
8. estimated_solution_time: Realistic estimate e.g. "Within 12 hours", "1 business day", "3 business days", "5 business days"

Return ONLY valid JSON with these exact keys:
citizen_name, phone, issue_type, description, location, priority, department, estimated_solution_time
"""

                    ai_result = _chat_json(citizen_prompt, api_key=citizen_api_key.strip())

                st.success("\u2705 AI analysis complete!")
                st.session_state["citizen_ai_result"] = ai_result
                st.session_state["citizen_ai_analyzed"] = True
            except Exception as err:
                st.error(f"\u274c AI analysis failed: {err}")
                st.session_state["citizen_ai_result"] = None
                st.session_state["citizen_ai_analyzed"] = False

    # Show AI analysis result if available
    ai_result = st.session_state.get("citizen_ai_result")
    ai_analyzed = st.session_state.get("citizen_ai_analyzed", False)

    if ai_result and ai_analyzed:
        st.markdown("### \U0001f4cb AI Analysis Result")

        result_html = '<div class="json-result"><table>'
        field_labels = {
            "citizen_name": "\U0001f464 Citizen Name",
            "phone": "\U0001f4de Phone",
            "issue_type": "\U0001f4cc Issue Type",
            "description": "\U0001f4dd Description",
            "location": "\U0001f4cd Location",
            "priority": "\u26a1 Priority",
            "department": "\U0001f3e2 Department",
            "estimated_solution_time": "\u23f1 Estimated Solution Time",
        }
        for key, label in field_labels.items():
            val = ai_result.get(key, "")
            if val:
                result_html += f"<tr><td>{label}</td><td>{val}</td></tr>"
        result_html += "</table></div>"
        st.markdown(result_html, unsafe_allow_html=True)

        if st.button("\U0001f4e4 Submit Complaint", key="citizen_submit_btn", type="primary"):
            priority = ai_result.get("priority", "Medium")
            add_complaint(
                {
                    "Name": ai_result.get("citizen_name", citizen_name),
                    "Phone": ai_result.get("phone", citizen_phone),
                    "Issue": format_issue(ai_result.get("issue_type", "Water issue")),
                    "Location": ai_result.get("location", ""),
                    "Department": ai_result.get("department", ""),
                    "Priority": priority,
                    "Description": ai_result.get("description", citizen_problem),
                    "Image": save_files(files),
                    "Time": get_time(),
                    "Status": "Pending",
                    "AI Status": T["ai_status_initial"],
                    "Progress": 10,
                    "Estimated Completion": ai_result.get("estimated_solution_time", estimate_completion(priority)),
                    "AI Updates": T["ai_updates_initial"],
                    "Admin Solution": "",
                    "Final AI Report": "",
                }
            )
            st.success("\u2705 " + T["success"])
            st.balloons()
            st.session_state.pop("citizen_ai_result", None)
            st.session_state.pop("citizen_ai_analyzed", None)

    elif ai_analyzed and not ai_result:
        st.info("\u2139\ufe0f AI analysis did not return valid results. Please try again with more details.")


# ---------- VIEW ----------

elif menu.startswith("Track Complaint"):
    df = get_all_complaints()
    if df.empty:
        st.warning(T["no_complaints"])
    else:
        for _, row in df.iterrows():
            if row["Status"] == "Resolved":
                st.success(f"\u2705 {row['Issue']} - {T['resolved']}")
            else:
                st.warning(f"\U0001f7e1 {row['Issue']} - {T['pending']}")

            with st.expander(T["view_details"]):
                st.write(T["name"], ":", row["Name"])
                st.write(T["phone"], ":", row["Phone"])
                st.write(T["issue_type"], ":", row["Issue"])
                st.write(T["location"], ":", row["Location"])
                st.write(T["department"], ":", row.get("Department", ""))
                st.write(T["priority"], ":", row.get("Priority", ""))
                st.write(T["description"], ":", row["Description"])
                st.write(T["ai_status"], ":", row.get("AI Status", ""))
                st.write(T["progress"], ":", f"{row.get('Progress', 0)}%")
                st.write(T["estimated_completion"], ":", row.get("Estimated Completion", ""))
                st.write(T["ai_updates"], ":", row.get("AI Updates", ""))
                st.subheader(T["citizen_proof"])
                show_files(row["Image"])
                if row["Status"] == "Resolved":
                    st.subheader(T["resolution_details"])
                    st.write(row["Resolution"])
                    st.write(T["final_ai_report"], ":", row.get("Final AI Report", ""))
                    st.subheader(T["resolution_proof"])
                    show_files(row["Resolution Files"])


# ---------- HELP DESK ----------

elif menu.startswith("Help Desk"):
    st.subheader(T["help_title"])
    st.write(T["help_description"])
    st.info(T["support_contact"])

    st.markdown("---")

    st.markdown("### \U0001f511 AI Configuration")
    help_api_key = groq_api_key_ui("help_desk")

    st.markdown("---")

    if "help_chat_history" not in st.session_state:
        st.session_state["help_chat_history"] = []

    help_query = st.text_area(
        T["help_chat_prompt"],
        height=100,
        key="help_chat_query_input",
    )

    col1, col2 = st.columns([1, 5])
    with col1:
        send_clicked = st.button("\U0001f4ac Send", key="help_chat_send_btn", type="primary")

    if send_clicked:
        if not help_query.strip():
            st.error("\u274c Please enter your question.")
        elif not help_api_key.strip():
            st.error("\u274c " + T["fill_api_key"])
        else:
            st.session_state["help_chat_history"].append({
                "role": "user",
                "content": help_query.strip(),
                "timestamp": get_time(),
            })

            try:
                with st.spinner("\U0001f916 AI is thinking..."):
                    help_response = ask_help_desk(
                        help_query.strip(),
                        api_key=help_api_key.strip(),
                    )

                st.session_state["help_chat_history"].append({
                    "role": "assistant",
                    "content": help_response,
                    "timestamp": get_time(),
                })
            except Exception as err:
                st.error(f"\u274c AI error: {err}")

    if st.session_state["help_chat_history"]:
        st.markdown("### \U0001f4ac Chat Conversation")
        chat_html = '<div class="chat-container">'
        for msg in st.session_state["help_chat_history"]:
            chat_html += render_chat_message(
                msg["role"],
                msg["content"],
                msg.get("timestamp", ""),
            )
        chat_html += "</div>"
        st.markdown(chat_html, unsafe_allow_html=True)

        if st.button("\U0001f5d1\ufe0f Clear Chat", key="help_chat_clear_btn"):
            st.session_state["help_chat_history"] = []
            st.rerun()
    else:
        st.info("\U0001f4a1 Start a conversation by typing a question above and clicking Send.")


# ---------- ADMIN ----------

elif menu.startswith("Admin"):
    st.subheader(T["admin_dashboard"])
    password = st.text_input(T["admin_password"], type="password", key="admin_password_input")

    if password == os.getenv("ADMIN_PASSWORD", "admin123"):
        df = get_all_complaints()
        total = len(df)
        resolved = len(df[df["Status"] == "Resolved"]) if total else 0
        pending = total - resolved

        col1, col2, col3 = st.columns(3)
        col1.metric(T["total"], total)
        col2.metric(T["pending"], pending)
        col3.metric(T["resolved"], resolved)

        if df.empty:
            st.warning(T["no_complaints"])
        else:
            st.dataframe(df, use_container_width=True)
            index = st.number_input(
                T["complaint_index"],
                min_value=0,
                max_value=len(df) - 1,
                key="admin_complaint_index_input",
            )
            selected = df.iloc[index]

            st.write(T["name"], ":", selected["Name"])
            st.write(T["phone"], ":", selected["Phone"])
            st.write(T["selected_issue"], selected["Issue"])
            st.write(T["current_status"], selected["Status"])
            st.write(T["location"], ":", selected["Location"])
            st.write(T["priority"], ":", selected.get("Priority", ""))
            st.write(T["department"], ":", selected.get("Department", ""))
            st.write(T["description"], ":", selected.get("Description", ""))
            st.write(T["ai_status"], ":", selected.get("AI Status", ""))
            st.write(T["progress"], ":", f"{selected.get('Progress', 0)}%")
            st.write(T["estimated_completion"], ":", selected.get("Estimated Completion", ""))
            st.subheader(T["citizen_proof"])
            show_files(selected.get("Image", ""))

            status = st.selectbox(
                T["status"],
                ["Pending", "Resolved"],
                index=0 if selected["Status"] == "Pending" else 1,
                key="admin_status_select",
            )
            resolution = st.text_area(
                T["resolution_details"],
                value=selected.get("Resolution", ""),
                key="admin_resolution_text",
                height=160,
            )
            # Show current AI-tracked values from DB (read-only, managed by AI)
            st.markdown("### \U0001f4ca Progress & Estimated Completion")
            col_a1, col_a2 = st.columns(2)
            current_progress = int(selected.get("Progress", 0) or 0)
            current_completion = selected.get("Estimated Completion", "Not set")
            current_ai_status = selected.get("AI Status", "Not set")
            current_updates = selected.get("AI Updates", "")
            with col_a1:
                st.metric("\U0001f4ca Progress", f"{current_progress}%")
                st.metric("\u23f1 Estimated Completion", current_completion)
            with col_a2:
                st.metric("\U0001f4ac AI Status", current_ai_status)
            if current_updates:
                st.info(f"\U0001f4dd AI Updates: {current_updates}")

            proof = st.file_uploader(
                T["resolution_proof"],
                type=["png", "jpg", "jpeg", "mp4", "mov", "avi", "mp3", "wav", "m4a"],
                accept_multiple_files=True,
                key="admin_proof_uploader",
            )

            if st.button(T["update"], key="admin_update_btn"):
                proof_files = save_files(proof)

                # Use existing values from DB (no AI auto-progress)
                ai_status = selected.get("AI Status", "")
                progress_percentage = int(selected.get("Progress", 0) or 0)
                estimated_completion = selected.get("Estimated Completion", "")
                ai_updates = selected.get("AI Updates", "")

                update_status(
                    index,
                    status=status,
                    resolution=resolution,
                    resolution_files=proof_files,
                    ai_status=ai_status,
                    progress_percentage=progress_percentage,
                    estimated_completion=estimated_completion,
                    ai_updates=ai_updates,
                    admin_solution="",
                    final_ai_report=selected.get("Final AI Report", ""),
                )
                st.success("\u2705 " + T["admin_success"])
                st.rerun()

            # ---------- OLLAMA ADMIN CHATBOT ----------
            st.markdown("---")
            st.markdown("### \U0001f916 AI Assistant (Ollama)")

            # Initialize admin chat history
            if "admin_ollama_chat_history" not in st.session_state:
                st.session_state["admin_ollama_chat_history"] = []

            admin_question = st.text_area(
                "Ask a question about this complaint (e.g., What is the possible cause? What repair steps are needed?)",
                height=80,
                key="admin_ollama_question_input",
            )

            col_ask, col_clear = st.columns([1, 5])
            with col_ask:
                ask_clicked = st.button("\U0001f4ac Ask AI", key="admin_ollama_ask_btn", type="primary")
            with col_clear:
                if st.button("\U0001f5d1\ufe0f Clear Chat", key="admin_ollama_clear_btn"):
                    st.session_state["admin_ollama_chat_history"] = []
                    st.rerun()

            if ask_clicked:
                if not admin_question.strip():
                    st.error("\u274c Please enter a question.")
                else:
                    ctx = complaint_context(selected.to_dict())
                    st.session_state["admin_ollama_chat_history"].append({
                        "role": "user",
                        "content": admin_question.strip(),
                        "timestamp": get_time(),
                    })
                    try:
                        with st.spinner("\U0001f9e0 AI is thinking..."):
                            ollama_response = ask_admin_ollama(ctx, admin_question.strip())
                        st.session_state["admin_ollama_chat_history"].append({
                            "role": "assistant",
                            "content": ollama_response,
                            "timestamp": get_time(),
                        })
                    except Exception as err:
                        st.error(f"\u274c AI error: {err}")

            if st.session_state["admin_ollama_chat_history"]:
                st.markdown("#### \U0001f4ac Chat History")
                chat_html = '<div class="chat-container">'
                for msg in st.session_state["admin_ollama_chat_history"]:
                    chat_html += render_chat_message(
                        msg["role"],
                        msg["content"],
                        msg.get("timestamp", ""),
                    )
                chat_html += "</div>"
                st.markdown(chat_html, unsafe_allow_html=True)
            else:
                st.info("\U0001f4a1 Ask a question about the selected complaint to get AI-powered insights.")

    elif password:
        st.error("\u274c " + T["wrong"])