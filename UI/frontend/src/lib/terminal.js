// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import { useEffect, useRef } from 'preact/hooks'

export function useTerminal(onCommand) {
  const terminalRef = useRef()
  const inputRef = useRef()
  const historyRef = useRef([])
  const historyIndexRef = useRef(-1)

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Enter') {
        e.preventDefault()
        const command = inputRef.current.value.trim()
        if (command) {
          addToHistory(command)
          onCommand(command)
          inputRef.current.value = ''
        }
      } else if (e.key === 'c' && e.ctrlKey) {
        e.preventDefault()
        onCommand('^C')
      } else if (e.key === 'ArrowUp') {
        e.preventDefault()
        navigateHistory(-1)
      } else if (e.key === 'ArrowDown') {
        e.preventDefault()
        navigateHistory(1)
      }
    }

    const addToHistory = (command) => {
      historyRef.current.push(command)
      historyIndexRef.current = -1
    }

    const navigateHistory = (direction) => {
      const history = historyRef.current
      if (history.length === 0) return

      historyIndexRef.current += direction
      if (historyIndexRef.current < -1) historyIndexRef.current = -1
      if (historyIndexRef.current >= history.length) historyIndexRef.current = history.length - 1

      if (historyIndexRef.current === -1) {
        inputRef.current.value = ''
      } else {
        inputRef.current.value = history[history.length - 1 - historyIndexRef.current]
      }
    }

    const input = inputRef.current
    if (input) {
      input.addEventListener('keydown', handleKeyDown)
      return () => input.removeEventListener('keydown', handleKeyDown)
    }
  }, [onCommand])

  const scrollToBottom = () => {
    if (terminalRef.current) {
      setTimeout(() => {
        terminalRef.current.scrollTop = terminalRef.current.scrollHeight
      }, 0)
    }
  }

  return { terminalRef, inputRef, scrollToBottom }
}