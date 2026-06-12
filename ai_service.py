import os

try:
    import streamlit as st
except Exception:
    st = None

from openai import OpenAI


def _get_api_key(api_key=None):
    if api_key:
        return api_key

    secret_key = None
    if st is not None and hasattr(st, "secrets"):
        secret_key = st.secrets.get("GROQ_API_KEY")

    if secret_key:
        return secret_key

    return os.getenv("GROQ_API_KEY")


def _get_groq_client(api_key=None):
    key = _get_api_key(api_key)
    if not key:
        raise ValueError("GROQ_API_KEY is required. Set it in Streamlit secrets or environment variables.")

    return OpenAI(
        api_key=key,
        base_url="https://api.groq.com/openai/v1",
    )


def _build_prompt(complaint):
    return f"""
You are a water issue registration assistant.
Extract the important details from the user's description.
Return JSON with these fields:
- issue
- location
- priority
- description
- solution

User description:
{complaint}

Return only valid JSON.
"""


def _build_admin_prompt(problem_text):
    return f"""
You are a water department incident response assistant.
Analyze the complaint and provide a JSON object with:
- possible_cause
- repair_steps
- department
- urgency

Complaint:
{problem_text}

Return only valid JSON.
"""


def _parse_json_or_fallback(text, fallback):
    try:
        import json

        return json.loads(text)
    except Exception:
        return fallback


def analyze_complaint_local(problem_text):
    if not problem_text:
        return {
            "issue": "",
            "location": "",
            "priority": "Low",
            "description": "",
            "solution": "",
        }

    client = _get_groq_client()
    prompt = _build_prompt(problem_text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content
    parsed = _parse_json_or_fallback(
        text,
        {
            "issue": "Water Issue",
            "location": "",
            "priority": "Medium",
            "description": text.strip(),
            "solution": "Please investigate and respond",
        },
    )

    return {
        "issue": parsed.get("issue", "Water Issue"),
        "location": parsed.get("location", ""),
        "priority": parsed.get("priority", "Medium"),
        "description": parsed.get("description", text.strip()),
        "solution": parsed.get("solution", "Please investigate and respond"),
    }


def analyze_complaint_byok(problem_text, api_key):
    if not problem_text:
        return {
            "issue": "",
            "location": "",
            "priority": "Low",
            "description": "",
            "solution": "",
        }

    client = _get_groq_client(api_key=api_key)
    prompt = _build_prompt(problem_text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content
    parsed = _parse_json_or_fallback(
        text,
        {
            "issue": "Water Issue",
            "location": "",
            "priority": "Medium",
            "description": text.strip(),
            "solution": "Please investigate and respond",
        },
    )

    return {
        "issue": parsed.get("issue", "Water Issue"),
        "location": parsed.get("location", ""),
        "priority": parsed.get("priority", "Medium"),
        "description": parsed.get("description", text.strip()),
        "solution": parsed.get("solution", "Please investigate and respond"),
    }


def analyze_admin_solution(problem_text, api_key=None):
    if not problem_text:
        return {
            "possible_cause": "",
            "repair_steps": "",
            "department": "",
            "urgency": "",
        }

    client = _get_groq_client(api_key=api_key)
    prompt = _build_admin_prompt(problem_text)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
    )

    text = response.choices[0].message.content
    parsed = _parse_json_or_fallback(
        text,
        {
            "possible_cause": text.strip(),
            "repair_steps": "Review the issue and take corrective action.",
            "department": "Water Department",
            "urgency": "Medium",
        },
    )

    return {
        "possible_cause": parsed.get("possible_cause", text.strip()),
        "repair_steps": parsed.get("repair_steps", "Review the issue and take corrective action."),
        "department": parsed.get("department", "Water Department"),
        "urgency": parsed.get("urgency", "Medium"),
    }
