import psutil

def get_network_data():
    connections = psutil.net_connections()
    data = []

    for conn in connections[:20]:
        try:
            data.append({
                "ip": conn.raddr.ip if conn.raddr else "N/A",
                "port": conn.raddr.port if conn.raddr else "N/A",
                "status": conn.status
            })
        except:
            pass

    return data
