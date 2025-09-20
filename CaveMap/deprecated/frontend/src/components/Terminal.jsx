// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import { useState, useEffect, useRef } from 'preact/hooks'
import { Terminal as XTerm } from '@xterm/xterm'
import { FitAddon } from '@xterm/addon-fit'
import { WebLinksAddon } from '@xterm/addon-web-links'
import '@xterm/xterm/css/xterm.css'

export default function Terminal({ onCommand, isConnected, onConnect, onDisconnect }) {
  const terminalRef = useRef()
  const xtermRef = useRef()
  const fitAddonRef = useRef()
  const [showConnectForm, setShowConnectForm] = useState(false)
  const [connectionForm, setConnectionForm] = useState({
    host: '',
    username: '',
    password: '',
    port: 22
  })

  useEffect(() => {
    if (terminalRef.current && !xtermRef.current) {
      // Create xterm instance
      const xterm = new XTerm({
        cursorBlink: true,
        fontSize: 14,
        fontFamily: 'Consolas, "Courier New", monospace',
        theme: {
          background: '#000000',
          foreground: '#00ff00',
          cursor: '#00ff00'
        },
        allowProposedApi: true,
        convertEol: true
      })
      
      // Add addons
      const fitAddon = new FitAddon()
      xterm.loadAddon(fitAddon)
      xterm.loadAddon(new WebLinksAddon())
      
      // Open terminal
      xterm.open(terminalRef.current)
      fitAddon.fit()
      
      // Handle input - send all data directly to SSH
      xterm.onData((data) => {
        onCommand(data)
      })
      
      xtermRef.current = xterm
      fitAddonRef.current = fitAddon
    }
    
    return () => {
      if (xtermRef.current) {
        xtermRef.current.dispose()
        xtermRef.current = null
      }
    }
  }, [])

  // Handle incoming data from WebSocket
  useEffect(() => {
    const handleMessage = (event) => {
      if (xtermRef.current && event.detail && event.detail.payload) {
        const output = event.detail.payload.output
        if (output) {
          xtermRef.current.write(output)
        }
      }
    }
    
    window.addEventListener('ssh-output', handleMessage)
    return () => window.removeEventListener('ssh-output', handleMessage)
  }, [])

  const handleConnect = (e) => {
    e.preventDefault()
    onConnect(connectionForm)
    setShowConnectForm(false)
  }

  return (
    <div className="bg-gray-900 text-green-400 font-mono text-sm flex flex-col border border-gray-700 rounded-lg overflow-hidden h-full">
      <div className="bg-gradient-to-r from-gray-800 to-gray-700 px-4 py-3 border-b border-gray-600">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-3 h-3 bg-red-500 rounded-full"></div>
            <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
            <div className="w-3 h-3 bg-green-500 rounded-full"></div>
            <span className="text-white font-semibold ml-4">SSH Terminal</span>
          </div>
          <div className="flex items-center space-x-4">
            {!isConnected ? (
              <button
                onClick={() => setShowConnectForm(!showConnectForm)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-xs transition-colors"
              >
                Connect
              </button>
            ) : (
              <button
                onClick={onDisconnect}
                className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded text-xs transition-colors"
              >
                Disconnect
              </button>
            )}
            <div className="flex items-center space-x-2">
              <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500 animate-pulse' : 'bg-red-500'}`}></div>
              <span className="text-gray-300 text-xs">{isConnected ? 'Connected' : 'Disconnected'}</span>
            </div>
          </div>
        </div>
        
        {showConnectForm && (
          <form onSubmit={handleConnect} className="mt-4 p-4 bg-gray-800 rounded border border-gray-600">
            <div className="grid grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Host"
                value={connectionForm.host}
                onChange={(e) => setConnectionForm({...connectionForm, host: e.target.value})}
                className="bg-gray-700 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
                required
              />
              <input
                type="number"
                placeholder="Port"
                value={connectionForm.port}
                onChange={(e) => setConnectionForm({...connectionForm, port: parseInt(e.target.value)})}
                className="bg-gray-700 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
              />
              <input
                type="text"
                placeholder="Username"
                value={connectionForm.username}
                onChange={(e) => setConnectionForm({...connectionForm, username: e.target.value})}
                className="bg-gray-700 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={connectionForm.password}
                onChange={(e) => setConnectionForm({...connectionForm, password: e.target.value})}
                className="bg-gray-700 text-white px-3 py-2 rounded border border-gray-600 focus:border-blue-500 outline-none"
              />
            </div>
            <div className="text-xs text-gray-400 mt-2">
              💡 Tip: Use Ctrl+C to interrupt running commands like htop, top, etc.
            </div>
            <div className="flex justify-end space-x-2 mt-4">
              <button
                type="button"
                onClick={() => setShowConnectForm(false)}
                className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded text-sm transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded text-sm transition-colors"
              >
                Connect
              </button>
            </div>
          </form>
        )}
      </div>
      
      <div className="flex-1 flex flex-col min-h-0">
        <div 
          ref={terminalRef}
          className="flex-1 bg-black min-h-0"
        />
      </div>
    </div>
  )
}