from kafka import KafkaProducer
from dotenv import dotenv_values
import json
from produce_schema import ProduceMessage

env = dotenv_values('.env')

KAFKA_BROKER_URL = "3.81.72.149:9093"
KAFKA_TOPIC = 'reply_from_ai_request'
PRODUCER_CLIENT_ID = 'fastapi_producer'

def create_kafka_producer():    
    producer = KafkaProducer(
        bootstrap_servers=[KAFKA_BROKER_URL],
        # client_id=PRODUCER_CLIENT_ID,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Serialize JSON messages
    )
    return producer

def produce_kafka_message(messageRequest: ProduceMessage):
    try:
        producer = create_kafka_producer()
        # json_data = json.dumps(messageRequest.message).encode('utf-8')
        print("Returning AI results to determine if devices are IoT")
        producer.send(KAFKA_TOPIC, messageRequest.message)
    except KeyboardInterrupt:
        pass
    finally:
        producer.flush()
        producer.close()

message = {
    "30:9C:23:74:6B:9B": {
        "src_ip": "192.168.1.81",
        "src_mac": "30:9C:23:74:6B:9B",
        "vendor": "Unknown Vendor",
        "host_name": "host.docker.internal",
        "port_scan_result": "None",
        "os": "Cisco_Solaris",
        "ttl": 128,
        "tcp_window_size": 252,
        "is_iot": 25,
        "iot_reasoning": "The device information does not provide enough explicit details to confidently determine if it is an IoT device. It's detected operating system is Cisco_Solaris which is commonly used in network devices and could potentially be used in an IoT device, but without additional clarification on the functionality of the device or specific IoT characteristics, it's only possible to make a low confident guess. Also, the hostname suggests that it could be a Docker instance running on a server rather than a typical IoT device."
    },
    "08:54:BB:A1:2B:A3": {
        "src_ip": "192.168.1.16",
        "src_mac": "08:54:BB:A1:2B:A3",
        "vendor": "Shenzhen Chuangwei-RGB Electronics",
        "host_name": "Unknown Hostname",
        "port_scan_result": "None",
        "os": "Cisco_Solaris",
        "ttl": 64,
        "tcp_window_size": 981,
        "is_iot": 60,
        "iot_reasoning": "The vendor \"Shenzhen Chuangwei-RGB Electronics\" is known for manufacturing IoT devices such as smart home appliances. However, the detected operating system \"Cisco_Solaris\" is usually found in more industrial or enterprise systems, making it less common in traditional consumer-grade IoT devices. Given the mixture of these characteristics, it can be likely an IoT device but not enough information to guarantee it."
    },
    "A4:22:49:64:D9:2A": {
        "src_ip": "192.168.1.78",
        "src_mac": "A4:22:49:64:D9:2A",
        "vendor": "Sagemcom Broadband SAS",
        "host_name": "HOTStreamerV3-d92a",
        "port_scan_result": "None",
        "os": "Cisco_Solaris",
        "ttl": 64,
        "tcp_window_size": 348,
        "is_iot": 50,
        "iot_reasoning": "The device information is ambiguous. It could be an IoT device, as the vendor Sagemcom Broadband SAS produces devices that connect to the internet, including IoT devices. However, the detected operating system is Cisco_Solaris, an operating system typically used for enterprise server systems, not usually associated with IoT devices. Hence, it's uncertain whether this is an IoT device or not."
    },
    "00:12:43:4D:44:58": {
        "src_ip": "192.168.1.80",
        "src_mac": "00:12:43:4D:44:58",
        "vendor": "Cisco Systems",
        "host_name": "Unknown Hostname",
        "port_scan_result": "None",
        "os": "Cisco_Solaris",
        "ttl": 64,
        "tcp_window_size": 0,
        "is_iot": 60,
        "iot_reasoning": "The device could potentially be an IoT device given it's from Cisco Systems, a manufacturer known for producing IoT devices. However, the lack of any ports or services and the fact it's using a Cisco_Solaris system (which is typically used for enterprise-level network equipment like routers, switches or firewalls) may suggest it could also be network equipment. Therefore, there's a moderate possibility but not certainly an IoT device."
    },
    "94:98:8F:D7:B2:FC": {
        "src_ip": "192.168.1.31",
        "src_mac": "94:98:8F:D7:B2:FC",
        "vendor": "Sagemcom Broadband SAS",
        "host_name": "HOTStreamerV3-b2fc",
        "port_scan_result": "None",
        "os": "Cisco_Solaris",
        "ttl": 64,
        "tcp_window_size": 359,
        "is_iot": 30,
        "iot_reasoning": "This device has a small chance of being an IoT device. Sagemcom Broadband SAS is a high-speed broadband and digital TV vendor. While it's possible that it is an IoT device like a smart TV or a modem/router combo, the detected operating system being Cisco_Solaris indicates that the device might be a networking or telecommunication device rather than an IoT device. However, more concrete data would be required to give a solid answer."
    },
    "4C:6B:B8:E5:DB:EB": {
        "src_ip": "192.168.1.75",
        "src_mac": "4C:6B:B8:E5:DB:EB",
        "vendor": "Hui Zhou Gaoshengda Technology",
        "host_name": "Unknown Hostname",
        "port_scan_result": "None",
        "os": "Cisco_Solaris",
        "ttl": 64,
        "tcp_window_size": 0,
        "is_iot": 85,
        "iot_reasoning": "This device is likely an IoT device. The vendor \"Hui Zhou Gaoshengda Technology\" is a known manufacturer of IoT devices. However, the operating system \"Cisco_Solaris\" is not typically associated with IoT devices, but it's not uncommon for IoT devices to run different operating systems. Furthermore, the other details given (including IP, MAC, destination IPs and MACs, Ports, TTL etc.) don't necessarily offer any strong indicators against this device being an IoT device. Based on this information, it's likely but not certainly an IoT device."
    },
    "94:98:8F:D8:37:AE": {
        "src_ip": "192.168.1.28",
        "src_mac": "94:98:8F:D8:37:AE",
        "vendor": "Sagemcom Broadband SAS",
        "host_name": "HOTStreamerV3-37ae",
        "port_scan_result": "HTTPS: rejected by host",
        "os": "Android 10 - 12 (Linux 4.14 - 4.19)",
        "ttl": 255,
        "tcp_window_size": 0,
        "is_iot": 75,
        "iot_reasoning": "The device seems to be a media streaming device, likely an IPTV or a smart TV, given the hostname \"HOTStreamerV3-37ae\" and the detected operating system Android 10 - 12, which is often used in such smart devices. Sagemcom Broadband SAS, the vendor, also commonly designs and manufactures communications equipment which often includes IoT devices. However, without more specific information, it is not guaranteed to be an IoT device."
    },
    "00:5F:67:EA:9E:78": {
        "src_ip": "192.168.1.254",
        "src_mac": "00:5F:67:EA:9E:78",
        "vendor": "TP-Link Limited",
        "host_name": "Unknown Hostname",
        "port_scan_result": "80: open, 443: open, HTTP: service is running, HTTPS: rejected by host",
        "os": "OpenWrt 19.07 (Linux 4.14)",
        "ttl": 1,
        "tcp_window_size": 0,
        "is_iot": 90,
        "iot_reasoning": "The presence of the OpenWrt operating system (which is often used with embedded devices), the vendor being TP-Link (known for creating IoT devices), as well routing indications such as a TTL of 1 (commonly used in hand-held devices like IoTs), and the network services that are running imply that this device is likely an IoT. However, lack of certain information like device model and specific use keeps the certainty below 100%."
    },
    "58:FC:20:1D:87:BF": {
        "src_ip": "192.168.1.1",
        "src_mac": "58:FC:20:1D:87:BF",
        "vendor": "Altice Labs",
        "host_name": "GEN8",
        "port_scan_result": "22: open, 53: open, 80: open, 139: open, 443: open, 445: open, 49152: open, HTTPS: rejected by host",
        "os": "Linux 3.2 - 4.14",
        "ttl": 64,
        "tcp_window_size": 0,
        "is_iot": 85,
        "iot_reasoning": "The device is likely an IoT device because it runs on a Linux operating system which is commonly used in IoT devices. Also, the vendor, Altice Labs, is known for creating IoT devices. The device has several ports open which are commonly used by IoT devices, such as ports 22, 80, and 443. Additionally, the destination IP address suggests that it's using multicast addressing which is a typical feature used by IoT devices."
    },
    "50:EB:71:93:13:2C": {
        "src_ip": "192.168.1.68",
        "src_mac": "50:EB:71:93:13:2C",
        "vendor": "Intel Corporate",
        "host_name": "SAGIV-BEDROOM",
        "port_scan_result": "135: open, 139: open, 445: open, 3389: open, 5900: open, HTTPS: rejected by host",
        "os": "Microsoft Windows 11 21H2",
        "ttl": 1,
        "tcp_window_size": 0,
        "is_iot": 10,
        "iot_reasoning": "The device is likely not an IoT device. The detected operating system is Microsoft Windows 11, which is typically used for desktops and laptops, not IoT devices. The hostname suggests that it's a device in someone's bedroom, hinting it could be a personal computer. Also, the open ports indicate services like RDP, SMB, potentially VNC (used for remote desktop), which are more typical for a workstation or server device rather than an IoT device. Hence, it is more probable that this is a personal computer rather than an IoT device."
    }
}

produce_kafka_message(ProduceMessage(message=message))

