import flet as ft
from typing import List, Dict, Any
from database.db_manager import DatabaseManager
from ui.widgets.chart_widget import ChartWidget
from ui.widgets.table_widget import TableWidget
from collectors.scheduler import Scheduler
from config import Config
from utils.logger import logger
from ui.widgets.date_picker_widget import DatePickerWidget
from datetime import datetime, time

class ClimateApp:
    """Основное приложение Flet"""
    def __init__(self):
        self.db = DatabaseManager()
        self.scheduler = Scheduler()
        self.chart_widget = None
        self.table_widget = None
        self.current_page = "chart"  # chart или table
        self.date_picker_widget = None

    def main(self, page: ft.Page):
        """Основная функция Flet"""
        page.title = Config.APP_TITLE
        page.theme_mode = ft.ThemeMode.LIGHT
        page.window_width = Config.APP_WIDTH
        page.window_height = Config.APP_HEIGHT

        self.page = page

        self.date_picker_widget = DatePickerWidget(page=page, on_date_change=self._on_date_change)

        # Запустить планировщик
        self.scheduler.start()
        
        # Создать навигацию
        navigation = self._create_navigation()

        # Контентная область
        self.content_area = ft.Container(
            expand=True,
            padding=20,
        )

        # Собираем макет
        page.add(
            ft.Row(
                [
                    navigation,
                    ft.VerticalDivider(width=1),
                    self.content_area,
                ],
                expand=True,
            )
        )

        # Обновление каждые 10 секунд
        page.on_event = self._on_event

        # Закрытие приложения
        page.on_close = self._on_close
        
        # Загружаем начальные данные
        self.load_data()


    def _create_navigation(self) -> ft.NavigationRail:
        """Создает панель навигации"""
        navigationsInfo = [
            {'label': 'График', 'icon': ft.Icons.SHOW_CHART},
            {'label': 'Таблица', 'icon': ft.Icons.TABLE_CHART},
            {'label': 'Обновить', 'icon': ft.Icons.REFRESH},
            {'label': 'Настройки', 'icon': ft.Icons.SETTINGS},
        ]
        destinations = []
        for navInfo in navigationsInfo:
            destinations.append(
                ft.NavigationRailDestination(
                    icon=navInfo['icon'], selected_icon=navInfo['icon'], label=navInfo['label'])
            )

        return ft.NavigationRail(selected_index=0, label_type=ft.NavigationRailLabelType.ALL,
            min_width=100, min_extended_width=150, group_alignment=-0.9,
            destinations=destinations, on_change=self._on_navigation_change,
        )

    def load_data(self):
        """Загрузка данных из БД"""
        try:
            from_date = datetime.combine(self.date_picker_widget.selected_date.date(), time.min)
            to_date = datetime.combine(self.date_picker_widget.selected_date.date(), time.max)
            data = self.db.get_climate_data(from_date=from_date, to_date=to_date)
            
            if self.current_page == "chart":
                self._show_chart(data)
            else:
                self._show_table(data)
                
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
            self._show_error(str(e))

    def _show_chart(self, data: List[Dict[str, Any]]):
        """Отображает график"""
        self.chart_widget = ChartWidget(data)
        chart = self.chart_widget.create_chart()

        
        date_picker = self.date_picker_widget.create_date_picker()
        
        self.content_area.content = ft.Column(
            [   
                date_picker,
                ft.Container(
                    content=chart,
                    expand=True,
                    padding=10,
                ),
            ],
            expand=True,
        )
        self.content_area.update()

    def _show_table(self, data: List[Dict[str, Any]]):
        """Отображает таблицу"""
        self.table_widget = TableWidget(data)
        table = self.table_widget.create_table()

        date_picker = self.date_picker_widget.create_date_picker()
                
        self.content_area.content = ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Записи за выбранный период:", size=16, weight=ft.FontWeight.BOLD),
                            date_picker,
                            ft.Container(
                                content=table,
                                padding=10,
                                border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                                border_radius=10,
                            )
                        ],
                        scroll=ft.ScrollMode.AUTO,
                        expand=True,
                    ),
                    expand=True,
                ),
            ],
            expand=True,
        )
        self.content_area.update()

    def _manual_collect(self):
        """Ручной сбор данных"""
        data = self.scheduler.collect_now()
        if data:
            logger.info("Данные собраны вручную")
            # Обновляем страницу
            self.load_data()

    def _show_settings(self):
        """Показывает настройки"""
        # Можно добавить диалог с настройками
        pass

    def _show_error(self, message: str):
        """Показывает ошибку"""
        self.content_area.content = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=64, color=ft.Colors.RED),
                    ft.Text("Ошибка загрузки данных", size=24, weight=ft.FontWeight.BOLD),
                    ft.Text(message, size=14),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
        self.content_area.update()
    
    # Обработчики событий
    def _on_event(self, e):
        """Обработка событий страницы"""
        # Автообновление каждые 30 секунд
        if e.data == "update":
            self.load_data()
    
    def _on_close(self):
        """Закрытие приложения"""
        self.scheduler.stop()
        logger.info("Приложение закрыто")

    def _on_navigation_change(self, e):
        """Обработка изменения навигации"""
        index = e.control.selected_index
        
        if index == 0:
            self.current_page = "chart"
            self.load_data()
        elif index == 1:
            self.current_page = "table"
            self.load_data()
        elif index == 2:
            # Принудительное обновление
            self._manual_collect()
            self.load_data()
        elif index == 3:
            self._show_settings()
    
    def _on_date_change(self, e):
        utc_date = self.date_picker_widget.date_picker.value
        local_date = utc_date.astimezone()
        self.date_picker_widget.selected_date = local_date
        self.date_picker_widget.update_date_display()
        self.content_area.update()
        self.load_data()