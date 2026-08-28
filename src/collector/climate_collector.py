import requests
from datetime import datetime
from typing import Optional
import json

from common.database.models import ClimateData
from common.database.db_manager import DatabaseManager
from utils.collector_logger import logger

class ClimateStationCollector():
    """Сборщик данных с метеостанции"""
    
    def __init__(self, station_url: str):
        self.station_url = station_url
        self.db = DatabaseManager()
    
    def collect(self) -> Optional[ClimateData]:
        """Собрать данные с метеостанции"""
        try:
            headers = {}
            
            response = requests.get(f"{self.station_url}",
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            # Преобразуем данные в модель
            climate_data = ClimateData(
                timestamp=datetime.now(),
                temperature=data.get('temperature', 0.0),
                humidity=data.get('humidity', 0.0)
            )
            
            # Сохраняем в базу
            record_id = self.db.insert_climate_data(climate_data)
            logger.info(f"Данные сохранены: ID={record_id}, Temp={climate_data.temperature}°C")
            
            return climate_data
            
        except requests.RequestException as e:
            logger.error(f"Ошибка при запросе к метеостанции: {e}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return None
        except Exception as e:
            logger.error(f"Неизвестная ошибка: {e}")
            return None
