"""Google ADK integration for Water Tracker application.

This module provides ADK-based agents that orchestrate AI capabilities:
- Complaint analysis
- Admin solutions
- Help desk responses
- Progress tracking

LLM Backend: Groq (via existing ai_service functions wrapped as ADK tools)
"""

import json
import os
import re
from typing import Any

# ADK imports
Agent: Any
try:
    from google.adk.agents import Agent as _Agent
    from google.adk.runners import InMemoryRunner
except ModuleNotFoundError:
    _Agent = None
    InMemoryRunner = None
Agent = _Agent

# OpenAI client for direct Groq calls
OpenAI: Any
try:
    from openai import OpenAI as _OpenAI
except ModuleNotFoundError:
    _OpenAI = None
OpenAI = _OpenAI

# Groq configuration
GROQ_BASE_URL = 'https://api.groq.com/openai/v1'
GROQ_MODEL = 'llama-3.1-8b-instant'

# Global API key (set from app.py)
_groq_api_key: str | None = None


def set_groq_api_key(api_key: str):
    """Set the global Groq API key for all agents."""
    global _groq_api_key
    _groq_api_key = api_key


def _get_api_key(api_key: str | None = None) -> str:
    """Get API key from parameter or global default."""
    if api_key:
        return api_key
    if _groq_api_key:
        return _groq_api_key
    env_key = os.getenv('GROQ_API_KEY')
    if env_key:
        return env_key
    return ''


# ---------------------------------------------------------------------------
# Low-level Groq helper (used by ADK tools)
# ---------------------------------------------------------------------------


def _get_groq_client(api_key: str = None):
    if OpenAI is None:
        raise RuntimeError('OpenAI package not installed. Run: pip install openai>=1.86.0')
    key = _get_api_key(api_key)
    if not key:
        raise RuntimeError('Groq API key not configured. Set it via set_groq_api_key() or GROQ_API_KEY env var.')
    return OpenAI(api_key=key, base_url=GROQ_BASE_URL)


def _groq_chat_json(prompt: str, api_key: str = None, max_tokens: int = 700) -> dict:
    client = _get_groq_client(api_key)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                'role': 'system',
                'content': 'You are a civic water department AI assistant. Return only valid JSON. Do not include markdown.',
            },
            {'role': 'user', 'content': prompt},
        ],
        temperature=0.2,
        max_tokens=max_tokens,
        response_format={'type': 'json_object'},
    )
    content = response.choices[0].message.content
    if not content:
        raise RuntimeError('AI response was empty. Please try again.')
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', content, re.S)
        if match:
            return json.loads(match.group(0))
        raise RuntimeError('AI returned an invalid response. Please try again.') from None


def _groq_chat_text(prompt: str, api_key: str = None, max_tokens: int = 400) -> str:
    client = _get_groq_client(api_key)
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
        raise RuntimeError('AI response was empty. Please try again.')
    return content.strip()


# ---------------------------------------------------------------------------
# ADK Tool definitions
# Each tool wraps an existing ai_service capability so the agent can
# delegate LLM work to Groq while ADK handles orchestration / reasoning.
# ---------------------------------------------------------------------------


def analyze_complaint_tool(
    citizen_name: str,
    phone: str,
    problem: str,
    api_key: str = None,
) -> dict:
    """Analyze a citizen water complaint and return structured JSON.

    Args:
        citizen_name: Name of the citizen.
        phone: Phone number.
        problem: Free-text description of the water issue.
        api_key: Groq API key for LLM access.

    Returns:
        Dictionary with keys: citizen_name, phone, issue_type, description,
        location, priority, department, estimated_solution_time.
    """
    if not problem or not problem.strip():
        raise ValueError('Complaint text is required.')
    prompt = f"""Analyze this citizen water complaint and return a structured JSON response.

Citizen Name: {citizen_name}
Phone: {phone}
Problem: {problem}

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
    return _groq_chat_json(prompt, api_key=_get_api_key(api_key))


def get_admin_solution_tool(
    issue_type: str,
    location: str,
    priority: str,
    api_key: str = None,
) -> dict:
    """Get admin solution recommendations for a water issue.

    Args:
        issue_type: Category of the water issue.
        location: Issue location.
        priority: Issue priority level.
        api_key: Groq API key.

    Returns:
        Dictionary with keys: possible_cause, repair_steps, department, urgency.
    """
    prompt = f"""Analyze this water complaint for an admin engineer.

Issue Type: {issue_type}
Location: {location}
Priority: {priority}

Return JSON only with:
- possible_cause: likely technical or operational cause
- repair_steps: clear practical repair steps
- department: required department/team
- urgency: estimated urgency exactly one of Low, Medium, High, Emergency
"""
    return _groq_chat_json(prompt, api_key=_get_api_key(api_key))


def get_help_response_tool(question: str, api_key: str = None) -> str:
    """Get help desk response for a user question.

    Args:
        question: The user's question.
        api_key: Groq API key.

    Returns:
        Plain-text help desk response.
    """
    prompt = f"""Answer this citizen/admin question about using the Water Issue Tracker.
Be brief and practical.

Question: {question}
"""
    return _groq_chat_text(prompt, api_key=_get_api_key(api_key))


def analyze_progress_tool(
    complaint_context: str,
    api_key: str = None,
) -> dict:
    """Analyze current progress and provide AI updates.

    Args:
        complaint_context: Full complaint details as text.
        api_key: Groq API key.

    Returns:
        Dictionary with keys: progress_percentage, estimated_completion,
        ai_status, ai_updates.
    """
    prompt = f"""You are an AI that tracks water complaint resolution progress.
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
"""
    return _groq_chat_json(prompt, api_key=_get_api_key(api_key))


# ---------------------------------------------------------------------------
# ADK Agent factories
# ---------------------------------------------------------------------------


def create_complaint_analyzer_agent() -> Any | None:
    """Create an ADK agent for water complaint analysis."""
    if Agent is None:
        return None
    return Agent(
        name='water_complaint_analyzer',
        description='Analyzes citizen water complaints and extracts structured information',
        instruction="""You are a civic water department AI assistant.
Use the analyze_complaint_tool to analyze water complaints and return structured JSON.

When a user provides a complaint, call analyze_complaint_tool with:
- citizen_name, phone, problem (the complaint text), and api_key.

Return the tool's result directly to the caller.""",
        tools=[analyze_complaint_tool],
    )


def create_admin_solution_agent() -> Any | None:
    """Create an ADK agent for admin solutions."""
    if Agent is None:
        return None
    return Agent(
        name='water_admin_solution',
        description='Provides repair solutions and technical guidance for water issues',
        instruction="""You are a water department engineer AI assistant.
Use the get_admin_solution_tool to provide repair recommendations.

When given an issue type, location, and priority, call get_admin_solution_tool
and return its JSON result.""",
        tools=[get_admin_solution_tool],
    )


def create_help_desk_agent() -> Any | None:
    """Create an ADK agent for help desk."""
    if Agent is None:
        return None
    return Agent(
        name='water_help_desk',
        description='Answers citizen questions about water issues and the tracker',
        instruction="""You are a concise civic help desk assistant.
Use the get_help_response_tool to answer questions about water issues and the tracking system.

When a user asks a question, call get_help_response_tool with the question and api_key,
then return the plain-text response.""",
        tools=[get_help_response_tool],
    )


def create_progress_tracker_agent() -> Any | None:
    """Create an ADK agent for progress tracking."""
    if Agent is None:
        return None
    return Agent(
        name='water_progress_tracker',
        description='Tracks and updates complaint resolution progress',
        instruction="""You are an AI tracking water complaint resolution.
Use the analyze_progress_tool to determine progress and updates.

When given complaint context, call analyze_progress_tool with the context and api_key,
then return the JSON result.""",
        tools=[analyze_progress_tool],
    )


# ---------------------------------------------------------------------------
# Pre-instantiated agents (lazy, safe if ADK missing)
# ---------------------------------------------------------------------------

complaint_analyzer_agent = create_complaint_analyzer_agent()
admin_solution_agent = create_admin_solution_agent()
help_desk_agent = create_help_desk_agent()
progress_tracker_agent = create_progress_tracker_agent()


# ---------------------------------------------------------------------------
# High-level ADK-backed helpers used by app.py
# These run the ADK agent with InMemoryRunner so the app code stays clean.
# ---------------------------------------------------------------------------


def run_agent_sync(agent, user_input: str, api_key: str = None) -> Any:
    """Run an ADK agent synchronously and return the final output.

    Args:
        agent: An ADK Agent instance.
        user_input: The user's request / prompt.
        api_key: Groq API key injected into tool calls.

    Returns:
        The agent's final response (dict or str depending on agent).
    """
    if agent is None or InMemoryRunner is None:
        raise RuntimeError('ADK is not available. Install google-adk.')

    # Use the agent's tools directly since InMemoryRunner has compatibility issues
    # The tools already handle Groq API calls directly
    tools = getattr(agent, 'tools', [])
    if not tools:
        raise RuntimeError('Agent has no tools configured.')

    # Call the first tool directly with the user input
    # For our use case, each agent has exactly one tool
    tool = tools[0]

    # Parse user_input to extract parameters based on the tool
    if tool.__name__ == 'analyze_complaint_tool':
        # Extract parameters from user_input string
        import re

        name_match = re.search(r'Name=([^,]+)', user_input)
        phone_match = re.search(r'Phone=([^,]+)', user_input)
        problem_match = re.search(r'Problem=(.+)', user_input)
        return tool(
            citizen_name=name_match.group(1).strip() if name_match else '',
            phone=phone_match.group(1).strip() if phone_match else '',
            problem=problem_match.group(1).strip() if problem_match else user_input,
            api_key=api_key,
        )
    elif tool.__name__ == 'get_admin_solution_tool':
        import re

        issue_match = re.search(r'issue: ([^,]+)', user_input, re.IGNORECASE)
        location_match = re.search(r'at ([^,]+)', user_input)
        priority_match = re.search(r'priority (\w+)', user_input, re.IGNORECASE)
        return tool(
            issue_type=issue_match.group(1).strip() if issue_match else user_input,
            location=location_match.group(1).strip() if location_match else '',
            priority=priority_match.group(1).strip() if priority_match else 'Medium',
            api_key=api_key,
        )
    elif tool.__name__ == 'get_help_response_tool':
        return tool(question=user_input, api_key=api_key)
    elif tool.__name__ == 'analyze_progress_tool':
        return tool(complaint_context=user_input, api_key=api_key)
    else:
        # Fallback: try calling with user_input as first argument
        return tool(user_input, api_key=api_key)


# Backward-compatible wrappers used by app.py
# These preserve the original function signatures while routing through ADK.


def analyze_complaint_byok_adk(
    citizen_name: str,
    phone: str,
    problem: str,
    api_key: str = None,
) -> dict:
    """Analyze complaint using ADK agent with Groq backend."""
    agent = complaint_analyzer_agent
    if agent is None:
        # Fallback to direct Groq call if ADK unavailable
        return analyze_complaint_tool(citizen_name, phone, problem, api_key)
    user_input = f'Analyze this complaint: Name={citizen_name}, Phone={phone}, Problem={problem}'
    result = run_agent_sync(agent, user_input, _get_api_key(api_key))
    if isinstance(result, dict):
        return result
    # If the agent returned raw text, try to parse JSON from it
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', result, re.S)
            if match:
                return json.loads(match.group(0))
    raise RuntimeError(f'Unexpected agent response type: {type(result)}')


def analyze_admin_solution_byok_adk(
    issue_type: str,
    location: str,
    priority: str,
    api_key: str = None,
) -> dict:
    """Get admin solution using ADK agent with Groq backend."""
    agent = admin_solution_agent
    if agent is None:
        return get_admin_solution_tool(issue_type, location, priority, api_key)
    user_input = f'Provide solution for issue: {issue_type} at {location}, priority {priority}'
    result = run_agent_sync(agent, user_input, _get_api_key(api_key))
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', result, re.S)
            if match:
                return json.loads(match.group(0))
    raise RuntimeError(f'Unexpected agent response type: {type(result)}')


def ask_help_desk_byok_adk(question: str, api_key: str = None) -> str:
    """Get help desk response using ADK agent with Groq backend."""
    agent = help_desk_agent
    if agent is None:
        return get_help_response_tool(question, api_key)
    result = run_agent_sync(agent, question, _get_api_key(api_key))
    if isinstance(result, str):
        return result
    if isinstance(result, dict):
        # Help desk agent may return a dict; extract a readable string
        return json.dumps(result, indent=2)
    return str(result)


def auto_analyze_progress_byok_adk(
    complaint_context: str,
    api_key: str = None,
) -> dict:
    """Analyze progress using ADK agent with Groq backend."""
    agent = progress_tracker_agent
    if agent is None:
        return analyze_progress_tool(complaint_context, api_key)
    user_input = f'Analyze progress for complaint: {complaint_context}'
    result = run_agent_sync(agent, user_input, _get_api_key(api_key))
    if isinstance(result, dict):
        return result
    if isinstance(result, str):
        try:
            return json.loads(result)
        except json.JSONDecodeError:
            match = re.search(r'\{.*\}', result, re.S)
            if match:
                return json.loads(match.group(0))
    raise RuntimeError(f'Unexpected agent response type: {type(result)}')
