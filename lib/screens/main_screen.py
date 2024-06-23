from lib.screens.video_list_screen import VideoListView
import flet as ft


class MainScreen(ft.View):
    # def __init__(self, show_selection, show_videos):
    def __init__(self, show_selection, show_video_list):
        super().__init__(
            route='/',
            vertical_alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.AppBar(title=ft.Text(
                    "Aita Auto VideoMaker", 
                    font_family="roboto",
                    weight=ft.FontWeight.BOLD, 
                    color=ft.colors.WHITE), 
                    center_title=True, 
                    bgcolor=ft.colors.BLUE),
                ft.Column(controls=[
                    ft.ElevatedButton(text="Lista de videos disponíveis", 
                                      bgcolor=ft.colors.BLUE,
                                      color=ft.colors.WHITE,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                      on_click=show_video_list),
                    
                    ft.ElevatedButton(text="Escolher subreddit", 
                                      bgcolor=ft.colors.BLUE,
                                      color=ft.colors.WHITE,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                      on_click=show_selection),
                ],
                alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )