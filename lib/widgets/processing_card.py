import flet as ft


class ProcessingCard(ft.UserControl):
    def __init__(self, text):
        super().__init__()
        self.text = text
        self.check_icon = ft.Icon(name=ft.icons.CHECK, color=ft.colors.GREY)
        self.label = ft.Text(value=self.text)

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    controls=[
                        self.check_icon,
                        self.label
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=10,
                border_radius=15,
                bgcolor=ft.colors.WHITE
            ),
            margin=10
        )

    def update_check(self, is_complete):
        self.check_icon.color = ft.colors.GREEN if is_complete else ft.colors.GREY
        self.update()