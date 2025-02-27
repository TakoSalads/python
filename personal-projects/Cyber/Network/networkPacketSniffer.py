#Kyle Button
#08/24/24

#Capturing network traffic --
from scapy.all import sniff, IP, TCP, UDP, ICMP, Ether
from datetime import datetime
import socket

# Convert protocol number to name
def get_protocol_name(protocol_number):
    protocols = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
    return protocols.get(protocol_number, 'Other')

# Convert port number to service name (if known)
def get_service_name(port_number, protocol):
    try:
        return socket.getservbyport(port_number, protocol)
    except:
        return str(port_number)

# Define a callback function to process each packet
def packet_callback(packet):
    # Timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Basic packet info
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst
    protocol = get_protocol_name(packet[IP].proto)

    print(f"\n[{timestamp}]")
    print(f"Source IP: {src_ip} --> Destination IP: {dst_ip}")
    print(f"Protocol: {protocol}")

    # Include MAC addresses
    if packet.haslayer(Ether):
        src_mac = packet[Ether].src
        dst_mac = packet[Ether].dst
        print(f"Source MAC: {src_mac} --> Destination MAC: {dst_mac}")

    # Additional TCP/UDP information
    if protocol == 'TCP' and packet.haslayer(TCP):
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
        print(f"Source Port: {get_service_name(src_port, 'tcp')} --> Destination Port: {get_service_name(dst_port, 'tcp')}")
        print(f"Flags: {packet[TCP].flags}")

    elif protocol == 'UDP' and packet.haslayer(UDP):
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        print(f"Source Port: {get_service_name(src_port, 'udp')} --> Destination Port: {get_service_name(dst_port, 'udp')}")

    elif protocol == 'ICMP' and packet.haslayer(ICMP):
        print(f"ICMP Type: {packet[ICMP].type}")

    # Display packet payload (optional)
    if packet.haslayer(IP):
        payload = bytes(packet[IP].payload)
        if payload:
            print(f"Payload: {payload[:30]}...")  # Show only the first 30 bytes

# Start sniffing
sniff(filter="ip", prn=packet_callback, count=100)