import flet as ft
from lib.reddit_utils import *

class PostScreen(ft.View):
    def __init__(self, post_title, post_text, go_home):
        super().__init__(route="/post_screen")
        self.go_home = go_home
        self.post_title = post_title
        self.post_text = post_text
        self.text_list = []
        self.text = ""
        
        def finished_text_action(e=None):
            self.text_list.extend([self.title_input.value, self.text_input.value])
            self.text = ' '.join(self.text_list)
            self.text = prepare_text(self.text)
            print(self.text)

        self.title_input = ft.TextField(
            value=self.post_title, 
            label="Titulo",
            )
        
        self.text_input = ft.TextField(
            value=self.post_text, 
            multiline=True, 
            expand=True
            )

        self.scrollable_text = ft.Container(
            content=self.text_input,
            expand=True
        )

        self.home_button = ft.ElevatedButton(
                            text="Home",
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=self.go_home
                            )
        
        self.process_button = ft.ElevatedButton(
                            text="Processar video",
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=finished_text_action
                            )
        self.button_row = ft.Row(controls=[self.process_button, self.home_button],
                                 alignment=ft.MainAxisAlignment.END
                                 )

        self.controls = [ft.AppBar(title=ft.Text("Edite o texto se necessário e processe a gravação do video"), 
                                 center_title=True, 
                                 bgcolor=ft.colors.BLUE),
                         self.title_input, 
                         self.scrollable_text,
                         self.button_row
                         ]

