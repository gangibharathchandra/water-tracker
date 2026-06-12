import requests
from openai import OpenAI


# ---------- LOCAL AI : OLLAMA ----------


def analyze_with_ollama(
    complaint,
):

    prompt = f"""
You are an assistant for a civic water issue
management system.

Analyze the following citizen complaint:

{complaint}


Return:

Issue Type:
Priority:
Possible Cause:
Suggested Resolution:
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
        },
        timeout=60,
    )

    data = response.json()

    return data.get(
        "response",
        "No response received",
    )


# ---------- CLOUD AI : BYOK ----------


def analyze_with_byok(
    api_key,
    complaint,
):

    client = OpenAI(
        api_key=api_key,
    )

    prompt = f"""
Analyze this water complaint:

{complaint}


Provide:

1. Issue Category

2. Priority Level
   (Low / Medium / High)

3. Explanation

4. Recommended Solution
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.choices[0].message.content
