blacklist = ["192.168.1.100", "10.0.0.5"]

def detect_threats(data):
    alerts = []

    for entry in data:
        if entry["ip"] in blacklist:
            alerts.append(f"Blacklisted IP detected: {entry['ip']}")

        if entry["port"] == 22:
            alerts.append("Possible SSH attack")

    return alerts
