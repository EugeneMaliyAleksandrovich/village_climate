from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class ClimateData:
    """Модель данных с метеостанции"""
    id: Optional[int] = None
    timestamp: Optional[datetime] = None
    temperature: float = 0.0
    humidity: float = 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'temperature': self.temperature,
            'humidity': self.humidity
        }

class DatabaseModels:
    """SQL-запрос для создания таблиц"""
    CREATE_TABLE = """
        CREATE TABLE IF NOT EXISTS climate_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME NOT NULL,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """

    CREATE_INDEXES = """
        CREATE INDEX IF NOT EXISTS idx_timestamp ON climate_data(timestamp);
    """
