import flet as ft

class SubredditCard(ft.UserControl):
    def __init__(self, subreddit_name, subreddit_description, go_select_post):
        super().__init__()
        self.subreddit_name = subreddit_name
        self.subreddit_description = subreddit_description
        self.go_select_post = go_select_post
    
    def build(self):
        return ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        controls=[
                            ft.Text(
                                self.subreddit_name,
                                size=20,
                                weight=ft.FontWeight.BOLD
                            ),
                            ft.Text(self.subreddit_description, size=14),
                            ft.ElevatedButton(
                                text="Selecionar",
                                on_click=lambda e: self.go_select_post(self.subreddit_name),
                                bgcolor=ft.colors.BLUE,
                                color=ft.colors.WHITE,
                                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
                            )
                        ],
                        spacing=10,
                        # alignment=ft.MainAxisAlignment.START
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
