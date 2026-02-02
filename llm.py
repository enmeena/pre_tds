import httpx
import os

# Dummy API key (as required)
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI1ZHMyMDAwMDEzQGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.SCUja7d56ab2gDI01c0_0TYAHxVsIY4MfKcHul9ZVVs"
#API_KEY = os.environ["OPENAI_API_KEY"]
# OpenAI Chat Completions endpoint
url = "https://aipipe.org/openrouter/v1/chat/completions"

# The meaningless text (must be EXACT)
text = """AuFCKX hk
6 4  q2VWM jd 9a0PX sdV l1iTfZi  aWN poN"""

# Request payload
payload = {
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "system",
            "content": "Analyze the sentiment of the following text and classify it strictly as GOOD, BAD, or NEUTRAL."
        },
        {
            "role": "user",
            "content": text
        }
    ]
}

# Send POST request
response = httpx.post(
    url,
    json=payload,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
)

# Raise error if request failed
response.raise_for_status()

# Print response JSON
print(response.json())