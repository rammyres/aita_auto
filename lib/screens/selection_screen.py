import flet as ft
import json

class SelectionScreen(ft.View):
    def get_subreddits(self) -> list:
        subreddits_json = None
        with open("config/subreddits.json") as f:
            subreddits_json = json.load(f)

        return subreddits_json['subreddits']

    def create_button(self, subreddit_name, subreddit_description, go_select_post):
        return ft.Card(content=ft.Column(controls=
            [
                ft.ElevatedButton(
                    text="{}".format(subreddit_name),
                    on_click=lambda e: go_select_post(subreddit_name)
                ),
                ft.Text(subreddit_description)
            ],
            width=300,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            
        )

    def __init__(self, go_home, go_select_post):
        row = ft.ResponsiveRow(col=6)
        column = ft.Column(
            spacing=10,
            scroll=ft.ScrollMode.ALWAYS,
        )
        subreddits = self.get_subreddits()
        for sr in subreddits:
            column.controls.append(self.create_button(sr['name'], sr['description'], go_select_post))
        row.controls.append(column)

        super().__init__(
            route = "/selection_screen",
            controls=[
                ft.AppBar(title=ft.Text("Escolha um subreddit")),
                row,
                ft.ElevatedButton(text="Volar para home", on_click=go_home),
            ]
            )
        self.scroll = ft.ScrollMode.ALWAYS
        # self.page.update()