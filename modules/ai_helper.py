import openai

openai.api_key = "YOUR_API_KEY"

def explain_alert(alert):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity SOC expert."},
                {"role": "user", "content": f"""
Alert: {alert}

Explain clearly:
- Meaning
- Risk level
- Fix
- Prevention
"""}
            ]
        )
        return res.choices[0].message["content"]
    except:
        return "AI unavailable"
