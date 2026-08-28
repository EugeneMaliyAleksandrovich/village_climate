from pathlib import Path
import sys
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import flet as ft
from client.ui.app import ClimateApp
from utils.client_logger import setup_logging

def main():
    """Точка входа в приложение"""
    # Настройка логирования
    setup_logging()
    
    # Запуск Flet приложения
    app = ClimateApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
