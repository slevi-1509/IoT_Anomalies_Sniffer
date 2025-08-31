import './App.css'
import { Routes, Route } from "react-router-dom"
import 'bootstrap/dist/css/bootstrap.css';
import 'bootstrap/dist/js/bootstrap.js';
import Devices from './Devices'
import HomePage from './HomePage'


function App() {

  // APP_PORT = 3300;

  // SERVER_IP = "http://localhost:";
  // DEVICES_URL = SERVER_IP+APP_PORT+"/devices";
  // MAIN_URL = SERVER_IP+APP_PORT+"/";

  return (
    <div>
      <Routes>
        <Route path='/' element={<HomePage />} />
        <Route path='/devices' element={<Devices />} />
      </Routes>
    </div>
)}

export default App


    
