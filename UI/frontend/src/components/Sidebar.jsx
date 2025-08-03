// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import { useState, useRef, useEffect } from 'preact/hooks'

export default function Sidebar({ logs }) {
  const [width, setWidth] = useState(288) // 18rem
  const [isResizing, setIsResizing] = useState(false)
  const [isCollapsed, setIsCollapsed] = useState(false)
  const [previousWidth, setPreviousWidth] = useState(288) // Store previous width before collapsing
  const logContainerRef = useRef()

  useEffect(() => {
    if (logContainerRef.current) {
      logContainerRef.current.scrollTop = logContainerRef.current.scrollHeight
    }
  }, [logs])

  const handleMouseDown = (e) => {
    setIsResizing(true)
    document.body.style.cursor = 'col-resize'
    document.body.style.userSelect = 'none'
  }

  const handleMouseMove = (e) => {
    if (!isResizing) return
    const newWidth = Math.max(192, Math.min(e.clientX, 512))
    setWidth(newWidth)
  }

  const handleMouseUp = () => {
    setIsResizing(false)
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
  }

  const toggleSidebar = () => {
    if (isCollapsed) {
      setWidth(previousWidth)
    } else {
      setPreviousWidth(width)
      setWidth(50) // Collapsed width
    }
    setIsCollapsed(!isCollapsed)
  }

  useEffect(() => {
    if (isResizing) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [isResizing])

  return (
    <div
      className="bg-gray-600 relative flex-shrink-0"
      style={{
        width: `${isCollapsed ? 50 : width}px`,
        transition: isResizing ? 'none' : 'width 0.3s ease-in-out',
      }}
    >
      <aside className="h-full bg-gray-800 p-6 shadow-lg space-y-6 flex flex-col justify-stretch w-full">
        <button
          onClick={toggleSidebar}
          className="absolute top-1/2 -translate-y-1/2 right-0 transform translate-x-full bg-gray-700 hover:bg-gray-600 text-white p-2 rounded-r-md shadow-lg z-20"
          style={{ display: isCollapsed ? 'block' : 'block' }}
        >
          {isCollapsed ? '>' : '<'}
        </button>
        {!isCollapsed && (
          <>
            <section className="bg-gray-900 p-4 rounded-lg shadow-sm flex-1 flex flex-col">
              <h2 className="text-lg font-semibold text-gray-100 mb-3">Logs</h2>
              <div
                ref={logContainerRef}
                className="text-sm text-gray-300 max-h-48 overflow-y-auto border border-gray-700 p-2 rounded bg-gray-800"
              >
                {logs.map((log, i) => (
                  <div key={i} className="log-entry">
                    {log.timestamp} - type: {log.subtype}, message: {log.payload.message}
                  </div>
                ))}
              </div>
            </section>
            {/* <section className="bg-gray-900 p-4 rounded-lg shadow-sm flex-none">
              <h2 className="text-lg font-semibold text-gray-100 mb-3">Commands</h2>
              <div className="flex flex-col space-y-3">
                <button className="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-md">
                  Start Bot
                </button>
                <button className="w-full bg-red-600 hover:bg-red-700 text-white font-bold py-2 px-4 rounded-md">
                  Stop Bot
                </button>
              </div>
            </section> */}
          </>
        )}
      </aside>
      {!isCollapsed && (
        <div
          className="absolute top-0 right-0 h-full w-2 cursor-col-resize bg-black opacity-50 hover:opacity-80 z-10"
          onMouseDown={handleMouseDown}
        />
      )}
    </div>
  )
}
