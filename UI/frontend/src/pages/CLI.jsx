import { useState, useEffect } from 'preact/hooks'
import Terminal from '../components/Terminal'
import { useSSHWebSocket } from '../lib/sshwebsocket'

// Global state to persist across tab switches
let globalIsConnected = false
let globalWebSocket = null

export default function CLI() {
  const [isConnected, setIsConnected] = useState(globalIsConnected)
  
  const { sendMessage } = useSSHWebSocket('ws://localhost:8000/ws/cli', {
    onMessage: (data) => {
      console.log('CLI received message:', data)
      if (data.type === 'cli_output') {
        // Forward to terminal component
        window.dispatchEvent(new CustomEvent('ssh-output', { detail: data }))
      } else if (data.type === 'ssh_status') {
        const connected = data.payload.status === 'connected'
        globalIsConnected = connected
        setIsConnected(connected)
        
        // Update navbar
        window.dispatchEvent(new CustomEvent('ssh-status-change', { detail: { connected } }))
      }
    }
  })
  
  // Store WebSocket globally
  useEffect(() => {
    globalWebSocket = sendMessage
  }, [sendMessage])

  const handleCommand = (data) => {
    // Send raw terminal data directly
    sendMessage({
      type: 'cli_command',
      payload: { command: data }
    })
  }

  const handleConnect = (connectionData) => {
    sendMessage({
      type: 'ssh_connect',
      payload: connectionData
    })
  }
  
  const handleDisconnect = () => {
    sendMessage({
      type: 'ssh_disconnect'
    })
    globalIsConnected = false
    setIsConnected(false)
    
    // Update navbar
    window.dispatchEvent(new CustomEvent('ssh-status-change', { detail: { connected: false } }))
  }

  return (
    <div className="bg-gradient-to-br from-gray-900 to-gray-800 flex flex-col w-full h-[calc(100vh-64px)] opacity-0 animate-[fadeIn_0.4s_ease-in-out_forwards] p-6">
      <div className="bg-gray-800 rounded-xl shadow-2xl w-full flex-1 flex flex-col border border-gray-700 min-h-0">
        <div className="bg-gradient-to-r from-gray-700 to-gray-600 p-6 rounded-t-xl border-b border-gray-600">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white text-xl font-bold">⚡</span>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">SSH Terminal</h2>
                <p className="text-gray-300 text-sm">Secure remote command execution</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <div className={`px-3 py-1 rounded-full text-xs font-medium ${
                isConnected 
                  ? 'bg-green-500/20 text-green-400 border border-green-500/30' 
                  : 'bg-red-500/20 text-red-400 border border-red-500/30'
              }`}>
                {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
              </div>
            </div>
          </div>
        </div>
        <div className="flex-1 p-6 min-h-0">
          <Terminal 
            onCommand={handleCommand} 
            isConnected={isConnected}
            onConnect={handleConnect}
            onDisconnect={handleDisconnect}
          />
        </div>
      </div>
    </div>
  )
}