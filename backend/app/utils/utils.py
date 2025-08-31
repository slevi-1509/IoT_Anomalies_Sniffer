import os
from scapy.all import DNS, DNSQR, TCP
from datetime import datetime
from itertools import count
from scapy.all import sniff
import threading
import ipaddress
import json
import socket
import nmap
import requests
import ast
import time
import config
from models.PacketSummary import PackageSummary
from kafka_producer.producer import send_message
from kafka_producer.produce_schema import ProduceMessage

session_new_devices = {}

def start_sniffer(interface, params):
    network = ipaddress.ip_network(f"{interface.ip}/24", strict=False)
    filter = "tcp or udp or icmp"
    if not os.path.exists(config.LOGS_DIR):
        os.makedirs(config.LOGS_DIR)
    for i in count(0):
        session_new_devices.clear()
        sniff(iface=interface, filter=filter, prn=lambda pkt: handle_packet(pkt, network, params.collect_data_time, params.iot_probability),
                count=params.no_of_packets, store=0)
        thread = threading.Thread(target=newDeviceExists, args=(session_new_devices, params.ports_scan, params.os_detect))
        if session_new_devices:
            thread.start()
        time.sleep(params.interval)
        if thread.is_alive():
            thread.join()
          
        if i == params.no_of_sessions-1:
            config.total_new_devices.clear()
            print("Sniffer finished current running")
            break
    
def handle_packet(packet, network, collect_data_time, iot_probability):
    if ipaddress.ip_address(packet.payload.src) not in network:
        return
    packet_summery = PackageSummary(
        timestamp=datetime.fromtimestamp(packet.time).strftime('%Y-%m-%d %H:%M:%S'),
        src_mac=packet.src.upper(),
        src_ip=packet.payload.src,
        dst_mac=packet.dst.upper(),
        dst_ip=packet.payload.dst,
        src_port=packet.payload.payload.sport if "sport" in packet.payload.payload.fields else "None",
        dst_port=packet.payload.payload.dport if "dport" in packet.payload.payload.fields else "None",
        protocol=packet.payload.proto,
        ip_version=packet.payload.version,
        ttl=packet.payload.ttl,
        tcp_window_size=packet[TCP].window if packet.haslayer(TCP) else 0,
    )
    if packet.haslayer(DNS) and packet_summery.dst_port == 53:
        try:
            packet_summery.dns_query = packet[DNSQR].qname.decode("utf-8") if packet.haslayer(DNSQR) else "None" #payload(DNS).qd.0.qname
            # packet_summery.dns_answer = packet[DNSRR].rdata.decode("utf-8") if 'rdata' in packet[DNSRR] else "None"
        except Exception as e:
            print(f"Error decoding DNS data: {e}")
    if (packet_summery.src_mac in config.registered_devices):
        is_iot = config.registered_devices[packet_summery.src_mac].get("is_iot")
        if is_iot < iot_probability:
            print(f"Device {packet_summery.src_mac} is not an IoT device (IoT probability: {is_iot}%)")
            return
    else:
        packet_summery.os = detect_os_fast(packet, packet_summery.tcp_window_size)
        if packet_summery.src_mac not in session_new_devices.keys() and packet_summery.src_mac not in config.total_new_devices.keys():           
            session_new_devices[packet_summery.src_mac] = packet_summery.__dict__
            config.total_new_devices[packet_summery.src_mac] = packet_summery.__dict__
    log_file_path = config.LOGS_DIR + packet_summery.src_mac.replace(":", "") + ".log"
    packet_exists = False
    line_to_dict = {}
    try:
        with open(log_file_path, "a+") as log_file:
            log_file.seek(0) 
            for line in log_file:
                # new_line = "{" + line.strip()[42:]
                line_to_dict = ast.literal_eval(line.strip())
                if [line_to_dict["dst_mac"], line_to_dict["dst_ip"], line_to_dict["dst_port"], line_to_dict["protocol"]] == [packet_summery.dst_mac, packet_summery.dst_ip, packet_summery.dst_port, packet_summery.protocol]:
                    packet_exists = True
                    break
            if not packet_exists:
                if len(line_to_dict) > 0:
                    format_string = "%Y-%m-%d %H:%M:%S"
                    last_packet_time = datetime.strptime(line_to_dict['timestamp'], format_string)
                    curr_packet_time = datetime.strptime(packet_summery.timestamp, format_string)
                    time_diff_sec = (curr_packet_time - last_packet_time).total_seconds()
                    if time_diff_sec > collect_data_time:
                        handle_anomaly(packet_summery)
                log_file.write(str(packet_summery.__dict__) + "\n")
    except IOError as e:
        print(f"Error writing to log file {log_file_path}: {e}")    
    except Exception as e:
        print(f"An error occurred while processing the packet: {e}")
    print(json.dumps(packet_summery.__dict__))

def handle_anomaly(packet_summery):
    with open(config.ANOMALIES_LOG, "a+") as log_file:
        anomaly = str(packet_summery.__dict__).replace("'", '"') # Ensure JSON format
        log_file.write(f"{anomaly}\n")

def newDeviceExists(session_new_devices, ports_scan, os_detect):
    new_devices_dict = {}
    for device in session_new_devices.values():
        if device['src_mac'] in config.registered_devices:
            continue
        host_name = get_hostname_from_ip(device['src_ip'])
        vendor_name = get_vendor_name(device['src_ip'], device['src_mac'])
        port_scan_result = scan_port(device['src_ip']) if ports_scan else "None"
        device_os = detect_os_long(device['src_ip']) if os_detect else device['os']
        device = {**device,
                    'vendor': vendor_name,
                    'host_name': host_name,
                    'port_scan_result': port_scan_result,
                    'os': device_os,
                    }
        new_devices_dict[device['src_mac']] = device
    data = ProduceMessage(message=new_devices_dict)
    send_message(data.message)
      
def get_vendor_name(ip, mac):
    nm = nmap.PortScanner()
    try:
        nm.scan(hosts=ip, arguments='-sP')
        if mac not in nm[ip]['vendor'].keys():
            return "Unknown Vendor"
        else:
            vendor_name = nm[ip]['vendor'][mac]
            return vendor_name
    except Exception as e:
        print(f"Error occurred while scanning: {e}")
        return "Unknown Vendor"

def get_hostname_from_ip(ip):
    try:  
        hostname, _, _ = socket.gethostbyaddr(ip)      
        return hostname
    except socket.herror:
        return "Unknown Hostname"
    
def scan_port(host):
    open_ports = ''
    PORTS_TO_SCAN = [20,21,22,23,25,53,67,68,69,80,110,111,123,135,137,138,139,143,161,162,443,445,500,514,520,554,631,993,995,1434,1723,1900,3306,3389,4500,5900,8080,49152]
    print(f"Scanning ports on {host}...")
    try: 
        for port in PORTS_TO_SCAN:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.1)
            result = sock.connect_ex((host, port))
            if result == 0:
                open_ports += f"{port}: open, " 
            elif result == 10013:  # Connection refused
                open_ports += f"{port}: open but permission denied, "
            elif result == 10048:  # Address already in use
                open_ports += f"{port}: Address already in use, "
            elif result == 10054:  # Connection reset by peer
                open_ports += f"{port}: Connection reset by peer, "
            elif result == 10056:  # Port is already in use
                open_ports += f"{port}: already in use, "
            elif result == 10061:  # The target machine actively refused it
                open_ports += f"{port}: machine actively refused it, "
        try:
            r_http = requests.get(f"http://{host}/")
            if r_http.status_code == 200:
                open_ports += 'HTTP: service is running, '
            r_https = requests.get(f"https://{host}/")
            if r_https.status_code == 200:
                open_ports += 'HTTPS: service is running, '
        except requests.RequestException:
            open_ports += 'HTTPS: rejected by host, '
            return open_ports.strip(', ')
        return open_ports.strip(', ')
    except socket.error as e:
        print(f"Socket error: {e}")
    
def detect_os_fast(packet, tcp_window_size):
    if packet:
        if packet.payload.ttl <= 80 and tcp_window_size > 64000:
            return "Linux_Unix"
        elif packet.payload.ttl <= 140 and tcp_window_size > 64000:
            return "Windows"
        elif packet.payload.ttl <= 255 and tcp_window_size < 17000:
            return "Cisco_Solaris"
        else:
            return "Unknown OS"
        
def detect_os_long(ip):
    nm = nmap.PortScanner()
    print(f"Detecting Operating System for {ip}...")
    try:
        scan = nm.scan(hosts=ip, arguments='-O')
        if 'osmatch' in scan['scan'][ip]:
            return scan['scan'][ip]['osmatch'][0]['name']
        else:
            return "Unknown OS"
    except Exception as e:
        print(f"Error occurred while scanning: {e}")
        return "Unknown OS"