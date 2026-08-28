import flet as ft
import flet_charts as fch
from typing import List, Dict, Any
from datetime import datetime


class ChartWidget:
    """Виджет для отображения графика"""

    MAX_Y = 100
    MIN_Y = 0
    HORIZONTAL_GRID_LINES_INTERVAL = 5
    MAX_TEMP = 50
    MIN_TEMP = -50

    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.chart = None

    def create_chart(self) -> fch.LineChart:
        """Создает график на основе данных"""
        if not self.data:
            return self._create_empty_chart()

        # Подготовить данные для графика
        temperature_data = self._prepare_series('temperature', ft.Colors.RED)
        humidity_data = self._prepare_series('humidity', ft.Colors.BLUE)

        temperature_labels = self._get_chart_y_axis_labels('temperature')
        humidity_labels = self._get_chart_y_axis_labels('humidity')

        data_series = [temperature_data, humidity_data]
        
        chart = fch.LineChart(
            data_series=data_series,
            min_y=0,
            max_y=self.MAX_Y,
            min_x=self.MIN_Y,
            max_x=len(self.data),
            horizontal_grid_lines=fch.ChartGridLines(
                interval=self.HORIZONTAL_GRID_LINES_INTERVAL,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1
            ),
            vertical_grid_lines=fch.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1
            ),
            left_axis=self._create_axis("Температура, °C", temperature_labels),
            right_axis=self._create_axis("Влажность, %", humidity_labels),
            bottom_axis=self._create_bottom_axis(),
        )

        self.chart = chart
        return chart

    def _prepare_series(self, field: str, color: ft.Colors) -> fch.LineChartData:
        """Подготовка данных для одной серии"""
        points = []
        for i, record in enumerate(self.data):
            if record.get(field) is not None:
                x = i
                y = self._map_temp_value_to_chart_axis(float(record[field])) if field == 'temperature' else float(record[field])

                dt = datetime.fromisoformat(record['timestamp'])
                tooltip = f"{record[field]} °C, {dt.strftime("%H:%M")}" if field == 'temperature' else f"{record[field]} %, {dt.strftime("%H:%M")}"
                points.append(fch.LineChartDataPoint(x=x, y=y, tooltip=tooltip))
        
        return fch.LineChartData(
            points=points,
            color=color,
            stroke_width=2
        )

    def _create_axis(self, title: str, labels: list[fch.ChartAxisLabel]) -> fch.ChartAxis:
        """Создание оси"""
        return fch.ChartAxis(
            title=ft.Text(title),
            labels=labels,
            show_labels=True,
            label_size=40
        )

    def _create_bottom_axis(self) -> fch.ChartAxis:
        """Создание нижней оси с временными метками"""
        labels = []

        if self.data:
            for i, record in enumerate(self.data):
                if record.get('timestamp'):
                    dt = datetime.fromisoformat(record['timestamp'])
                    labels.append(fch.ChartAxisLabel(
                        value=i,
                        label=ft.Text(dt.strftime("%H:%M"), size=10)
                    ))
        
        return fch.ChartAxis(
            labels=labels,
            show_labels=True,
        )

    def _create_empty_chart(self) -> fch.LineChart:
        """Создает пустой график"""
        return fch.LineChart(
            data_series=[],
            min_y=0,
            max_y=10,
            min_x=0,
            max_x=10,
            horizontal_grid_lines=fch.ChartGridLines(
                interval=1,
                color=ft.Colors.with_opacity(0.2, ft.Colors.ON_SURFACE),
                width=1
            )
        )

    def update_data(self, new_data: List[Dict[str, Any]]):
        """Обновление данных графика"""
        self.data = new_data
        new_chart = self.create_chart()
        
        if self.chart:
            # Обновление существующего графика
            self.chart.data_series = new_chart.data_series
            self.chart.update()
        else:
            self.chart = new_chart

    def _map_temp_value_to_chart_axis(self, temp):
        # mapped_value = min_target + (original_value - min_original) * (max_target - min_target) / (max_original - min_original)
        offset = temp - self.MIN_TEMP # Смещение значения относительно минимума исходной шкалы
        scaling_factor = (self.MAX_Y - self.MIN_Y) / (self.MAX_TEMP - self.MIN_TEMP)
        result = self.MIN_Y + offset * scaling_factor
        return result

    def _get_chart_y_axis_labels(self, field: str) -> list[fch.ChartAxisLabel]:

        horizontal_lines_number = self.MAX_Y / self.HORIZONTAL_GRID_LINES_INTERVAL
        grids_number = horizontal_lines_number

        labels = []

        start_value = -50 if field == 'temperature' else 0

        for grid_number in range(1, int(grids_number) + 1):
            value_delta = int(grid_number * self.MAX_Y / grids_number)
            label = start_value + value_delta

            labels.append(fch.ChartAxisLabel(value=value_delta, label=ft.Text(label)))

        return labels

    