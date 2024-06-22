import flet as ft
from lib.reddit_utils import *
from lib.interface_utils import suggest_gender

class PostScreen(ft.View):
    def __init__(self, post_title, post_text, go_generate, go_home):
        super().__init__(route="/post_screen")
        self.gender = None
        self.go_home = go_home
        self.go_generate = go_generate
        self.post_title = post_title
        self.post_text = post_text
        self.text_list = []
        self.text = ""
        
        def finished_text_action(e=None):
            self.text_list.extend([self.title_input.value, self.text_input.value])
            self.text = ' '.join(self.text_list)
            self.text = prepare_text(self.text)
            self.go_generate(self.text, self.gender)
            
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
            disabled=True,
            on_click=finished_text_action
        )
        
        self.male_checkbox = ft.Checkbox(label="Masculino", on_change=self.on_checkbox_change)
        self.female_checkbox = ft.Checkbox(label="Feminino", on_change=self.on_checkbox_change)
        self.suggested_text = ft.Text(value="", visible=False)
        
        self.gender_selection_row = ft.Row(
            controls=[self.suggested_text, self.male_checkbox, self.female_checkbox],
            alignment=ft.MainAxisAlignment.START
        )

        self.button_row = ft.Row(
            controls=[self.gender_selection_row, self.process_button, self.home_button],
            alignment=ft.MainAxisAlignment.END
        )

        self.controls = [
            ft.AppBar(
                title=ft.Text("Edite o texto se necessário e processe a gravação do video"),
                center_title=True,
                bgcolor=ft.colors.BLUE
            ),
            self.title_input,
            self.scrollable_text,
            self.button_row
        ]

    def did_mount(self):
        self.update_gender_text()

    def update_gender_text(self):
        self.suggested_gender = suggest_gender(" ".join([self.post_title, self.post_text]))
        if self.suggested_gender:
            self.suggested_text.value = f"Sugestão de gênero: {self.suggested_gender}"
            self.suggested_text.visible = True
        else:
            self.suggested_text.visible = False
        self.update()
    
    def on_checkbox_change(self, e):
        if e.control == self.male_checkbox and self.male_checkbox.value:
            self.female_checkbox.value = False
            self.gender = "male"
            self.process_button.disabled=False
        elif e.control == self.female_checkbox and self.female_checkbox.value:
            self.male_checkbox.value = False
            self.gender = "female"
            self.process_button.disabled=False
        self.update()