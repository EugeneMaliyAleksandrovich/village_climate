import flet as ft
from typing import List, Dict, Any
from datetime import datetime

class TableWidget:
    """Виджет для отображения таблицы с данными"""

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.table = None

    def create_table(self) -> ft.DataTable:
        """Создает таблицу с данными"""
        columns = [
            ft.DataColumn(ft.Text("Время")),
            ft.DataColumn(ft.Text("Температура")),
            ft.DataColumn(ft.Text("Влажность"))
        ]
        
        rows = []
        for record in self.data[:50]:  # Показываем последние 50 записей
            timestamp = datetime.fromisoformat(record['timestamp']) if record.get('timestamp') else None
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(timestamp.strftime("%H:%M:%S") if timestamp else "")),
                        ft.DataCell(ft.Text(f"{record.get('temperature', 0):.1f}°C")),
                        ft.DataCell(ft.Text(f"{record.get('humidity', 0):.0f}%")),
                    ]
                )
            )
        
        self.table = ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            heading_row_color=ft.Colors.BLUE_GREY_50,
            heading_text_style=ft.TextStyle(weight=ft.FontWeight.BOLD),
            divider_thickness=0,
        )
        
        return self.table

    def update_data(self, new_data: List[Dict[str, Any]]):
        """Обновление данных таблицы"""
        self.data = new_data
        if self.table:
            new_table = self.create_table()
            self.table.rows = new_table.rows
            self.table.update()
