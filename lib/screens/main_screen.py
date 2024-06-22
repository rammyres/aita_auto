from typing import Any, List
import flet as ft


class MainScreen(ft.View):
    # def __init__(self, show_selection, show_videos):
    def __init__(self, show_selection):
        super().__init__(
            route='/',
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.AppBar(title=ft.Text("Aita Auto VideoMaker")),
                ft.Column(controls=[
                    ft.ElevatedButton(text="Escolher subreddit", 
                                      bgcolor=ft.colors.BLUE,
                                      color=ft.colors.WHITE,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                      on_click=show_selection),
                    # ft.ElevatedButton(text="Mostrar lista de videos disponíveis", on_click=show_videos),
                ])
            ]
        )