import json
import os
import re
from typing import Any

OpenAI: Any
try:
    from openai import OpenAI as _OpenAI
except ModuleNotFoundError:
    _OpenAI = None
OpenAI = _OpenAI

load_dotenv: Any
try:
    from dotenv import load_dotenv as _load_dotenv
except ModuleNotFoundError:

    def _load_dotenv(*_args, **_kwargs):
        return False


load_dotenv = _load_dotenv


load_dotenv()

GROQ_BASE_URL = 'https://api.groq.com/openai/v1'
GROQ_MODEL = 'llama-3.1-8b-instant'

OLLAMA_BASE_URL = 'http://localhost:11434/v1'
OLLAMA_MODEL = 'llama3:latest'


class AIServiceError(Exception):
    pass


def _get_api_key(api_key=None):
    if api_key:
        return api_key

    try:
        import streamlit as st

        secret_key = st.secrets['GROQ_API_KEY']
        if secret_key:
            return secret_key
    except Exception:  # noqa: S110
        pass

    return os.getenv('GROQ_API_KEY')


def _get_client(api_key=None):
    if OpenAI is None:
        raise AIServiceError('OpenAI package is not installed. Run: pip install openai>=1.86.0')

    key = _get_api_key(api_key)
    if not key:
        raise AIServiceError('GROQ_API_KEY not found. Add it to Streamlit secrets or environment variables.')

    return OpenAI(api_key=key, base_url=GROQ_BASE_URL)


def _parse_json_response(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, re.S)
        if match:
            return json.loads(match.group(0))
        raise AIServiceError('AI returned an invalid response. Please try again.') from None


def _chat_json(prompt, api_key=None, max_tokens=700):
    client = _get_client(api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are a civic water department AI assistant. Return only valid JSON. Do not include markdown.'
                ),
            },
            {'role': 'user', 'content': prompt},
        ],
        temperature=0.2,
        max_tokens=max_tokens,
        response_format={'type': 'json_object'},
    )

    content = response.choices[0].message.content
    if not content:
        raise AIServiceError('AI response was empty. Please try again.')

    return _parse_json_response(content)


def _chat_text(prompt, api_key=None, max_tokens=400):
    client = _get_client(api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                'role': 'system',
                'content': 'You are a concise civic help desk assistant.',
            },
            {'role': 'user', 'content': prompt},
        ],
        temperature=0.3,
        max_tokens=max_tokens,
    )

    content = response.choices[0].message.content
    if not content:
        raise AIServiceError('AI response was empty. Please try again.')
    return content.strip()


def _complaint_prompt(problem_text, evidence_files=None):
    evidence = ''
    if evidence_files:
        evidence = '\nUploaded evidence filenames:\n' + '\n'.join(f'- {file_name}' for file_name in evidence_files)

    return f"""
Analyze this citizen water complaint.

Citizen only provided a free-text problem statement. Detect and return:
- issue_type: short issue category such as Water leakage, No water, Dirty water, Low pressure, Contamination, Billing/connection issue, or Other water issue
- issue: same value as issue_type for backward compatibility
- location: exact street/area/city/landmark if mentioned, otherwise "Not mentioned"
- priority: exactly one of Low, Medium, High, Emergency
- department: best department such as Water Supply, Water Maintenance, Water Quality, Emergency Response, or Customer Support
- description: clean rewritten complaint summary
- estimated_resolution_date: realistic target date in DD/MM/YYYY format
- estimated_solution_time: realistic completion estimate e.g. "Within 12 hours", "1 business day", "3 business days", "5 business days"
- solution_steps: practical suggested next steps for the citizen and department
- solution: same value as solution_steps for backward compatibility

Priority rules:
- Emergency for unsafe/contaminated water, burst pipe flooding, health hazard, hospital/school impact, or complete water outage affecting many people
- High for active leakage, dirty/discolored water, severe pressure loss, or repeated outage
- Medium for intermittent supply, low pressure, or localized inconvenience
- Low for minor or informational issues

Return JSON only with keys:
issue_type, issue, location, priority, department, description, estimated_resolution_date, estimated_solution_time, solution_steps, solution
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


def _status_prompt(stage, complaint):
    return f"""
Generate one short citizen-facing update message for this water complaint.

Stage: {stage}
Complaint details:
{complaint}

Return JSON only with:
- ai_status: a short status title
- progress_percentage: numeric progress from 0 to 100
- estimated_completion: expected date or time window
- ai_updates: one friendly update message for the citizen
""".strip()


def _final_verification_prompt(original_issue, admin_solution, progress):
    return f"""
Perform final AI verification for this water complaint before closure.

Original issue:
{original_issue}

Admin solution notes:
{admin_solution}

Progress: {progress}%

Return JSON only with:
- resolution_confidence: number from 0 to 100
- summary: brief verification summary
- recommendation: whether to resolve now or inspect again
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
        raise AIServiceError('Complaint text is required.')
    return _chat_json(_complaint_prompt(problem_text, evidence_files=evidence_files))


def analyze_complaint_byok(problem_text, api_key, evidence_files=None):
    if not problem_text or not problem_text.strip():
        raise AIServiceError('Complaint text is required.')
    if not api_key or not api_key.strip():
        raise AIServiceError('API key is required for BYOK analysis.')
    return _chat_json(
        _complaint_prompt(problem_text, evidence_files=evidence_files),
        api_key=api_key.strip(),
    )


def analyze_admin_solution_local(problem_text):
    if not problem_text or not problem_text.strip():
        raise AIServiceError('Complaint description is required.')
    return _chat_json(_admin_prompt(problem_text))


def analyze_admin_solution(problem_text, api_key):
    if not api_key or not api_key.strip():
        raise AIServiceError('API key is required for BYOK analysis.')
    return _chat_json(_admin_prompt(problem_text), api_key=api_key.strip())


def generate_status_update(stage, complaint_text, api_key=None):
    if not stage or not complaint_text:
        raise AIServiceError('Stage and complaint text are required.')
    return _chat_json(_status_prompt(stage, complaint_text), api_key=api_key)


def verify_final_resolution(original_issue, admin_solution, progress, api_key=None):
    if not original_issue:
        raise AIServiceError('Original issue is required for final verification.')
    return _chat_json(
        _final_verification_prompt(original_issue, admin_solution or '', progress or 0),
        api_key=api_key,
    )


def ask_help_desk_local(problem_text):
    if not problem_text or not problem_text.strip():
        raise AIServiceError('Question is required.')
    return _chat_text(_help_prompt(problem_text))


def ask_help_desk(problem_text, api_key):
    if not api_key or not api_key.strip():
        raise AIServiceError('API key is required for BYOK help.')
    return _chat_text(_help_prompt(problem_text), api_key=api_key.strip())


def _ollama_chat_text(prompt, max_tokens=500):
    """Use Ollama local API for text generation (admin chatbot)."""
    if OpenAI is None:
        raise AIServiceError('OpenAI package is not installed. Run: pip install openai>=1.86.0')
    try:
        client = OpenAI(api_key='ollama', base_url=OLLAMA_BASE_URL)
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': 'You are a water department engineer AI assistant. Provide practical, helpful responses.',
                },
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.3,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content
        if not content:
            raise AIServiceError('Ollama response was empty. Ensure Ollama is running.')
        return content.strip()
    except Exception as e:
        raise AIServiceError(f'Ollama error: {e}. Ensure Ollama is running at {OLLAMA_BASE_URL}') from e


def ask_admin_ollama(complaint_context, admin_question):
    """Admin chatbot using Ollama local AI with complaint context."""
    if not admin_question or not admin_question.strip():
        raise AIServiceError('Question is required.')
    prompt = f"""You are a water department engineer AI assistant.
You have access to the following complaint context:

{complaint_context}

Answer this question based on the complaint context above. Be specific to this complaint.

Question: {admin_question.strip()}

Provide a helpful, practical response that addresses the question directly."""
    return _ollama_chat_text(prompt)


def _auto_progress_prompt(complaint_context):
    return f"""
You are an AI that tracks water complaint resolution progress.
Analyze the following complaint details and determine the current progress and estimated completion.

Complaint details:
{complaint_context}

Based on the complaint information (issue type, priority, current status, and any admin solution/resolution notes):
1. Determine an appropriate progress_percentage (0 to 100) by analyzing what work has likely been done
2. Determine a realistic estimated_completion date and time based on the issue severity, priority, and current stage
3. Determine a concise ai_status update (one line like "Team assigned", "Repair in progress", "Final checking", etc.)
4. Determine a friendly ai_updates message for the citizen

Return JSON only with:
- progress_percentage: number from 0 to 100
- estimated_completion: date and time string e.g. "15/06/2026 04:30 PM"
- ai_status: short status title
- ai_updates: friendly update message for the citizen
""".strip()


def auto_analyze_progress(complaint_context, api_key=None):
    """
    AI analyzes the complaint work done and automatically sets:
    - progress percentage (0-100)
    - estimated completion date/time
    - AI status update
    - AI updates message
    """
    if not complaint_context:
        raise AIServiceError('Complaint context is required.')
    return _chat_json(_auto_progress_prompt(complaint_context), api_key=api_key)


def _ollama_chat_json(prompt, max_tokens=700):
    """Use Ollama local API for JSON response (citizen complaint analysis)."""
    if OpenAI is None:
        raise AIServiceError('OpenAI package is not installed. Run: pip install openai>=1.86.0')
    try:
        client = OpenAI(api_key='ollama', base_url=OLLAMA_BASE_URL)
        response = client.chat.completions.create(
            model=OLLAMA_MODEL,
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are a civic water department AI assistant. '
                        'Return only valid JSON. Do not include markdown.'
                    ),
                },
                {'role': 'user', 'content': prompt},
            ],
            temperature=0.2,
            max_tokens=max_tokens,
        )
        content = response.choices[0].message.content
        if not content:
            raise AIServiceError('Ollama response was empty. Ensure Ollama is running.')
        return _parse_json_response(content)
    except Exception as e:
        raise AIServiceError(f'Ollama error: {e}. Ensure Ollama is running at {OLLAMA_BASE_URL}') from e


def analyze_complaint_ollama(problem_text, evidence_files=None):
    """Analyze citizen complaint using local Ollama AI (offline mode)."""
    if not problem_text or not problem_text.strip():
        raise AIServiceError('Complaint text is required.')
    return _ollama_chat_json(_complaint_prompt(problem_text, evidence_files=evidence_files))
