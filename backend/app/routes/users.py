from fastapi import APIRouter ,Request
from scapy import interfaces
import os
import config
from models.Interfaces import InterfaceClass
from models.SubmitFromUser import SubmitFromUser
from utils.utils import start_sniffer

router = APIRouter()

@router.get("/")
def read_root(request: Request):
    return {"message": "Welcome to the API "}

@router.get("/interfaces", response_model=list[InterfaceClass])
def getInterfaces(request: Request):
    return config.active_interfaces

@router.get("/devices")
def getDevices(request: Request):
    # print(type(request.app.state.devices))
    return config.registered_devices

@router.get("/anomalies")
def getAnomalies(request: Request, response_model=list[str]):
    anomalies = []
    if os.path.exists(config.ANOMALIES_LOG):
        with open(config.ANOMALIES_LOG, 'r') as file:
            for anomaly in file.readlines():
                anomalies.append(anomaly.strip())
    return anomalies

@router.get("/log/{mac}")
def getDeviceLog(request: Request, mac: str, response_model=list[str]):
    device_log = []
    if os.path.exists(config.LOGS_DIR + mac + ".log"):
        with open(config.LOGS_DIR + mac + ".log", 'r') as file:
            for log in file.readlines():
                device_log.append(log.strip())
    return device_log

@router.post("/runsniffer")
def startSniffer(params: SubmitFromUser, request: Request):
    found_working_interfaces = interfaces.get_working_ifaces()
    for interface_item in found_working_interfaces:
        if params.interface == interface_item.name:
            interface = interface_item
            break
    start_sniffer(interface, params)
    return {"message": "Sniffer started successfully", "interface": interface.name}