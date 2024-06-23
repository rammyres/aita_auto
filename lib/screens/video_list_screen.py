import json
import os
import flet as ft
from lib.data_utils import delete_video

class VideoListView(ft.View):
    def __init__(self, page, go_video_screen, go_home):
        super().__init__(route="/video_list")
        self.page = page
        self.go_home = go_home
        self.go_video_screen = go_video_screen

        self.controls = [
            ft.AppBar(
                title=ft.Text(
                    "Lista de Vídeos",
                    font_family="roboto",
                    weight=ft.FontWeight.BOLD,
                    color=ft.colors.WHITE
                ),
                center_title=True,
                bgcolor=ft.colors.BLUE
            ),
            ft.Container(height=500, content=self.build_video_list()),
            ft.ElevatedButton(
                text="Voltar para home",
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                on_click=lambda e: self.go_home()
            )
        ]

    def build_video_list(self):
        video_list = ft.Column()
        if not os.path.exists('output/videos_db.json'):
            return ft.Text("Nenhum vídeo encontrado.")

        with open('output/videos_db.json', 'r') as f:
            try:
                videos = json.load(f)
            except json.JSONDecodeError:
                return ft.Text("Erro ao carregar vídeos.")
            
            if not videos:
                return ft.Text("Nenhum vídeo encontrado.")

            for index, video in enumerate(videos):
                title_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(video['title'], weight=ft.FontWeight.BOLD),
                                *[
                                    ft.TextButton(f"Parte {i+1}", on_click=lambda e, p=part['video']: self.go_video_screen(p))
                                    for i, part in enumerate(video['videos'])
                                ],
                                ft.ElevatedButton(
                                    text="Excluir",
                                    bgcolor=ft.colors.RED,
                                    color=ft.colors.WHITE,
                                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                    on_click=lambda e, idx=index: self.delete_video_and_refresh(idx)
                                )
                            ],
                            spacing=10
                        ),
                        padding=10,
                        border_radius=15,
                        bgcolor=ft.colors.WHITE
                    ),
                    margin=10
                )
                video_list.controls.append(title_card)
        return video_list

    def delete_video_and_refresh(self, index):
        delete_video(index)
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Vídeo deletado com sucesso!"),
            duration=5000, 
            show_close_icon=True
        )
        self.page.snack_bar.open = True
        self.page.update()
        # Recarregar a lista de vídeos
        self.controls[1].content = self.build_video_list()
        self.page.update()
