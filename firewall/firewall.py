import json
import time
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, UDP, ICMP

DictOfPackets = {}

try:
    with open('firewall_rules.json', 'r') as f:
        rules = json.load(f)
    
    ListOfBannedIpAddr = rules.get("ListOfBannedIpAddr", [])
    ListOfBannedPorts = rules.get("ListOfBannedPorts", [])
    ListOfBannedPrefixes = rules.get("ListOfBannedPrefixes", [])
    TimeThreshold = rules.get("TimeThreshold", 10)  # Time window in seconds
    PacketThreshold = rules.get("PacketThreshold", 100) # Packets per window
    BlockPingAttacks = rules.get("BlockPingAttacks", True)
    
    print("Firewall rules loaded successfully from firewall_rules.json")

except FileNotFoundError:
    print("Warning: 'firewall_rules.json' not found. Using default empty rules.")
    ListOfBannedIpAddr = []
    ListOfBannedPorts = []
    ListOfBannedPrefixes = []
    TimeThreshold = 10
    PacketThreshold = 100
    BlockPingAttacks = True

# --- Main Packet Processing Function ---

def process_packet(pkt):
    """
    This function is called for each packet intercepted by NetfilterQueue.
    It applies the loaded security rules to decide whether to accept or drop the packet.
    """
    try:
        # Convert the raw packet into a scapy IP object for easy analysis
        sca_pkt = IP(pkt.get_payload())

        # 1. Block by Source IP Address
        if sca_pkt.src in ListOfBannedIpAddr:
            print(f"Blocking packet: Source IP {sca_pkt.src} is on the ban list.")
            pkt.drop()
            return

        # 2. Block by Source IP Prefix
        if any(sca_pkt.src.startswith(prefix) for prefix in ListOfBannedPrefixes):
            print(f"Blocking packet: Source IP {sca_pkt.src} matches a banned prefix.")
            pkt.drop()
            return

        # 3. Block by Destination Port (for TCP and UDP)
        if sca_pkt.haslayer(TCP):
            tcp_layer = sca_pkt.getlayer(TCP)
            if tcp_layer.dport in ListOfBannedPorts:
                print(f"Blocking packet: Destination port {tcp_layer.dport} is on the ban list.")
                pkt.drop()
                return

        if sca_pkt.haslayer(UDP):
            udp_layer = sca_pkt.getlayer(UDP)
            if udp_layer.dport in ListOfBannedPorts:
                print(f"Blocking packet: Destination port {udp_layer.dport} is on the ban list.")
                pkt.drop()
                return

        # 4. Anomaly Detection: Block Ping (ICMP) Floods
        if BlockPingAttacks and sca_pkt.haslayer(ICMP):
            icmp_layer = sca_pkt.getlayer(ICMP)
            # Check if it's an ICMP echo-request (ping)
            if icmp_layer.type == 8:
                current_time = time.time()
                src_ip = sca_pkt.src

                # If we haven't seen this IP before, start tracking it
                if src_ip not in DictOfPackets:
                    DictOfPackets[src_ip] = []

                # Add the current timestamp to this IP's list
                DictOfPackets[src_ip].append(current_time)
                
                # Remove timestamps that are outside the time window
                DictOfPackets[src_ip] = [t for t in DictOfPackets[src_ip] if current_time - t < TimeThreshold]

                # If the number of packets exceeds the threshold, block it
                if len(DictOfPackets[src_ip]) > PacketThreshold:
                    print(f"Blocking Ping Flood Attack from {src_ip}.")
                    pkt.drop()
                    return
        
        # If no rules were matched, accept the packet
        pkt.accept()

    except Exception as e:
        print(f"An error occurred while processing a packet: {e}")
        pkt.accept() # Accept packet on error to avoid blocking legitimate traffic


if __name__ == "__main__":
    # Create an instance of NetfilterQueue
    nfqueue = NetfilterQueue()
    
    # Bind it to queue number 1 and set process_packet as the callback
    nfqueue.bind(1, process_packet)
    
    print("Firewall is now running... Press CTRL+C to stop.")
    
    try:
        # Start listening for packets
        nfqueue.run()
    except KeyboardInterrupt:
        print("Stopping firewall...")
    finally:
        # Unbind the queue to clean up
        nfqueue.unbind()
        print("Firewall stopped.")

