import logging
from pathlib import Path
from datetime import datetime

LOG_DIR = Path("logs/client_logs/")
LOG_DIR.mkdir(exist_ok=True)

def setup_logging():
    """Настройка логирования"""
    log_file = LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()  # Вывод в консоль
        ]
    )

logger = logging.getLogger(__name__)