// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

const API_BASE = '';

export const api = {
  // State management
  async getCurrentState() {
    const response = await fetch(`${API_BASE}/api/state`);
    return response.json();
  },

  async listStates() {
    const response = await fetch(`${API_BASE}/api/states`);
    return response.json();
  },

  async saveState(name, description = '') {
    const response = await fetch(`${API_BASE}/api/states`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, description })
    });
    return response.json();
  },

  async getState(stateId) {
    const response = await fetch(`${API_BASE}/api/states/${stateId}`);
    return response.json();
  },

  async deleteState(stateId) {
    const response = await fetch(`${API_BASE}/api/states/${stateId}`, {
      method: 'DELETE'
    });
    return response.json();
  },

  // Bot position
  async updateBotPosition(x, y, angle) {
    const response = await fetch(`${API_BASE}/api/bot/position`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ x, y, angle })
    });
    return response.json();
  },

  // Map points
  async addMapPoint(x, y, sensor) {
    const response = await fetch(`${API_BASE}/api/map/point`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ x, y, sensor })
    });
    return response.json();
  }
};