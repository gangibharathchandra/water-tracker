import requests
from openai import OpenAI


# ==================================================
# CITIZEN AI AGENT (GROQ)
# Creates proper complaint
# ==================================================


def citizen_ai_agent(
    api_key,
    complaint,
):

    if not api_key:
        return "AI service key missing."

    if not complaint:
        return "Please explain your water problem."

    try:
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

        prompt = f"""
You are an AI complaint registration officer
for a water issue management system.

Citizen may explain problems in simple words.

Citizen Complaint:

{complaint}


Analyze and create an official complaint.


Return exactly:


Issue Type:


Location:


Priority:
Low / Medium / High


Complaint Description:


Possible Cause:
"""

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content

    except Exception as error:
        return f"""
Citizen AI Error:

{error}
"""


# ==================================================
# ADMIN AI AGENT (OLLAMA LOCAL)
# Helps solve problem
# ==================================================


def admin_ai_solver(
    complaint,
):

    if not complaint:
        return "No complaint selected."

    prompt = f"""
You are a water department engineer.

Analyze this complaint:

{complaint}


Provide:

Problem Type:

Priority:

Root Cause:

Required Materials:

Repair Steps:

Department Action:
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
            },
            timeout=180,
        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "No response from Ollama",
        )

    except Exception:
        return """
Ollama is not running.

Start Ollama:

ollama serve
"""


# ==================================================
# OLD FUNCTION SUPPORT
# ==================================================


def analyze_with_byok(
    api_key,
    complaint,
):

    return citizen_ai_agent(
        api_key,
        complaint,
    )


def analyze_with_ollama(
    complaint,
):

    return admin_ai_solver(
        complaint,
    )


def analyze_complaint_local(
    complaint,
):

    return analyze_with_ollama(
        complaint,
    )


def analyze_complaint_byok(
    api_key,
    complaint,
):

    return analyze_with_byok(
        api_key,
        complaint,
    )
