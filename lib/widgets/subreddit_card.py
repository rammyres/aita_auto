
import flet as ft

class SubredditCard(ft.UserControl):
    def __init__(self, subreddit_name, subreddit_description, go_select_post):
        super().__init__()
        self.subreddit_name = subreddit_name
        self.subreddit_description = subreddit_description
        self.go_select_post = go_select_post
    
    def build(self):
        return ft.Container(
            content=ft.GestureDetector(
                on_tap=lambda e: self.go_select_post(self.subreddit_name),
                content=ft.Container(
                    content=ft.Column(
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        controls=[
                            ft.Text(
                                self.subreddit_name,
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE
                            ),
                            ft.Text(
                                self.subreddit_description,
                                size=14,
                                color=ft.colors.WHITE
                            ),
                        ],
                        spacing=10
                    ),
                    padding=15,
                    border_radius=ft.border_radius.all(15),
                    gradient=ft.LinearGradient(
                        begin=ft.alignment.top_left,
                        end=ft.alignment.bottom_right,
                        colors=[ft.colors.BLUE, ft.colors.LIGHT_BLUE_100]
                    ),
                    shadow=ft.BoxShadow(
                        blur_radius=10,
                        spread_radius=2,
                        color=ft.colors.GREY
                    )
                )
            ),
            width=300,
            margin=10,
            border_radius=ft.border_radius.all(15),
        )
