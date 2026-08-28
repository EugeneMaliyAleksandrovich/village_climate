import flet as ft
from datetime import datetime

class DatePickerWidget:
    """Виджет для отображения даты отбора данных из базы данных"""

    def __init__(self, page: ft.Page, selected_date: datetime = datetime.today(), on_date_change=None):
        self.date_picker = None
        self.page = page
        self.date_display = None
        self.selected_date = selected_date
        self.page = page
        self.content_area = None
        self.on_date_change = on_date_change
        
    def create_date_picker(self) -> ft.Row:
        self.date_picker = ft.DatePicker(on_change=self.on_date_change)
        self.update_date_display()
        date_button = ft.ElevatedButton("Выбрать дату", icon=ft.Icons.CALENDAR_TODAY, on_click=lambda e: self.page.show_dialog(self.date_picker),)

        self.content_area = ft.Container()
        self.content_area.content = ft.Row(
                [
                    self.date_display,
                    ft.VerticalDivider(width=1),
                    date_button,
                ],
            )
        
        return self.content_area

    def update_date_display(self):
        if self.date_display:
            self.date_display.value = f"📅 {self.selected_date.strftime('%d.%m.%Y')}"
        else:
            self.date_display = ft.Text(value=f"📅 {self.selected_date.strftime('%d.%m.%Y')}", size=18,
                        weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_700,)