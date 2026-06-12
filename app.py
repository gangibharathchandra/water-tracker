import os

import streamlit as st

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        return False

from ai_service import (
    analyze_complaint_byok,
    analyze_complaint_local,
    analyze_admin_solution,
    analyze_admin_solution_local,
    ask_help_desk,
    ask_help_desk_local,
)
from database import add_complaint, get_all_complaints, update_status
from languages import LANG
from utils import format_issue, get_time, is_valid_phone


load_dotenv()


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


st.set_page_config(page_title="Water Issue Tracker", page_icon="💧", layout="wide")

language = st.sidebar.selectbox("🌐 Language", list(LANG.keys()), index=0, key="language")
T = LANG.get(language, LANG["English"])

st.title(T["title"])


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
    mapping = {
        T["emergency"]: "Within 12 hours",
        T["high"]: "1 business day",
        T["medium"]: "3 business days",
        T["low"]: "5 business days",
    }
    return mapping.get(priority, "3 business days")


# ---------- MENU ----------

menu = st.sidebar.radio(
    T["menu"],
    [
        T["dashboard"],
        T["report"],
        T["view"],
        T["admin"],
        T["help"],
    ],
    key="main_menu",
)


# ---------- DASHBOARD ----------

if menu == T["dashboard"]:
    df = get_all_complaints()
    total = len(df)
    resolved = len(df[df["Status"] == "Resolved"]) if total else 0
    pending = total - resolved

    col1, col2, col3 = st.columns(3)
    col1.metric(T["total"], total)
    col2.metric(T["pending"], pending)
    col3.metric(T["resolved"], resolved)


# ---------- REPORT ----------

elif menu == T["report"]:
    st.subheader(T["report_title"])

    name = st.text_input(T["name"], key="citizen_name")
    phone = st.text_input(T["phone"], max_chars=10, key="citizen_phone")
    problem = st.text_area(T["problem_explain"], key="citizen_problem", height=160)

    files = st.file_uploader(
        T["upload_evidence"],
        type=["jpg", "png", "mp4", "mp3", "wav"],
        accept_multiple_files=True,
        key="citizen_files",
    )

    ai_mode = st.radio(
        T["ai_mode"],
        [T["local_ai"], T["byok_ai"]],
        key="citizen_ai_mode",
    )

    api_key = ""
    if ai_mode == T["byok_ai"]:
        api_key = st.text_input(T["api_key"], type="password", key="citizen_byok_api_key")

    if st.button(T["analyze_complaint"], key="analyze_complaint"):
        if not name.strip() or not phone.strip() or not problem.strip():
            st.error(T["fill_required"])
        elif not is_valid_phone(phone):
            st.error(T["invalid_phone"])
        elif ai_mode == T["byok_ai"] and not api_key.strip():
            st.error(T["fill_api_key"])
        else:
            evidence_file_names = [file.name for file in files] if files else None
            try:
                with st.spinner(T["ai_processing"]):
                    if ai_mode == T["local_ai"]:
                        ai_result = analyze_complaint_local(problem, evidence_files=evidence_file_names)
                    else:
                        ai_result = analyze_complaint_byok(problem, api_key, evidence_files=evidence_file_names)
                st.success(T["ai_complete"])
                st.session_state["ai_result"] = ai_result
            except Exception as err:
                st.error(f"AI analysis failed: {err}")
                ai_result = {
                    "issue": "",
                    "location": "",
                    "priority": T["medium"],
                    "description": problem,
                    "solution": "",
                    "department": "",
                }
                st.session_state["ai_result"] = ai_result

    ai_result = st.session_state.get(
        "ai_result",
        {
            "issue": "",
            "location": "",
            "department": "",
            "priority": T["medium"],
            "description": problem if problem else "",
            "solution": "",
        },
    )

    st.markdown(f"### {T['ai_result']}")
    
    if ai_result.get("issue") or ai_result.get("location") or ai_result.get("priority"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label=T["issue_type"],
                value=ai_result.get("issue", "—"),
            )
        
        with col2:
            priority_val = ai_result.get("priority", T["medium"])
            st.metric(
                label=T["priority"],
                value=priority_val,
            )
        
        with col3:
            location_str = ai_result.get("location", "—")
            display_location = (location_str[:20] + "..." if len(location_str) > 20 else location_str)
            st.metric(
                label=T["location"],
                value=display_location,
            )
        
        with col4:
            st.metric(
                label=T["department"],
                value=ai_result.get("department", "—"),
            )
    
    if files:
        st.info(f"📎 Evidence: {len(files)} file(s) uploaded")
    
    if ai_result.get("solution"):
        with st.expander(f"✨ {T['ai_solution']}", expanded=True):
            st.info(ai_result["solution"])
    
    description = st.text_area(
        T["description"],
        value=ai_result.get("description", problem if problem else ""),
        key="ai_description",
        height=150,
    )

    if st.button(T["submit"], key="submit_complaint"):
        if not name or not phone or not problem:
            st.error(T["fill_required"])
        elif not is_valid_phone(phone):
            st.error(T["invalid_phone"])
        else:
            uploaded = save_files(files)
            priority = ai_result.get("priority", T["medium"])
            add_complaint(
                {
                    "Name": name,
                    "Phone": phone,
                    "Issue": format_issue(ai_result.get("issue", "")),
                    "Location": ai_result.get("location", ""),
                    "Department": ai_result.get("department", ""),
                    "Priority": priority,
                    "Description": description,
                    "Image": uploaded,
                    "Time": get_time(),
                    "Status": "Pending",
                    "AI Status": T["ai_status_initial"],
                    "Progress": 10,
                    "Estimated Completion": estimate_completion(priority),
                    "AI Updates": T["ai_updates_initial"],
                    "Admin Solution": "",
                    "Final AI Report": "",
                }
            )
            st.success(T["success"])
            st.session_state.pop("ai_result", None)


# ---------- VIEW ----------

elif menu == T["view"]:
    df = get_all_complaints()
    if df.empty:
        st.warning(T["no_complaints"])
    else:
        for _, row in df.iterrows():
            if row["Status"] == "Resolved":
                st.success(f"✅ {row['Issue']} - {T['resolved']}")
            else:
                st.warning(f"🟡 {row['Issue']} - {T['pending']}")

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
                    st.write(T["admin_solution"], ":", row.get("Admin Solution", ""))
                    st.write(T["final_ai_report"], ":", row.get("Final AI Report", ""))
                    st.subheader(T["resolution_proof"])
                    show_files(row["Resolution Files"])


# ---------- HELP ----------

elif menu == T["help"]:
    st.subheader(T["help_title"])
    st.write(T["help_description"])
    st.info(T["support_contact"])

    help_query = st.text_area(T["help_chat_prompt"], height=140, key="help_chat_prompt")
    help_ai_mode = st.radio(
        T["ai_mode"],
        [T["local_ai"], T["byok_ai"]],
        key="help_ai_mode",
    )
    help_api_key = ""
    if help_ai_mode == T["byok_ai"]:
        help_api_key = st.text_input(T["api_key"], type="password", key="help_byok_api_key")

    if st.button(T["help_submit"], key="help_submit"):
        if not help_query:
            st.error(T["fill_required"])
        elif help_ai_mode == T["byok_ai"] and not help_api_key:
            st.error(T["fill_api_key"])
        else:
            try:
                if help_ai_mode == T["local_ai"]:
                    help_response = ask_help_desk_local(help_query)
                else:
                    help_response = ask_help_desk(
                        help_query,
                        api_key=help_api_key,
                    )
                st.session_state["help_ai_response"] = help_response
            except Exception as err:
                st.error(str(err))

    help_response = st.session_state.get("help_ai_response")
    if help_response:
        st.subheader(T["help_response"])
        st.write(help_response)


# ---------- ADMIN ----------

elif menu == T["admin"]:
    st.subheader(T["admin_dashboard"])
    password = st.text_input(T["admin_password"], type="password", key="admin_password")

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
                key="admin_complaint_index",
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
                key="admin_status",
            )
            resolution = st.text_area(T["resolution_details"], value=selected.get("Resolution", ""), key="admin_resolution", height=160)
            ai_status = st.text_input(T["ai_status"], value=selected.get("AI Status", ""), key="admin_ai_status")
            progress_percentage = st.slider(
                T["progress"],
                min_value=0,
                max_value=100,
                value=int(selected.get("Progress", 0) or 0),
                key="admin_progress",
            )
            estimated_completion = st.text_input(
                T["estimated_completion"],
                value=selected.get("Estimated Completion", ""),
                key="admin_estimated_completion",
            )
            ai_updates = st.text_area(
                T["ai_updates"],
                value=selected.get("AI Updates", ""),
                key="admin_ai_updates",
                height=120,
            )
            admin_solution = st.text_area(
                T["admin_solution"],
                value=selected.get("Admin Solution", ""),
                key="admin_solution",
                height=120,
            )
            final_ai_report = st.text_area(
                T["final_ai_report"],
                value=selected.get("Final AI Report", ""),
                key="admin_final_ai_report",
                height=120,
            )
            proof = st.file_uploader(
                T["resolution_proof"],
                type=["png", "jpg", "jpeg", "mp4", "mov", "avi", "mp3", "wav", "m4a"],
                accept_multiple_files=True,
                key="admin_proof",
            )

            if st.button(T["update"], key="admin_update"):
                proof_files = save_files(proof)
                update_status(
                    index,
                    status=status,
                    resolution=resolution,
                    resolution_files=proof_files,
                    ai_status=ai_status,
                    progress_percentage=progress_percentage,
                    estimated_completion=estimated_completion,
                    ai_updates=ai_updates,
                    admin_solution=admin_solution,
                    final_ai_report=final_ai_report,
                )
                st.success(T["admin_success"])
                st.rerun()

            st.markdown(f"### {T['ai_suggest_solution']}")
            admin_problem = st.text_area(
                T["problem_explain"],
                value=selected.get("Description", ""),
                key="admin_problem",
                height=120,
            )

            admin_ai_mode = st.radio(
                T["ai_mode"],
                [T["local_ai"], T["byok_ai"]],
                key="admin_ai_mode",
            )
            admin_api_key = ""
            if admin_ai_mode == T["byok_ai"]:
                admin_api_key = st.text_input(T["api_key"], type="password", key="admin_byok_api_key")

            if st.button(T["ai_suggest_solution"], key="admin_ai_suggest"):
                if admin_ai_mode == T["byok_ai"] and not admin_api_key:
                    st.error(T["fill_api_key"])
                else:
                    try:
                        if admin_ai_mode == T["local_ai"]:
                            admin_result = analyze_admin_solution_local(admin_problem)
                        else:
                            admin_result = analyze_admin_solution(
                                admin_problem,
                                api_key=admin_api_key,
                            )
                        st.session_state["admin_ai_result"] = admin_result
                    except Exception as err:
                        st.error(str(err))

            admin_result = st.session_state.get("admin_ai_result")
            if admin_result:
                st.subheader(f"🔧 {T['ai_solution']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        label=T['urgency'],
                        value=admin_result.get('urgency', 'Medium'),
                    )
                with col2:
                    st.metric(
                        label=T['department'],
                        value=admin_result.get('department', 'Water Maintenance'),
                    )
                
                with st.expander("📖 Possible Cause", expanded=True):
                    st.write(admin_result.get('possible_cause', 'Analysis pending...'))
                
                with st.expander("✅ Repair Steps", expanded=True):
                    st.write(admin_result.get('repair_steps', 'Steps pending...'))


    elif password:
        st.error(T["wrong"])
