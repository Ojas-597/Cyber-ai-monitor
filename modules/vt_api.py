import requests

API_KEY = "YOUR_VIRUSTOTAL_API_KEY"

def check_ip(ip):
    try:
        url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
        headers = {"x-apikey": API_KEY}
        res = requests.get(url, headers=headers).json()

        stats = res["data"]["attributes"]["last_analysis_stats"]

        if stats["malicious"] > 0:
            return f"⚠️ Malicious IP: {ip}"

    except:
        return None
