import { useEffect, useState } from 'react'
import { Link } from "react-router-dom"
import { Stack } from "@mui/material"
import axios from 'axios'
import './App.css'

const Devices = () => {
    const SERVER_URL = 'http://localhost:8000'
    const [devices, setDevices] = useState({});
    const [deviceToShow, setDeviceToShow] = useState({});
    const [anomalies, setAnomalies] = useState([]);
    const [anomaliesToShow, setAnomaliesToShow] = useState([]);
    const [log, setLog] = useState([]);

    useEffect (() => {
        const getInfo = async () => {
            await axios.get(`${SERVER_URL}/devices`).then(({ data: response }) => {
            setDevices(Object.values({...response}));
            }).catch((error) => {
            console.log("d" + error.message);
            });

            await axios.get(`${SERVER_URL}/anomalies`).then(({ data: response }) => {
            if (typeof(response) == String)
                setAnomalies([]);
            setAnomalies(response.map(logItem => JSON.parse(logItem.replace(/'/g, '"'))));
            setAnomaliesToShow(response.map(logItem => JSON.parse(logItem.replace(/'/g, '"'))));
            }).catch((error) => {
                console.log("a" + error.message);
            });
        }
        getInfo();
    }, [])

    const handleSelect = async (e) => {
        let { value } = e.target;
        setDeviceToShow(devices.find(device => device.src_mac === value) || {});
        if (value === "Show All Anomalies") {
            setAnomaliesToShow(anomalies);
        } else {
            setAnomaliesToShow(anomalies.filter(anomaly => anomaly.src_mac === value));
        }
        await axios.get(`${SERVER_URL}/log/${value.replace(/:/g, "")}`).then(({ data: response }) => {
            if (typeof(response) == String)
                setLog([]);
            setLog(response.map(logItem => JSON.parse(logItem.replace(/'/g, '"'))));
        }).catch((error) => {
            console.log("a" + error.message);
        });
    }

    return (
        <div>
            <Stack spacing={1} direction="row">
                <Link to={'/'}>
                    Home
                </Link>
            </Stack>
            <h2>Devices and Anomalies Information</h2>
            { devices.length > 0 && 
                <section style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                    <label htmlFor="device">Select a device:</label>
                    <select name="device" id="device" onChange={handleSelect}>
                        <option>Show All Anomalies</option>
                        {devices.map((device_item, index) => (
                            <option key={index} value={`${device_item['src_mac']}`}>{`IP : ${device_item['src_ip']} / MAC : ${device_item['src_mac']} / IoT : ${device_item['is_iot']}%`}</option>
                        ))}
                    </select>
                </section> 
            }  
            <br/>
            {deviceToShow && Object.keys(deviceToShow).length > 0 &&
                <div style={{fontSize: '0.9rem', border: '3px solid darkgreen', width: '90%', maxWidth: '60rem'}}>
                    <h3>Device Information</h3>
                    <p><strong>IP:</strong> {deviceToShow.src_ip}</p>
                    <p><strong>MAC:</strong> {deviceToShow.src_mac}</p> 
                    <p><strong>IoT Probability:</strong> {deviceToShow.is_iot}%</p>
                    <p><strong>Host Name:</strong> {deviceToShow.host_name}</p>
                    <p><strong>Device OS:</strong> {deviceToShow.os}</p>
                    <p><strong>Ports Scan Result:</strong> {deviceToShow.port_scan_result}</p>
                    <p><strong>TTL:</strong> {deviceToShow.ttl}</p>
                    <p><strong>TCP Window Size:</strong> {deviceToShow.tcp_window_size}</p>
                    <p><strong>IoT AI Reasoning:</strong> {deviceToShow.iot_reasoning}</p>
                </div>
            }
            <br/>
            <h3>Anomalies:</h3>   
            { anomaliesToShow.length > 0 ? (
                <table style={{fontSize: '0.7rem', width: '95%', borderCollapse: 'collapse'}}>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>s-mac</th>
                            <th>s-ip</th>
                            <th>d-mac</th>
                            <th>d-ip</th>
                            <th>protocol</th>
                            <th>dns_qry</th>
                        </tr>
                    </thead>
                    <tbody>
                    {anomaliesToShow.map((anomaly, index) => (
                        <tr key={index} >
                            <td>{anomaly.timestamp}</td>
                            <td>{anomaly.src_mac}</td>
                            <td>{anomaly.src_ip}</td>
                            <td>{anomaly.dst_mac}</td>
                            <td>{anomaly.dst_ip}</td>
                            <td>{anomaly.protocol}</td>
                            <td>{anomaly.dns_query}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            ) : (
              <p>No anomalies found.</p>
            )}  
            <br/> 
            <h3>Log (Packets Summary):</h3>   
            { log.length > 0 ? (
                <table style={{fontSize: '0.7rem', width: '95%', borderCollapse: 'collapse'}}>
                    <thead>
                        <tr>
                            <th>Time</th>
                            <th>s-mac</th>
                            <th>s-ip</th>
                            <th>d-mac</th>
                            <th>d-ip</th>
                            <th>protocol</th>
                            <th>dns_qry</th>
                        </tr>
                    </thead>
                    <tbody>
                    {log.map((logItem, index) => (
                        <tr key={index} >
                            <td>{logItem.timestamp}</td>
                            <td>{logItem.src_mac}</td>
                            <td>{logItem.src_ip}</td>
                            <td>{logItem.dst_mac}</td>
                            <td>{logItem.dst_ip}</td>
                            <td>{logItem.protocol}</td>
                            <td>{logItem.dns_query}</td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            //   <div>
            //     {log.map((logItem, index) => (
            //       <div key={index} style={{fontSize: '12px', border: '1px solid blue', width: '80%'}}>
            //       <p className="log-text">{logItem}</p>
            //       </div>
            //     ))}

            //   </div>
            ) : (
              <p>No log found.</p>
            )}       
        </div>
    );
};

export default Devices;