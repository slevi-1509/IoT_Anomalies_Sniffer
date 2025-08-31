import uvicorn
from fastapi import FastAPI
from scapy import interfaces
from fastapi.middleware.cors import CORSMiddleware
import threading
import json
import os
from routes import users
from kafka_consumer.consumer import consume_messages
import config

app = FastAPI(title="Sniffer API", version="1.0.0", 
              description="API for Sniffer application")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)

def get_interfaces():
    found_working_interfaces = interfaces.get_working_ifaces()
    for interface in found_working_interfaces:
        config.active_interfaces.append({'interface': interface.name, 'ip': interface.ip})
    return config.active_interfaces

def get_registered_devices():

    if os.path.exists(config.DEVICES_FILE):
        try:
            with open(config.DEVICES_FILE, "r") as file:
                config.registered_devices = json.load(file)
        except Exception as e:
            print(f"Error reading devices file: {e}")
    return config.registered_devices

def main():
    get_interfaces()
    get_registered_devices()
    thread = threading.Thread(target=consume_messages)
    thread.start()
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
    thread.join()
    # consume_messages()
    
if __name__ == "__main__":
    main()
