import flet as ft

class MainScreen(ft.View):
    # def __init__(self, show_selection, show_videos):
    def __init__(self, show_selection, show_video_list, show_url_screen, show_config_screen):
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
                    bgcolor=ft.colors.BLUE,
                    actions=[ft.IconButton(
                        icon=ft.icons.SETTINGS,
                        icon_color=ft.colors.WHITE,
                        icon_size=30,
                        on_click=show_config_screen
                    )]),
                ft.Column(controls=[
                    ft.ElevatedButton(text="Escolher subreddit", 
                                      bgcolor=ft.colors.BLUE,
                                      color=ft.colors.WHITE,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                      on_click=show_selection),
                    ft.ElevatedButton(text="Usar URL de post", 
                                      bgcolor=ft.colors.BLUE,
                                      color=ft.colors.WHITE,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                      on_click=show_url_screen),
                    ft.ElevatedButton(text="Lista de videos disponíveis", 
                                      bgcolor=ft.colors.BLUE,
                                      color=ft.colors.WHITE,
                                      style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                      on_click=show_video_list),
                    
                ],
                alignment=ft.MainAxisAlignment.CENTER
                )
            ]
        )