import { useEffect, useRef } from 'preact/hooks'
import { initializeDesmos } from '../lib/desmos'
import { bot } from '../lib/bot'

export default function MapContainer() {
  const containerRef = useRef()
  const calculatorRef = useRef()

  useEffect(() => {
    console.log('MapContainer useEffect triggered')
    console.log('Container ref:', containerRef.current ? 'AVAILABLE' : 'NULL')
    console.log('Calculator ref:', calculatorRef.current ? 'EXISTS' : 'NULL')
    
    if (containerRef.current && !calculatorRef.current) {
      console.log('Initializing Desmos and setting up bot')
      calculatorRef.current = initializeDesmos(containerRef.current)
      bot.setCalculator(calculatorRef.current)
      console.log('Setup complete')
    }

    const handleResize = () => {
      console.log('Window resize triggered')
      if (calculatorRef.current && containerRef.current) {
        console.log('Resizing calculator')
        calculatorRef.current.resize()
      }
    }

    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])

  return (
    <main className="flex-1 flex flex-col items-center justify-center p-4 h-full min-w-0">
      <div className="bg-gray-800 p-6 rounded-lg shadow-lg w-full h-full flex flex-col items-center justify-center">
        <h2 className="text-xl font-semibold text-white mb-4">Minimap</h2>
        <div 
          ref={containerRef}
          className="bg-gray-600 relative w-full h-full min-h-[400px] min-w-[400px]"
        />
      </div>
    </main>
  )
}