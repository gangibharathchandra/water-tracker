import json
import os
import re

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


def _build_complaint_prompt(problem_text, evidence_files=None):
    evidence_section = ""
    if evidence_files:
        evidence_section = "\nEvidence files:\n" + "\n".join(
            f"- {name}" for name in evidence_files
        )

    return (
        "You are a municipal complaint assistant. Analyze the complaint and extract structured information.\n\n"
        "EXTRACTION RULES:\n"
        "1. ISSUE: Identify water problem type (Leakage, No Water, Dirty Water, Low Pressure, Contamination, etc)\n"
        "2. LOCATION: Extract specific area name, street, zone, or coordinates mentioned\n"
        "3. PRIORITY: Choose one based on impact:\n"
        "   - Emergency: No water, health hazard, major leak affecting many people\n"
        "   - High: Continuous leak, water discoloration, building flooded\n"
        "   - Medium: Intermittent issues, low pressure in building\n"
        "   - Low: Minor issues, isolated area\n"
        "4. DEPARTMENT: Assign to Water Supply, Maintenance, Quality, or Emergency\n"
        "5. DESCRIPTION: Provide clear summary with impact details\n"
        "6. SOLUTION: Suggest immediate actions\n\n"
        "Return ONLY valid JSON with keys: issue, location, priority, description, solution, department."
        f"{evidence_section}\n\n"
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


def _extract_image_metadata(file_path):
    """Extract metadata from image files."""
    metadata = {"filename": os.path.basename(file_path)}
    
    try:
        if not os.path.exists(file_path):
            return metadata
        
        file_size = os.path.getsize(file_path)
        metadata["size_mb"] = round(file_size / (1024 * 1024), 2)
        
        ext = os.path.splitext(file_path)[1].lower()
        metadata["format"] = ext.lstrip('.')
    except Exception:
        pass
    
    return metadata


def _infer_priority_from_text(text):
    """Infer priority from complaint keywords."""
    text_lower = text.lower()
    
    emergency_keywords = ["no water", "health", "contaminated", "major leak", "flood", "burst", "toxic", "outbreak"]
    high_keywords = ["leak", "burst", "flooding", "black water", "dirty water", "discolor", "major"]
    medium_keywords = ["low pressure", "intermittent", "slow", "issue", "problem"]
    
    if any(kw in text_lower for kw in emergency_keywords):
        return "Emergency"
    if any(kw in text_lower for kw in high_keywords):
        return "High"
    if any(kw in text_lower for kw in medium_keywords):
        return "Medium"
    return "Medium"


def _infer_department_from_text(text):
    """Infer department from complaint keywords."""
    text_lower = text.lower()
    
    if any(kw in text_lower for kw in ["quality", "dirty", "color", "taste", "smell", "contaminated"]):
        return "Water Quality"
    if any(kw in text_lower for kw in ["pressure", "low water", "no water"]):
        return "Water Supply"
    if any(kw in text_lower for kw in ["leak", "burst", "pipe", "flooding"]):
        return "Maintenance"
    if any(kw in text_lower for kw in ["emergency", "urgent", "crisis", "disaster"]):
        return "Emergency Response"
    return "Water Maintenance"


def _parse_response(response_text):
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", response_text, re.S)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
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


def analyze_complaint_local(problem_text, evidence_files=None):
    if not problem_text or len(problem_text.strip()) < 20:
        raise AIServiceError("Complaint text must be at least 20 characters for local analysis.")

    try:
        response_text = _ollama_generate(
            _build_complaint_prompt(problem_text, evidence_files=evidence_files),
            model=os.getenv("OLLAMA_MODEL", "llama-3.1-8b-instant"),
        )
        return _parse_response(response_text)
    except AIServiceError:
        priority = _infer_priority_from_text(problem_text)
        department = _infer_department_from_text(problem_text)
        
        return {
            "issue": "Water Issue",
            "location": "Area mentioned in complaint",
            "priority": priority,
            "description": problem_text.strip(),
            "solution": f"Contact the {department} department for inspection and repair.",
            "department": department,
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


def analyze_complaint_byok(problem_text, api_key=None, evidence_files=None):
    return _call_openai(
        _build_complaint_prompt(problem_text, evidence_files=evidence_files),
        api_key=api_key,
    )


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
