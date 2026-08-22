class Config:
    DB_PATH = "data/climate.db"
    DB_ECHO = False  # Логи SQL запросов

    # Расписание сбора данных (в секундах)
    COLLECT_INTERVAL = 3600  # 1 час

    # Настройки метеостанции
    STATION_URL = "http://192.168.1.98/data"
