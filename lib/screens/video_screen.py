import flet as ft
import os

class VideoView(ft.View):
    def __init__(self, page, video_path, go_home):
        super().__init__(route="/video_view")
        self.page = page
        self.video_path = video_path
        self.go_home = go_home

        self.playlist = [ft.VideoMedia(video_path)]
        self.video_player = ft.Video(
                    playlist=self.playlist,
                    autoplay=True,
                    show_controls=True,
                    playlist_mode=ft.PlaylistMode.LOOP,
                    aspect_ratio=9/16,
                    volume=100,
                    filter_quality=ft.FilterQuality.HIGH,
                    width=300,  # Defina a largura desejada
                    height=533
                )

        self.controls = [
            ft.AppBar(
                title=ft.Text(
                    "Visualizador de Vídeo", 
                    font_family="roboto",
                    weight=ft.FontWeight.BOLD, 
                    color=ft.colors.WHITE
                ), 
                actions=[ft.IconButton(
                    icon=ft.icons.HOME_FILLED,
                    icon_color=ft.colors.WHITE, 
                    icon_size=30, 
                    on_click=self.close_player)],
                center_title=True, 
                bgcolor=ft.colors.BLUE
            ),
            ft.Container(
                content=ft.Row(controls=[self.video_player],
                alignment=ft.MainAxisAlignment.CENTER),
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
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]

    def close_player(self, e):
        self.video_player.stop()
        self.go_home()
        

    def copy_to_clipboard(self, e):
        self.page.set_clipboard(f"{os.getcwd()}/{self.video_path}")
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Caminho copiado"),
            duration=5000, 
            show_close_icon=True
        )
        self.page.snack_bar.open = True
        self.page.update()
