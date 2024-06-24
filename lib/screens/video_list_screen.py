import json
import os
import flet as ft
from lib.utils.data_utils import delete_video

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
                bgcolor=ft.colors.BLUE,
                actions=[
                    ft.IconButton(icon=ft.icons.HOME_FILLED,
                                  icon_color=ft.colors.WHITE, 
                                  icon_size=30, 
                                  on_click=go_home)
                ]
            ),
            ft.Container(height=500, content=self.build_video_list()),
        ]

    def build_video_list(self):
        video_db = os.path.join('output', 'videos_db.json')
        video_list = ft.Column()
        if not os.path.exists(video_db):
            return ft.Text("Nenhum vídeo encontrado.")

        with open(os.path.join(video_db), 'r') as f:
            try:
                videos = json.load(f)
            except json.JSONDecodeError:
                return ft.Text("Erro ao carregar vídeos.")
            
            if not videos:
                return ft.Text("Nenhum vídeo encontrado.")

            for index, video in enumerate(videos):
                parts = []
                for v in video['videos']:
                    part_name = v['video'][-5:]
                    part_number = int(part_name[0])
                    parts.append(ft.TextButton(f"Parte {part_number}", on_click=lambda e, p=v['video']: self.go_video_screen(p)))
                title_card = ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            controls=[
                                ft.Text(video['title'], weight=ft.FontWeight.BOLD),
                                *parts,
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
