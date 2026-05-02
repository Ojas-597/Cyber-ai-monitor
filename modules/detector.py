from modules.vt_api import check_ip

blacklist = ["192.168.1.100"]

def detect_threats(data):
    alerts = []

    for entry in data:
        ip = entry["ip"]

        if ip == "N/A":
            continue

        # 🔴 Blacklist
        if ip in blacklist:
            alerts.append({
                "message": f"Blacklisted IP: {ip}",
                "severity": "HIGH"
            })

        # 🌍 VirusTotal
        vt = check_ip(ip)
        if vt:
            alerts.append(vt)

        # 🔐 SSH detection
        if entry["port"] == 22:
            alerts.append({
                "message": "Possible SSH attack",
                "severity": "MEDIUM"
            })

    return alerts
