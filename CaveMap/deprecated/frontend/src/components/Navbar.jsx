// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import { useState, useEffect } from 'preact/hooks'
import { Link } from 'preact-router/match';

export default function Navbar() {
  const [picobatteryPercent, setpicoBatteryPercent] = useState(100)
  const [batteryPercent, setSPRKPRMBatteryPercent] = useState(100)
  const [botstatus, setbotstatus] = useState('connected')
  const [sshConnected, setSshConnected] = useState(false)
  
  useEffect(() => {
    const handleSSHStatusChange = (event) => {
      setSshConnected(event.detail.connected)
    }
    
    window.addEventListener('ssh-status-change', handleSSHStatusChange)
    return () => window.removeEventListener('ssh-status-change', handleSSHStatusChange)
  }, [])
  return (
    <nav className="bg-gray-950 p-4">
      <div className="flex justify-between items-center">
        <a href="#" className="text-white text-lg font-semibold hover:bg-gray-700 px-4 py-2 rounded-lg transition duration-300">
          CaveBot UI
        </a>
        
        <div className="flex items-center space-x-6">
          <div className="text-gray-300">
            <span className={`mr-4 px-3 py-1 rounded-full text-sm ${picobatteryPercent > 50 ? 'bg-green-700' : picobatteryPercent > 20 ? 'bg-yellow-600' : 'bg-red-600'}`}>Pico Battery: {picobatteryPercent}%</span>
            <span className={`mr-4 px-3 py-1 rounded-full text-sm ${batteryPercent > 50 ? 'bg-green-700' : batteryPercent > 20 ? 'bg-yellow-600' : 'bg-red-600'}`}>SPKPRM Battery: {batteryPercent}%</span>
            
            <span className={`mr-4 px-3 py-1 rounded-full text-sm ${botstatus === 'connected' ? 'bg-green-700' : 'bg-red-600'}`}>Bot: {botstatus}</span>
            <span className={`mr-4 px-3 py-1 rounded-full text-sm ${sshConnected ? 'bg-green-700' : 'bg-gray-600'}`}>SSH: {sshConnected ? 'connected' : 'disconnected'}</span>
            
          </div>
          
          <div className="flex bg-gray-800 rounded-lg overflow-hidden">
            <Link href="/" activeClassName="bg-blue-600 border-b-4 border-blue-600 !border-r !border-r-gray-700" className="cursor-pointer bg-gray-900 hover:bg-gray-700 text-white px-4 py-2 transition-all duration-500 border-r border-r-gray-700 flex items-center space-x-2">
              <span>🗺️</span>
              <span>Map</span>
            </Link>
            <Link href="/CLI" activeClassName="bg-blue-600 border-b-4 border-blue-600 !border-r !border-r-gray-700" className="cursor-pointer bg-gray-900 hover:bg-gray-700 text-white px-4 py-2 transition-all duration-500 border-r border-r-gray-700 flex items-center space-x-2">
              <span>⚡</span>
              <span>SSH</span>
            </Link>
            <Link href="/settings" activeClassName="bg-blue-600 border-b-4 border-blue-600" className="cursor-pointer bg-gray-900 hover:bg-gray-700 text-white px-4 py-2 transition-all duration-500">
              Settings
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}
