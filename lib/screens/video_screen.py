import flet as ft

class VideoView(ft.View):
    def __init__(self, page, video_path, go_home):
        super().__init__(route="/video_view")
        self.page = page
        self.video_path = video_path

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
                    src=video_path,
                    autoplay=True,
                    controls=True,
                    loop=False,
                    width=800,  # Ajuste a largura conforme necessário
                    height=600,  # Ajuste a altura conforme necessário
                ),
                alignment=ft.alignment.center
            ),
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        text="Voltar para home", 
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=go_home
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        ]
