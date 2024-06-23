import flet as ft
import os

class VideoView(ft.View):
    def __init__(self, page, video_path, go_home):
        super().__init__(route="/video_view")
        self.page = page
        self.video_path = video_path

        self.playlist = [ft.VideoMedia(video_path)]

        self.controls = [
            ft.AppBar(
                title=ft.Text(
                    "Visualizador de Vídeo", 
                    font_family="roboto",
                    weight=ft.FontWeight.BOLD, 
                    color=ft.colors.WHITE
                ), 
                center_title=True, 
                bgcolor=ft.colors.BLUE
            ),
            ft.Container(
                content=ft.Video(
                    playlist=self.playlist,
                    autoplay=True,
                    show_controls=True,
                    playlist_mode=ft.PlaylistMode.LOOP,
                    aspect_ratio=9/16,
                    volume=100,
                    filter_quality=ft.FilterQuality.HIGH,
                    width=300,  # Defina a largura desejada
                    height=533
                ),
                width=300, 
                height=533,
                alignment=ft.alignment.center
            ),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        text="Copiar caminho", 
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=self.copy_to_clipboard
                    ),
                    ft.ElevatedButton(
                        text="Voltar para home", 
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=go_home
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]

    def copy_to_clipboard(self, e):
        self.page.set_clipboard(f"{os.getcwd()}/{self.video_path}")
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Caminho copiado"),
            duration=5000, 
            show_close_icon=True
        )
        self.page.snack_bar.open = True
        self.page.update()
