from modules.vt_api import check_ip

def detect_threats(data):
    alerts = []

    for entry in data:
        ip = entry["ip"]

        if ip != "N/A":
            vt = check_ip(ip)
            if vt:
                alerts.append(vt)

        if entry["port"] == 22:
            alerts.append("SSH attack suspected")

    return alerts
