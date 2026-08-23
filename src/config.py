class Config:
    DB_PATH = "data/climate.db"
    DB_ECHO = False  # Логи SQL запросов

    # Расписание сбора данных (в секундах)
    COLLECT_INTERVAL = 3600  # 1 час

    # Настройки метеостанции
    STATION_URL = "http://192.168.1.98/data"

    # Flet настройки
    APP_TITLE = "Метеостанция"
    APP_WIDTH = 1200
    APP_HEIGHT = 800

    # График
    CHART_MIN_Y = 0
    CHART_MAX_Y = 40
    CHART_MIN_X = 0
    CHART_MAX_X = 24  # 24 часа