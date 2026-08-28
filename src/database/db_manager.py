import sqlite3
from datetime import datetime, timedelta
from contextlib import contextmanager
from typing import Any, Dict, Optional, List

from .models import ClimateData, DatabaseModels
from config import Config

class DatabaseManager:
    def __init__(self, db_path: str = Config.DB_PATH):
        self.db_path = db_path
        self._init_db()

    @contextmanager
    def get_connection(self):
        """Контекстный менеджер для соединения с БД"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def _init_db(self):
        """Инициализация базы данных"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(DatabaseModels.CREATE_TABLE)
            cursor.execute(DatabaseModels.CREATE_INDEXES)
            connection.commit()

    def insert_climate_data(self, data: ClimateData) -> int:
        """Вставка данных с метеостанции"""
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(
                "INSERT INTO climate_data (timestamp, temperature, humidity) VALUES (?, ?, ?)",
                    (data.timestamp, data.temperature, data.humidity))
            connection.commit()
            return cursor.lastrowid

    def get_climate_data(self, limit: int = 100, offset: int = 0,
        from_date: Optional[datetime] = None, to_date: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """Получение данных с фильтрацией"""
        query = "SELECT * FROM climate_data WHERE TRUE"
        params = []
        
        if from_date:
            query += " AND timestamp >= ?"
            params.append(from_date)
        
        if to_date:
            query += " AND timestamp <= ?"
            params.append(to_date)
        
        query += " ORDER BY timestamp LIMIT ? OFFSET ?"
        params.extend([limit, offset])
        
        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]

    def get_last_data(self, count: int = 24) -> List[Dict[str, Any]]:
        """Получить последние N записей (для графика)"""
        return self.get_climate_data(limit=count)
