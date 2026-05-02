import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def explain_alert(alert):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert."},
                {"role": "user", "content": f"""
Explain this alert clearly:
{alert}

Include:
- Meaning
- Risk level
- Fix
- Prevention
"""}
            ]
        )
        return res.choices[0].message["content"]
    except:
        return "AI explanation unavailable"
