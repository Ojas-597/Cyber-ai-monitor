import requests

API_KEY = "YOUR_VIRUSTOTAL_API_KEY"
cache = {}

def vt_request(url):
    headers = {"x-apikey": API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=3)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None


def check_ip(ip):
    if ip in cache:
        return cache[ip]

    data = vt_request(f"https://www.virustotal.com/api/v3/ip_addresses/{ip}")
    if not data:
        return None

    stats = data["data"]["attributes"]["last_analysis_stats"]

    if stats["malicious"] > 0:
        result = {
            "type": "IP",
            "value": ip,
            "message": f"Malicious IP detected: {ip}",
            "severity": "HIGH"
        }
        cache[ip] = result
        return result

    return None


def check_domain(domain):
    data = vt_request(f"https://www.virustotal.com/api/v3/domains/{domain}")
    if data:
        stats = data["data"]["attributes"]["last_analysis_stats"]
        if stats["malicious"] > 0:
            return {
                "type": "DOMAIN",
                "value": domain,
                "message": f"Malicious domain: {domain}",
                "severity": "HIGH"
            }
    return None


def check_url(url_input):
    data = vt_request(f"https://www.virustotal.com/api/v3/urls/{url_input}")
    if data:
        stats = data["data"]["attributes"]["last_analysis_stats"]
        if stats["malicious"] > 0:
            return {
                "type": "URL",
                "value": url_input,
                "message": f"Malicious URL detected",
                "severity": "HIGH"
            }
    return None


def check_hash(file_hash):
    data = vt_request(f"https://www.virustotal.com/api/v3/files/{file_hash}")
    if data:
        stats = data["data"]["attributes"]["last_analysis_stats"]
        if stats["malicious"] > 0:
            return {
                "type": "FILE",
                "value": file_hash,
                "message": "Malicious file hash detected",
                "severity": "HIGH"
            }
    return None
