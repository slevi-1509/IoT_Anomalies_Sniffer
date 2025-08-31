from openai import OpenAI
import os
import logging
import json
from dotenv import dotenv_values

logging.basicConfig(
    level=logging.INFO,
    # filename="server_ai.log",
    encoding="utf-8",
    # filemode="a",
    format="{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    )
logger = logging.getLogger(__name__)
env = dotenv_values('.env')
api_key = env.get("OPEN_AI_KEY") if not os.environ.get("OPEN_AI_KEY") else os.environ.get("OPEN_AI_KEY")

def get_openai_response(new_devices, data_queue):
    devices_from_file = {}
    if os.path.exists(env.get('DEVICES_FILE')):
        with open(env.get('DEVICES_FILE'), 'r') as file:
            devices_from_file = json.load(file) 
    devices_return_dict = {}
    for pack_sum in new_devices.values():
        if len(devices_from_file) > 0:
            if pack_sum['src_mac'] in devices_from_file:
                print(f"Device {pack_sum['src_mac']} already exists in the devices file.")
                continue
        if not pack_sum:
            print("Empty packet summary received")
            return "Empty packet summary received"

        # Format device info into prompt
        prompt = f"""
        Given the following device information from a local network, determine if it is likely an IoT device:

        Device Info:
        - IP: {pack_sum['src_ip']}
        - MAC: {pack_sum['src_mac']}
        - Vendor: {pack_sum['vendor']}
        - Hostname: {pack_sum['host_name']}
        - Detected Operating System: {pack_sum['os']}
        - Destination MAC Address: {pack_sum['dst_mac']}
        - Destination IP Address: {pack_sum['dst_ip']}
        - Destination Port: {pack_sum['dst_port']}
        - Source Port: {pack_sum['src_port']}
        - TTL: {pack_sum['ttl']}
        - TCP Window Size: {pack_sum['tcp_window_size']}
        - Ports and Services with scan status: {pack_sum['port_scan_result']}
`
        Is this device likely an IoT device?
        return a percentage number as an integer of probability that it is an IoT device and a short explanation
        (up to 500 characters) of the reasoning behind the probability result (separated by ::).
        """
        
        client = OpenAI(
            # api_key=os.environ.get("OPEN_AI_KEY"),
            api_key=api_key,
        )
        
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
        except Exception as e:
            logging.error(f"OpenAI API error: {e}")
            # log_file_path = "server_ai.log"
            # with open(log_file_path, 'a') as log_file:
            #     log_file.write(f"OpenAI API error: {e}\n")
            return "Error in OpenAI API request"
        try:
            is_iot = int(response.choices[0].message.content.split('::')[0].strip().replace('%', ''))
        except ValueError:
            is_iot = 0
            
        iot_reasoning = (response.choices[0].message.content.split('::')[1].strip())
        devices_return_dict[pack_sum['src_mac']] = {
            "src_ip": pack_sum['src_ip'],
            "src_mac": pack_sum['src_mac'],
            "vendor": pack_sum['vendor'],
            "host_name": pack_sum['host_name'],
            "port_scan_result": pack_sum['port_scan_result'],
            "os": pack_sum['os'],
            "ttl": pack_sum['ttl'],
            "tcp_window_size": pack_sum['tcp_window_size'],
            "is_iot": is_iot,
            "iot_reasoning": iot_reasoning
        }
    data_queue.put(write_devices_to_file(devices_return_dict))

def write_devices_to_file(devices):
    try:
        if os.path.exists(env.get('DEVICES_FILE')):
            with open(env.get('DEVICES_FILE'), 'r') as file:
                data = json.load(file)
        else:
            data = {}
        with open(env.get('DEVICES_FILE'), 'w') as file:
            for device in devices.values():
                data[device['src_mac']] = device
            json.dump(data, file, indent=4)
        return data
    except Exception as e:
        print(f"Error writing devices to file: {e}")