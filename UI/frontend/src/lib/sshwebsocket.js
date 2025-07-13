import { useEffect } from 'preact/hooks'

// Global WebSocket instance
let globalSSHWebSocket = null
let globalMessageHandlers = new Set()

export function useSSHWebSocket(url, options = {}) {
  const { onMessage, onOpen, onClose } = options

  useEffect(() => {
    // Add message handler to global set
    if (onMessage) {
      globalMessageHandlers.add(onMessage)
    }

    // Create WebSocket only if it doesn't exist
    if (!globalSSHWebSocket || globalSSHWebSocket.readyState === WebSocket.CLOSED) {
      console.log(`SSH WebSocket connecting to: ${url}`)
      globalSSHWebSocket = new WebSocket(url)

      globalSSHWebSocket.onopen = () => {
        console.log(`SSH WebSocket connected: ${url}`)
        onOpen?.()
      }

      globalSSHWebSocket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data)
          // Send to all registered handlers
          globalMessageHandlers.forEach(handler => handler(data))
        } catch (error) {
          console.error('SSH WebSocket parse error:', error)
        }
      }

      globalSSHWebSocket.onerror = (error) => {
        console.error('SSH WebSocket error:', error)
      }

      globalSSHWebSocket.onclose = (event) => {
        console.log(`SSH WebSocket closed: ${url}`)
        onClose?.()
      }
    }

    return () => {
      // Remove message handler when component unmounts
      if (onMessage) {
        globalMessageHandlers.delete(onMessage)
      }
    }
  }, [url])

  const sendMessage = (data) => {
    if (globalSSHWebSocket?.readyState === WebSocket.OPEN) {
      globalSSHWebSocket.send(JSON.stringify(data))
    }
  }

  return { sendMessage }
}