from scapy.all import sniff

packets = []

def process_packet(packet):
    try:
        packets.append(packet.summary())
        if len(packets) > 20:
            packets.pop(0)
    except:
        pass

def start_sniffing():
    sniff(prn=process_packet, store=False)
