import flet as ft
import json

class SelectionScreen(ft.View):
    def get_subreddits(self) -> list:
        with open("config/subreddits.json") as f:
            subreddits_json = json.load(f)
        return subreddits_json['subreddits']

    def create_button(self, subreddit_name, subreddit_description, go_select_post):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            subreddit_name,
                            size=20,
                            weight=ft.FontWeight.BOLD
                        ),
                        ft.Text(subreddit_description, size=14),
                        ft.ElevatedButton(
                            text="Selecionar",
                            on_click=lambda e: go_select_post(subreddit_name),
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=10,
                border_radius=15,
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    spread_radius=2,
                    color=ft.colors.GREY
                ),
                bgcolor=ft.colors.WHITE
            ),
            width=300,
            margin=10
        )

    def __init__(self, go_home, go_select_post):
        grid = ft.GridView(
            spacing=20,
            # scroll=ft.ScrollMode.ALWAYS,
            # alignment=ft.MainAxisAlignment.CENTER
            padding=10,
            max_extent=250,
        )
        subreddits = self.get_subreddits()
        for sr in subreddits:
            grid.controls.append(self.create_button(sr['name'], sr['description'], go_select_post))

        super().__init__(
            route="/selection_screen",
            controls=[
                ft.AppBar(title=ft.Text("Escolha um subreddit"), center_title=True, bgcolor=ft.colors.BLUE),
                ft.Container(
                    content=grid,
                    padding=20,
                    alignment=ft.alignment.center,
                    
                ),
                ft.ElevatedButton(
                    text="Voltar para Home",
                    on_click=go_home,
                    bgcolor=ft.colors.BLUE,
                    color=ft.colors.WHITE,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                ),
            ]
        )
        self.scroll = ft.ScrollMode.ALWAYS