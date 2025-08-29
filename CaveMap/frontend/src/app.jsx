// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import { useState, useEffect } from 'preact/hooks'
import { Router } from 'preact-router';
import Navbar from './components/Navbar'
import MapWindow from './pages/mapWindow';
import CLI from './pages/CLI';
import NotFound from './pages/NotFound';
import { useWebSocket } from './lib/readingswebsocket'
import { bot } from './lib/bot'
import { addpoints } from './lib/mapperlib'

export default function App() {
  const [logs, setLogs] = useState([])
  

  const { sendMessage } = useWebSocket('ws://localhost:8000/ws', {
    onMessage: (data) => {
      console.log('=== App WebSocket Message Received ===')
      console.log('Full data:', data)
      
      if (data.type === 'log') {
        setLogs(prev => [...prev, data])
      } else if (data.type === 'sensor_readings') {
        console.log('Processing sensor readings in App')
        addpoints(data)
      } else if (data.type === 'bot') {
        console.log('Processing bot command in App:', data.subtype)
        if (data.subtype === 'move') {
          console.log('Bot move command:', data.payload.distance)
          bot.move(data.payload.distance)
        } else if (data.subtype === 'rotate') {
          console.log('Bot rotate command:', data.payload.degrees)
          bot.rotate(data.payload.degrees)
        }
      }
      console.log('=== End App WebSocket Message ===')
    }
  })

  return (
    <div className="min-h-screen text-gray-800 bg-gray-900">
      <Navbar />
      <Router>
        <MapWindow logs={logs} path="/"/>
        <CLI path="/CLI"/>
        <NotFound default />
      </Router>
    </div>
  )
}