import flet as ft
from ui.app import ClimateApp
from utils.logger import setup_logging

def main():
    """Точка входа в приложение"""
    # Настройка логирования
    setup_logging()
    
    # Запуск Flet приложения
    app = ClimateApp()
    ft.app(target=app.main)

if __name__ == "__main__":
    main()
