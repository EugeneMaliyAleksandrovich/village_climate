from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from utils.collector_logger import setup_logging, logger
from climate_collector import ClimateStationCollector
from common.config import Config
import time

def main():
    """Точка входа в приложение"""
    # Настройка логирования
    setup_logging()
    
    interval = 3600
    collector = ClimateStationCollector(Config.STATION_URL)

    while True:
        try:
            logger.info("Начинается сбор данных...")
            data = collector.collect()
            
            if data:
                logger.info(f"Данные успешно собраны: {data.temperature}°C")
            else:
                logger.warning("Не удалось собрать данные")
            
        except Exception as e:
            logger.error(f"Ошибка в планировщике: {e}")
            pass
        
        # Ждем до следующего сбора
        logger.info(f"Жду {interval} секунд.")
        for _ in range(interval):
            time.sleep(1)

if __name__ == "__main__":
    main()
