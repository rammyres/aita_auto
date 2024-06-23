import flet as ft
from lib.reddit_utils import get_story_from_url

class UrlScreen(ft.View):
    def __init__(self, page, go_post_screen):
        super().__init__(route = '/url_screen')
        self.page = page
        self.post_screen = go_post_screen

        self.appbar = ft.AppBar(leading=ft.Text("Postagem a partir de URL de post"), color=ft.colors.WHITE)
        self.url_field = ft.TextField(label="Insira a URL")

        self.url_button = ft.ElevatedButton("Enviar", 
                                       style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                                       on_click=self.submit_action
                                        )
        
        self.controls.append(self.appbar)
        self.controls.append(
            ft.Column(
                controls=[
                self.url_field,
                self.url_button
            ]
            )
            
        )
            
    def submit_action(self, e):
            self.controls.append(
                 ft.Row(controls=[
                      ft.ProgressRing(),
                      ft.Text("Carregando...")
                 ])
            )
            self.update()
            story = get_story_from_url(self.url_field.value)
            self.post_screen(story['title'], story['text'])
            self.url_field.disabled = True
            
