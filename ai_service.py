import json
import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    def load_dotenv(*args, **kwargs):
        return False

load_dotenv()


GROQ_API_URL = "https://api.groq.com/openai/v1"


class AIServiceError(Exception):
    pass


def _get_api_key(api_key=None):
    if api_key:
        return api_key

    try:
        import streamlit as st
        if hasattr(st, "secrets"):
            secret_key = st.secrets.get("GROQ_API_KEY")
            if secret_key:
                return secret_key
    except Exception:
        pass

    return os.getenv("GROQ_API_KEY") or os.getenv("OPENAI_API_KEY")


def _get_groq_client(api_key=None):
    try:
        from openai import OpenAI
    except ModuleNotFoundError:
        raise AIServiceError("The OpenAI package is not installed. Install openai>=1.0.0.")

    key = _get_api_key(api_key)
    if not key:
        raise AIServiceError("API key not found. Set GROQ_API_KEY in Streamlit secrets or environment variables, or pass api_key.")

    return OpenAI(api_key=key, api_base=GROQ_API_URL)


def _build_complaint_prompt(problem_text):
    return (
        "You are a municipal complaint assistant. "
        "Extract the issue type, location, priority, description, and solution from the complaint text. "
        "Return only valid JSON with keys: issue, location, priority, description, solution. "
        f"Complaint: {problem_text}"
    )


def _build_admin_prompt(problem_text):
    return (
        "You are a municipal service administrator assistant. "
        "Analyze the complaint and return a JSON object with keys: possible_cause, repair_steps, department, urgency. "
        f"Complaint: {problem_text}"
    )


def _build_help_prompt(problem_text):
    return (
        "You are a civic support assistant. "
        "Provide a concise, helpful answer for the user question about the water issue tracker or complaint process. "
        "Return the answer as plain text without JSON wrappers. "
        f"Question: {problem_text}"
    )


def _parse_response(response_text):
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        raise AIServiceError("Invalid AI response format: expected JSON.")


def _ollama_generate(prompt, model="llama-3.1-8b-instant"):
    try:
        import requests
    except ModuleNotFoundError:
        raise AIServiceError("The requests package is required for local Ollama inference. Install requests.")

    ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    try:
        response = requests.post(ollama_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        text = data.get("response") or data.get("output") or ""
        if not text:
            raise AIServiceError("Local Ollama response was empty.")
        return text
    except Exception as err:
        raise AIServiceError(f"Local Ollama inference failed: {err}")


def _extract_text_from_response(response):
    if hasattr(response, "output_text") and response.output_text:
        return response.output_text

    if hasattr(response, "output") and response.output:
        output = response.output
        if isinstance(output, list):
            text_segments = []
            for item in output:
                if isinstance(item, dict):
                    for segment in item.get("content", []):
                        text_segments.append(segment.get("text", ""))
                elif hasattr(item, "text"):
                    text_segments.append(item.text)
            return "".join(text_segments)

    if hasattr(response, "choices") and response.choices:
        first = response.choices[0]
        if hasattr(first, "message") and hasattr(first.message, "content"):
            return first.message.content
        if isinstance(first, dict):
            message = first.get("message") or first
            if isinstance(message, dict):
                return message.get("content", "")

    return ""


def _call_openai(prompt, api_key=None):
    client = _get_groq_client(api_key)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        max_output_tokens=500,
    )

    text = _extract_text_from_response(response)
    if not text:
        raise AIServiceError("AI response was empty.")

    return _parse_response(text)


def analyze_complaint_local(problem_text):
    if not problem_text or len(problem_text.strip()) < 20:
        raise AIServiceError("Complaint text must be at least 20 characters for local analysis.")

    try:
        response_text = _ollama_generate(_build_complaint_prompt(problem_text), model=os.getenv("OLLAMA_MODEL", "llama-3.1-8b-instant"))
        return _parse_response(response_text)
    except AIServiceError:
        return {
            "issue": "Water Leak",
            "location": "Municipal pipeline area",
            "priority": "High",
            "description": problem_text.strip(),
            "solution": "Contact the water department and dispatch a repair crew.",
        }


def analyze_admin_solution_local(problem_text):
    if not problem_text or len(problem_text.strip()) < 20:
        raise AIServiceError("Admin analysis text must be at least 20 characters for local analysis.")

    try:
        response_text = _ollama_generate(_build_admin_prompt(problem_text), model=os.getenv("OLLAMA_MODEL", "llama-3.1-8b-instant"))
        return _parse_response(response_text)
    except AIServiceError:
        return {
            "possible_cause": "Local service review indicates the issue is likely due to aging infrastructure or a blocked line.",
            "repair_steps": "Inspect the affected area, clear blockages, replace damaged pipes, and monitor pressure after repair.",
            "department": "Water Maintenance",
            "urgency": "High",
        }


def ask_help_desk_local(problem_text):
    if not problem_text or len(problem_text.strip()) < 10:
        raise AIServiceError("Help desk question must be at least 10 characters for local assistance.")

    try:
        return _ollama_generate(_build_help_prompt(problem_text), model=os.getenv("OLLAMA_MODEL", "llama-3.1-8b-instant"))
    except AIServiceError:
        return (
            "For support, submit the complaint with as much detail as possible. "
            "If you need urgent help, contact the local water authority or use the admin panel for escalation."
        )


def analyze_complaint_byok(problem_text, api_key=None):
    return _call_openai(_build_complaint_prompt(problem_text), api_key=api_key)


def analyze_admin_solution(problem_text, api_key=None):
    return _call_openai(_build_admin_prompt(problem_text), api_key=api_key)


def ask_help_desk(problem_text, api_key=None):
    client = _get_groq_client(api_key)
    response = client.responses.create(
        model="gpt-4o-mini",
        input=_build_help_prompt(problem_text),
        max_output_tokens=300,
    )
    text = _extract_text_from_response(response)
    if not text:
        raise AIServiceError("AI help desk response was empty.")
    return text.strip()
