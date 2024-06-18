import flet as ft
import json

class SelectionScreen(ft.View):
    def get_subreddits(self) -> list:
        subreddits_json = None
        with open("config/subreddits.json") as f:
            subreddits_json = json.load(f)

        return subreddits_json['subreddits']

    def __init__(self, go_home):
        row = ft.ResponsiveRow(col=6)
        column = ft.Column()
        for i, k in enumerate(self.get_subreddits()):
            texto = "{} - {}".format(i+1, k['name'])
            column.controls.append(ft.ElevatedButton(text=texto))
        row.controls.append(column)

        super().__init__(
            route = "/selection_screen",
            controls=[
                ft.AppBar(title=ft.Text("Escolha um subreddit")),
                row,
                ft.ElevatedButton(text="Volar para home", on_click=go_home),
            ]
            )