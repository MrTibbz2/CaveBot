# Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

import json
import os
from datetime import datetime
from typing import List, Optional
from models import BotPosition, MapPoint, SensorReading, MapState
import uuid

class CaveMapDatabase:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.current_state_file = os.path.join(data_dir, "current_state.json")
        self.states_dir = os.path.join(data_dir, "states")
        
        # Create directories if they don't exist
        os.makedirs(data_dir, exist_ok=True)
        os.makedirs(self.states_dir, exist_ok=True)
        
        # Initialize current state
        self.current_bot_position = BotPosition(x=0, y=0, angle=0, timestamp=datetime.now())
        self.current_map_points = []
        self.current_sensor_readings = []
    
    def update_bot_position(self, x: float, y: float, angle: float):
        self.current_bot_position = BotPosition(x=x, y=y, angle=angle, timestamp=datetime.now())
        self._save_current_state()
    
    def add_map_point(self, x: float, y: float, sensor: str):
        point = MapPoint(x=x, y=y, sensor=sensor, timestamp=datetime.now())
        self.current_map_points.append(point)
        self._save_current_state()
    
    def add_sensor_reading(self, sensor_name: str, distance: float):
        reading = SensorReading(sensor_name=sensor_name, distance=distance, timestamp=datetime.now())
        self.current_sensor_readings.append(reading)
        self._save_current_state()
    
    def get_current_state(self):
        return {
            "bot_position": self.current_bot_position.dict(),
            "map_points": [p.dict() for p in self.current_map_points],
            "sensor_readings": [r.dict() for r in self.current_sensor_readings]
        }
    
    def save_state(self, name: str, description: str = "") -> str:
        state_id = str(uuid.uuid4())
        state = MapState(
            id=state_id,
            name=name,
            bot_position=self.current_bot_position,
            map_points=self.current_map_points.copy(),
            sensor_readings=self.current_sensor_readings.copy(),
            created_at=datetime.now(),
            description=description
        )
        
        state_file = os.path.join(self.states_dir, f"{state_id}.json")
        with open(state_file, 'w') as f:
            json.dump(state.dict(), f, default=str, indent=2)
        
        return state_id
    
    def load_state(self, state_id: str):
        state_file = os.path.join(self.states_dir, f"{state_id}.json")
        if not os.path.exists(state_file):
            return None
        
        with open(state_file, 'r') as f:
            data = json.load(f)
        
        return MapState(**data)
    
    def list_states(self) -> List[dict]:
        states = []
        for filename in os.listdir(self.states_dir):
            if filename.endswith('.json'):
                state_id = filename[:-5]
                state = self.load_state(state_id)
                if state:
                    states.append({
                        "id": state.id,
                        "name": state.name,
                        "created_at": state.created_at,
                        "description": state.description
                    })
        return sorted(states, key=lambda x: x["created_at"], reverse=True)
    
    def delete_state(self, state_id: str) -> bool:
        state_file = os.path.join(self.states_dir, f"{state_id}.json")
        if os.path.exists(state_file):
            os.remove(state_file)
            return True
        return False
    
    def _save_current_state(self):
        with open(self.current_state_file, 'w') as f:
            json.dump(self.get_current_state(), f, default=str, indent=2)