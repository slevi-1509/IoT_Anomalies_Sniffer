import { useEffect, useState } from 'react'
import { Link, Outlet, useNavigate } from "react-router-dom"
import { Stack, Button } from "@mui/material"
import Slider from '@mui/material/Slider'
import axios from 'axios'
import './App.css'

const HomePage = () => {
  const SERVER_URL = 'http://localhost:8000'
  const [interfaces, setInterfaces] = useState([]);
  const [devices, setDevices] = useState({});
  const [devicesToShow, setDevicesToShow] = useState({});
  const [anomalies, setAnomalies] = useState([]);
  const [anomaliesToShow, setAnomaliesToShow] = useState([]);
  const [parameters, setParameters] = useState({});
  const [portsScan, setPortsScan] = useState(false);
  const [osDetect, setOsDetect] = useState(false);
  const [iotProbability, setIotProbability] = useState(50)

  useEffect (() => {
    const getInfo = async () => {
        // debugger;
        await axios.get(`${SERVER_URL}/interfaces`).then(({ data: response }) => {
          response = response.filter(item => item.ip !== "")
          setInterfaces(response);
          setParameters({'interface': response[0]['interface'],
                          'interval': 0,
                          'no_of_packets': 10,
                          'no_of_sessions': 1,
                          'collect_data_time': 3600,
                          'ports_scan': false,
                          'os_detect': false});
        }).catch((error) => {
          console.log("i" + error.message);
        });
        await axios.get(`${SERVER_URL}/devices`).then(({ data: response }) => {
          // debugger
          setDevicesToShow(Object.values({...response}));
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

  const handleSelect = (e) => {
    let { value, name } = e.target;
    if (['interval', 'no_of_packets', 'no_of_sessions', 'collect_data_time'].includes(name)) {
      value = parseInt(value);
    }
    setParameters({...parameters, [name]: value})
    console.log(parameters)
  }

  const handleChecked = (e) => {
    let { checked, name } = e.target;
    switch (name) {
      case 'ports_scan':
        setPortsScan(checked);
        break;
      case 'os_detect':
        setOsDetect(checked);
        break;
      default:
        break;
    }
    setParameters({...parameters, [name]: checked})
    console.log(parameters)
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    // let send_params = {'interface': parameters.interface? parameters.interface : interfaces[0]['interface'],
    //                     'interval': parseInt(parameters.interval)? parseInt(parameters.interval) : 0,
    //                     'no_of_packets': parseInt(parameters.no_of_packets)? parseInt(parameters.no_of_packets) : 10,
    //                     'no_of_sessions': parseInt(parameters.no_of_sessions)? parseInt(parameters.no_of_sessions) : 1}
    // console.log(send_params);
    parameters['iot_probability'] = iotProbability;
    try {
      let response = await axios.post(`${SERVER_URL}/runsniffer`, parameters);
    } catch (error) {
      console.log(error.message);
    }
  }

  const handle_device_click = async (device) => {
    let device_anomalies = [];
    let { src_mac } = device;
    setAnomaliesToShow(anomalies.filter(anomaly => anomaly.src_mac === src_mac));
  }
  
  const handleIotChange = (e) => {
    let devices_iot = [];
    let { value } = e.target;
    setIotProbability(value);
    setParameters({...parameters, 'iot_probability': value});
    for (let device of devices) {
      let device_iot = device.is_iot;
      if (device_iot >= iotProbability) {
        devices_iot.push(device);
      }
      setDevicesToShow([...devices_iot]);
    }
  }

  return (
    <>
      <Stack spacing={1} direction="row">
          <Link to={'devices'}>
              Devices
          </Link>
      </Stack>
      <h1>My Python Sniffer Client</h1>
      <br/>
      {interfaces && 
        <div>
          <section style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <h3>Interface List</h3>
            <label htmlFor="interface">Select an interface:</label>
            <select name="interface" id="interface" onChange={handleSelect}>
              {interfaces.map((interface_item, index) => (
                <option key={index} value={`${interface_item['interface']}`}>{`${index}: ${interface_item['interface']} - ${interface_item['ip']}`}</option>
              ))}
            </select>
          </section>
          <br/>
          <section style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <h3>Options:</h3>
            <label htmlFor="interval">Set interval (seconds): </label>
            <input type="number" id="interval" name="interval" defaultValue='0' min="0" onChange={handleSelect} />
            <label htmlFor="no_of_packets">Set number of packets: </label>
            <input type="number" id="no_of_packets" name="no_of_packets" defaultValue='10' min="1" onChange={handleSelect} />
            <label htmlFor="no_of_sessions">Set number of sessions (0 for infinite): </label>
            <input type="number" id="no_of_sessions" name="no_of_sessions" defaultValue='1' min="1" onChange={handleSelect} />
            <label htmlFor="collect_data_time">Set collection data time for anomalies (seconds): </label>
            <input type="number" id="collect_data_time" name="collect_data_time" defaultValue='3600' min="600" onChange={handleSelect} />
            <label><input type="checkbox" name="ports_scan" checked={portsScan} onChange={handleChecked} /> Ports Scanning</label>
            <label><input type="checkbox" name="os_detect" checked={osDetect} onChange={handleChecked} /> Deep OS detection (slower)</label>
            <div className="slidecontainer" style={{width: "12rem"}}>
                <label htmlFor="iot-probability" style={{fontSize: '0.9rem'}}>Minimum IoT Probability: <strong>{iotProbability}</strong></label>
                <div id="iot-probability">
                  <Slider 
                      name="iot-probability"
                      min={0}
                      max={100}
                      step={1}
                      aria-label="IoT Probability"
                      value={iotProbability}
                      valueLabelDisplay="auto"
                      onChange={handleIotChange} 
                  />
                </div>
            </div>
            <button type="submit" value="Submit" onClick={handleSubmit}> Submit </button>
          </section>
          <br/>
          <div
            style={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
            <h3>Devices:</h3>
            {devicesToShow.length > 0 ? (
              <table style={{fontSize: '0.7rem', width: '95%', borderCollapse: 'collapse'}}>
                <thead>
                  <tr>
                    <th>Mac</th>
                    <th>IP</th>
                    <th>OS</th>
                    <th>Vendor</th>
                    <th>Hostname</th>
                    <th>is_IoT</th>
                  </tr>
                </thead>
                <tbody>
                {devicesToShow.map((device, index) => (
                  <tr key={index} onClick={() => handle_device_click(device)}>
                    <td style={{cursor: 'pointer'}}>{device.src_mac}</td>
                    <td>{device.src_ip}</td>
                    <td>{device.os}</td>
                    <td>{device.vendor}</td>
                    <td>{device.host_name}</td>
                    <td>{device.is_iot}%</td>
                  </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              <p>No devices found.</p>
            )}
            <br/>
            <h3>Anomalies:</h3>
            <button type="button" onClick={()=>{setAnomaliesToShow(anomalies)}}>Show All</button>
            <br/>
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
            //   <div>
            //     {anomaliesToShow.map((anomaly, index) => (
            //       <div key={index} style={{fontSize: '12px', border: '1px solid red', width: '80%', maxWidth: '30rem'}}>
            //       <p className="anomaly-text" style={{cursor: 'pointer'}} onClick={() => handleAnomalyClick(anomaly)}>{anomaly}</p>
            //       </div>
            //     ))}

            //   </div>
            ) : (
              <p>No anomalies found.</p>
            )}  
            <br/> 
          </div>
        </div>      }
    </>
  )
}

export default HomePage;
