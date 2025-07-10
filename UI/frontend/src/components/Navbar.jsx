import { useState } from 'preact/hooks'


export default function Navbar() {
  const [picobatteryPercent, setpicoBatteryPercent] = useState(100)
  const [batteryPercent, setSPRKPRMBatteryPercent] = useState(100)
  const [botstatus, setbotstatus] = useState('connected')
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
            
            <span className={`mr-4 px-3 py-1 rounded-full text-sm ${botstatus === 'connected' ? 'bg-green-700' : 'bg-red-600'}`}>Status: {botstatus}</span>
            
          </div>
          
          <div className="flex space-x-4">
            <button className="bg-gray-900 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition duration-300">
              map
            </button>
            <button className="bg-gray-900 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition duration-300">
              CLI
            </button>
            <button className="bg-gray-900 hover:bg-gray-700 text-white px-4 py-2 rounded-lg transition duration-300">
              Settings
            </button>
          </div>
        </div>
      </div>
    </nav>
  )
}
