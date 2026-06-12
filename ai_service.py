import json
import os
import re

from openai import OpenAI

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        return False


load_dotenv()

GROQ_BASE_URL = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.1-8b-instant"


class AIServiceError(Exception):
    pass


def _get_api_key(api_key=None):
    if api_key:
        return api_key

    try:
        import streamlit as st

        secret_key = st.secrets["GROQ_API_KEY"]
        if secret_key:
            return secret_key
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY")


def _get_client(api_key=None):
    key = _get_api_key(api_key)
    if not key:
        raise AIServiceError(
            "GROQ_API_KEY not found. Add it to Streamlit secrets or environment variables."
        )

    return OpenAI(api_key=key, base_url=GROQ_BASE_URL)


def _parse_json_response(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            return json.loads(match.group(0))
        raise AIServiceError("AI returned an invalid response. Please try again.")


def _chat_json(prompt, api_key=None, max_tokens=700):
    client = _get_client(api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a civic water department AI assistant. "
                    "Return only valid JSON. Do not include markdown."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=max_tokens,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    if not content:
        raise AIServiceError("AI response was empty. Please try again.")

    return _parse_json_response(content)


def _chat_text(prompt, api_key=None, max_tokens=400):
    client = _get_client(api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a concise civic help desk assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message.content
    if not content:
        raise AIServiceError("AI response was empty. Please try again.")
    return content.strip()


def _complaint_prompt(problem_text, evidence_files=None):
    evidence = ""
    if evidence_files:
        evidence = "\nUploaded evidence filenames:\n" + "\n".join(
            f"- {file_name}" for file_name in evidence_files
        )

    return f"""
Analyze this citizen water complaint.

Citizen only provided a free-text problem statement. Detect and return:
- issue: short issue category such as Water leakage, No water, Dirty water, Low pressure, Contamination, Billing/connection issue, or Other water issue
- location: exact street/area/city/landmark if mentioned, otherwise "Not mentioned"
- priority: exactly one of Low, Medium, High, Emergency
- description: clean rewritten complaint summary
- solution: suggested department/action for municipal staff
- department: best department such as Water Supply, Water Maintenance, Water Quality, Emergency Response, or Customer Support

Priority rules:
- Emergency for unsafe/contaminated water, burst pipe flooding, health hazard, hospital/school impact, or complete water outage affecting many people
- High for active leakage, dirty/discolored water, severe pressure loss, or repeated outage
- Medium for intermittent supply, low pressure, or localized inconvenience
- Low for minor or informational issues

Return JSON only with keys:
issue, location, priority, description, solution, department
{evidence}

Complaint:
{problem_text}
""".strip()


def _admin_prompt(problem_text):
    return f"""
Analyze this water complaint for an admin engineer.

Return JSON only with:
- possible_cause: likely technical or operational cause
- repair_steps: clear practical repair steps
- department: required department/team
- urgency: estimated urgency exactly one of Low, Medium, High, Emergency

Complaint:
{problem_text}
""".strip()


def _help_prompt(problem_text):
    return f"""
Answer this citizen/admin question about using the Water Issue Tracker.
Be brief and practical.

Question:
{problem_text}
""".strip()


def analyze_complaint_local(problem_text, evidence_files=None):
    if not problem_text or not problem_text.strip():
        raise AIServiceError("Complaint text is required.")
    return _chat_json(_complaint_prompt(problem_text, evidence_files=evidence_files))


def analyze_complaint_byok(problem_text, api_key, evidence_files=None):
    if not problem_text or not problem_text.strip():
        raise AIServiceError("Complaint text is required.")
    if not api_key or not api_key.strip():
        raise AIServiceError("API key is required for BYOK analysis.")
    return _chat_json(
        _complaint_prompt(problem_text, evidence_files=evidence_files),
        api_key=api_key.strip(),
    )


def analyze_admin_solution_local(problem_text):
    if not problem_text or not problem_text.strip():
        raise AIServiceError("Complaint description is required.")
    return _chat_json(_admin_prompt(problem_text))


def analyze_admin_solution(problem_text, api_key):
    if not api_key or not api_key.strip():
        raise AIServiceError("API key is required for BYOK analysis.")
    return _chat_json(_admin_prompt(problem_text), api_key=api_key.strip())


def ask_help_desk_local(problem_text):
    if not problem_text or not problem_text.strip():
        raise AIServiceError("Question is required.")
    return _chat_text(_help_prompt(problem_text))


def ask_help_desk(problem_text, api_key):
    if not api_key or not api_key.strip():
        raise AIServiceError("API key is required for BYOK help.")
    return _chat_text(_help_prompt(problem_text), api_key=api_key.strip())
