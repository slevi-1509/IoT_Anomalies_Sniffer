active_interfaces = []
registered_devices = {}
total_new_devices = {}
anomalies = []
ANOMALIES_LOG = "anomalies.log"
LOGS_DIR = "./logs/"
CONFIG_FILE = "config.json"
DEVICES_FILE = "devices.json"
KAFKA_URL = '3.81.72.149:9092'
# KAFKA_URL = 'localhost:9092'
# KAFKA_URL = '192.168.1.95:9093'
# ANOMALIES_FILE = "anomalies.json"
SERVER_AI_URL = "http://192.168.1.95:8002"
PORTS_TO_SCAN = [20,21,22,23,25,53,67,68,69,80,110,111,123,135,137,138,139,143,161,162,443,445,500,514,520,554,631,993,995,1434,1723,1900,3306,3389,4500,5900,8080,49152]

