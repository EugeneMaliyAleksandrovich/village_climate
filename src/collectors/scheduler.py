import threading
import time
from datetime import datetime
from typing import Callable, Optional

from collectors.climate_collector import ClimateStationCollector
from config import Config
from utils.logger import logger

class Scheduler:
    """Планировщик задач для сбора данных"""
    
    def __init__(self, interval_seconds: int = Config.COLLECT_INTERVAL):
        self.interval = interval_seconds
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.collector = ClimateStationCollector(Config.STATION_URL)

    def start(self):
        """Запуск планировщика"""
        if self.running:
            logger.warning("Планировщик уже запущен")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run)#, daemon=True)
        self.thread.start()
        logger.info(f"Планировщик запущен. Интервал: {self.interval} сек")

    def stop(self):
        """Остановка планировщика"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Планировщик остановлен")
    
    def _run(self):
        """Основной цикл планировщика"""
        while self.running:
            try:
                logger.info("Начинается сбор данных...")
                data = self.collector.collect()
                
                if data:
                    logger.info(f"Данные успешно собраны: {data.temperature}°C")
                else:
                    logger.warning("Не удалось собрать данные")
                
            except Exception as e:
                logger.error(f"Ошибка в планировщике: {e}")
            
            # Ждем до следующего сбора
            for _ in range(self.interval):
                if not self.running:
                    break
                time.sleep(1)
    
    def collect_now(self) -> Optional[dict]:
        """Ручной сбор данных"""
        logger.info("Ручной сбор данных...")
        data = self.collector.collect()
        return data.to_dict() if data else None