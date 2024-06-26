import flet as ft
from lib.utils.reddit_utils import get_story_from_url
import re

class UrlScreen(ft.View):
    def __init__(self, page, go_post_screen, go_home):
        super().__init__(route='/url')
        self.page = page
        self.go_post_screen = go_post_screen

        self.appbar = ft.AppBar(
                    title=ft.Text("Insira a URL do post", color=ft.colors.WHITE), 
                    actions=[ft.IconButton(
                        icon=ft.icons.HOME_FILLED, 
                        icon_size=30,
                        icon_color=ft.colors.WHITE,
                        on_click=go_home,
                    )],
                    center_title=True, 
                    bgcolor=ft.colors.BLUE)
        self.url_field = ft.TextField(label="Insira a URL")

        self.error_message = ft.Text("", color=ft.colors.RED)

        self.url_button = ft.ElevatedButton("Enviar",
                                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                            on_click=self.submit_action)

        self.controls.append(self.appbar)
        self.controls.append(
            ft.Column(
                controls=[
                    self.url_field,
                    self.error_message,
                    self.url_button
                ]
            )
        )

    def submit_action(self, e):
        url = self.url_field.value
        if not self.is_valid_reddit_url(url):
            self.error_message.value = "URL inválida do Reddit. Por favor, insira uma URL válida."
            self.url_field.disabled = False
            self.update()
        else:
            self.error_message.value = ""
            self.controls.append(
                ft.Row(controls=[
                    ft.ProgressRing(),
                    ft.Text("Carregando...")
                ])
            )
            self.update()
            story = get_story_from_url(url)
            self.go_post_screen(f"{story['title']}|{story['text']}")
            self.url_field.disabled = True
            self.update()

    def is_valid_reddit_url(self, url):
        regex = r"https?://(www\.)?reddit\.com/r/\w+/comments/\w+/.+"
        return re.match(regex, url) is not None
