import { useEffect, useRef } from 'preact/hooks'

export function useWebSocket(url, options = {}) {
  const wsRef = useRef()
  const { onMessage, onOpen, onClose } = options

  useEffect(() => {
    console.log(`Attempting WebSocket connection to: ${url}`)
    const ws = new WebSocket(url)
    wsRef.current = ws

    ws.onopen = () => {
      console.log(`✅ WebSocket connected successfully: ${url}`)
      onOpen?.()
    }

    ws.onmessage = (event) => {
      console.log('Raw WebSocket message received:', event.data)
      try {
        const safeData = event.data.replace(/:Infinity/g, ':null')
        console.log('Processed WebSocket data:', safeData)
        const data = JSON.parse(safeData)
        console.log('Parsed WebSocket data:', data)
        onMessage?.(data)
      } catch (error) {
        console.error('❌ WebSocket message parse error:', error)
        console.error('Raw data that failed:', event.data)
      }
    }

    ws.onerror = (error) => {
      console.error('❌ WebSocket error:', error)
    }

    ws.onclose = (event) => {
      console.log(`❌ WebSocket closed: ${url}`, event.code, event.reason)
      onClose?.()
    }

    return () => {
      console.log(`Closing WebSocket connection: ${url}`)
      ws.close()
    }
  }, [url])

  const sendMessage = (data) => {
    console.log('Attempting to send WebSocket message:', data)
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      console.log('✅ Sending WebSocket message')
      wsRef.current.send(JSON.stringify(data))
    } else {
      console.error('❌ WebSocket not ready for sending. State:', wsRef.current?.readyState)
    }
  }

  return { sendMessage }
}