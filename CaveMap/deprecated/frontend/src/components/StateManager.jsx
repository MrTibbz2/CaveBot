// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

import { useState, useEffect } from 'preact/hooks'
import { api } from '../lib/api'

export default function StateManager() {
  const [states, setStates] = useState([])
  const [showSaveDialog, setShowSaveDialog] = useState(false)
  const [saveName, setSaveName] = useState('')
  const [saveDescription, setSaveDescription] = useState('')

  useEffect(() => {
    loadStates()
  }, [])

  const loadStates = async () => {
    try {
      const stateList = await api.listStates()
      setStates(stateList)
    } catch (error) {
      console.error('Failed to load states:', error)
    }
  }

  const handleSave = async () => {
    if (!saveName.trim()) return
    
    try {
      await api.saveState(saveName, saveDescription)
      setShowSaveDialog(false)
      setSaveName('')
      setSaveDescription('')
      loadStates()
    } catch (error) {
      console.error('Failed to save state:', error)
    }
  }

  const handleDelete = async (stateId) => {
    if (!confirm('Are you sure you want to delete this state?')) return
    
    try {
      await api.deleteState(stateId)
      loadStates()
    } catch (error) {
      console.error('Failed to delete state:', error)
    }
  }

  return (
    <div className="p-4 bg-gray-800 rounded-lg">
      <div className="flex justify-between items-center mb-4">
        <h3 className="text-lg font-semibold text-white">Saved States</h3>
        <button
          onClick={() => setShowSaveDialog(true)}
          className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700"
        >
          Save Current
        </button>
      </div>

      {showSaveDialog && (
        <div className="mb-4 p-3 bg-gray-700 rounded">
          <input
            type="text"
            placeholder="State name"
            value={saveName}
            onChange={(e) => setSaveName(e.target.value)}
            className="w-full p-2 mb-2 bg-gray-600 text-white rounded"
          />
          <textarea
            placeholder="Description (optional)"
            value={saveDescription}
            onChange={(e) => setSaveDescription(e.target.value)}
            className="w-full p-2 mb-2 bg-gray-600 text-white rounded h-20"
          />
          <div className="flex gap-2">
            <button
              onClick={handleSave}
              className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
            >
              Save
            </button>
            <button
              onClick={() => setShowSaveDialog(false)}
              className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="space-y-2 max-h-60 overflow-y-auto">
        {states.map((state) => (
          <div key={state.id} className="flex justify-between items-center p-2 bg-gray-700 rounded">
            <div className="flex-1">
              <div className="text-white font-medium">{state.name}</div>
              <div className="text-gray-400 text-sm">
                {new Date(state.created_at).toLocaleString()}
              </div>
              {state.description && (
                <div className="text-gray-300 text-sm">{state.description}</div>
              )}
            </div>
            <button
              onClick={() => handleDelete(state.id)}
              className="px-2 py-1 bg-red-600 text-white rounded hover:bg-red-700 text-sm"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}