import flet as ft
from lib.reddit_utils import get_story_from_url
import re

class UrlScreen(ft.View):
    def __init__(self, page, go_post_screen):
        print("Initializing UrlScreen")
        super().__init__(route='/url_screen')
        self.page = page
        self.go_post_screen = go_post_screen

        self.appbar = ft.AppBar(leading=ft.Text("Postagem a partir de URL de post"), color=ft.colors.WHITE)
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
            self.go_post_screen(story['title'], story['text'])
            self.url_field.disabled = True
            self.update()

    def is_valid_reddit_url(self, url):
        regex = r"https?://(www\.)?reddit\.com/r/\w+/comments/\w+/.+"
        return re.match(regex, url) is not None

# Exemplo de uso
def main(page: ft.Page):
    def go_post_screen(title, text):
        print(f"Título: {title}\nTexto: {text}")

    page.views.append(UrlScreen(page, go_post_screen))
    page.update()

ft.app(target=main)
