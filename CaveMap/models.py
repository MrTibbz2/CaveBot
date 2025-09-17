# Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

from pydantic import BaseModel
from typing import Dict, List, Optional
from datetime import datetime

class BotPosition(BaseModel):
    x: float
    y: float
    angle: float
    timestamp: datetime

class MapPoint(BaseModel):
    x: float
    y: float
    sensor: str
    timestamp: datetime

class SensorReading(BaseModel):
    sensor_name: str
    distance: float
    timestamp: datetime

class MapState(BaseModel):
    id: str
    name: str
    bot_position: BotPosition
    map_points: List[MapPoint]
    sensor_readings: List[SensorReading]
    created_at: datetime
    description: Optional[str] = ""