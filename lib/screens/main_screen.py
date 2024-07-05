import flet as ft

class MainScreen(ft.View):
    def __init__(self, show_selection, show_video_list, show_url_screen, show_config_screen, show_post):
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
                    ft.Container(
                        height=200,
                        padding=10,
                        content=ft.Row(
                            controls=[
                            ft.ElevatedButton(text="Escolher subreddit", 
                                            tooltip="Inicie a geração escolhendo um subreddit e uma história",
                                            bgcolor=ft.colors.BLUE,
                                            color=ft.colors.WHITE,
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=show_selection),
                            ft.ElevatedButton(text="Iniciar a partir de texto",
                                            bgcolor=ft.colors.BLUE,
                                            color=ft.colors.WHITE,
                                            tooltip="Digite/cole o título e o texto da história na próxima tela",
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=lambda e: show_post("{}|{}".format("",""))),
                            ft.ElevatedButton(text="Usar URL de post",
                                            tooltip="Insira a URL de uma postagem para iniciar a geração", 
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
                    ),
                
            ]
        )
