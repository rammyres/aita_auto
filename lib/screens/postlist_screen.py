import flet as ft
from lib.reddit_utils import *

class PostListScreen(ft.View):
    def __init__(self, sub_name, go_home, go_post_screen):
        super().__init__(route="/postlist_screen")
        self.sub_name = sub_name
        self.go_home = go_home
        self.go_post_screen = go_post_screen

        self.posts_list = ft.ListView(expand=True)

        self.top_posts_button = self.create_button("10 postagens mais populares", self.load_top_posts)
        self.top_random_posts_button = self.create_button("10 posts aleatórios entre os 500 mais populares", self.load_random_top_posts)
        self.recent_posts_button = self.create_button("10 postagens mais populares da última semana", self.load_recent_posts)
        self.random_recent_posts_button = self.create_button("10 postagens entre as 100 mais populares da última semana", self.load_random_recent_posts)

        self.button_row = ft.Container(
            content=ft.GridView(
                controls=[
                    self.top_posts_button,
                    self.top_random_posts_button,
                    self.recent_posts_button,
                    self.random_recent_posts_button,
                ],
                padding=10,
                max_extent=160
            ),
            height=180  # Adjust the height as needed to occupy the first quarter of the page
        )

        self.controls = [
            ft.AppBar(
                title=ft.Text(
                    sub_name, 
                    font_family="Roboto", 
                    weight=ft.FontWeight.BOLD, 
                    color=ft.colors.WHITE
                    ), 
                actions=[ft.IconButton(
                        icon=ft.icons.HOME_FILLED, 
                        icon_size=30,
                        icon_color=ft.colors.WHITE,
                        on_click=go_home,
                    )],
                center_title=True, 
                bgcolor=ft.colors.BLUE
                ),
            self.button_row,
            self.posts_list,
        ]

    def create_button(self, text, on_click):
        return ft.ElevatedButton(
            text=text,
            on_click=on_click,
            bgcolor=ft.colors.BLUE,
            color=ft.colors.WHITE,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        )

    def generate_button(self, post_name, post_url, post_text):
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.ElevatedButton(
                            text=post_name,
                            bgcolor=ft.colors.BLUE,
                            color=ft.colors.WHITE,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                            on_click=lambda e: self.go_post_screen(post_name, post_text)
                        ),
                        ft.TextButton(text="Link do post", on_click=lambda e: self.page.launch_url(post_url))
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
            margin=10
        )

    def get_posts_buttons(self, sub_name=None, mode='top_10'):
        posts = []
        if mode == 'top_10':
            posts = get_stories(sub_name=sub_name)
        elif mode == 'random_top':
            posts = get_stories(sub_name=sub_name, sample_size=500)
        elif mode == 'recent_stories':
            posts = get_stories(sub_name=sub_name, time_limit='week')
        elif mode == 'top_recent_stories':
            posts = get_stories(sub_name=sub_name, sample_size=100, time_limit='week')

        rows = [ft.Row(controls=[self.generate_button(post['title'], post['url'], post['text'])]) for post in posts]
        return rows

    def load_top_posts(self, e):
        self.update_posts('top_10')

    def load_random_top_posts(self, e):
        self.update_posts('random_top')

    def load_recent_posts(self, e):
        self.update_posts('recent_stories')

    def load_random_recent_posts(self, e):
        self.update_posts('top_recent_stories')

    def update_posts(self, mode):
        self.posts_list.controls.clear()
        self.posts_list.controls.append(
            ft.Row(
                controls=[
                    ft.ProgressRing(),
                    ft.Text("Recuperando postagens", color=ft.colors.GREY)
                ]

            )
        )
        self.posts_list.update()
        rows = self.get_posts_buttons(self.sub_name, mode)
        self.posts_list.controls.clear()
        self.posts_list.controls.extend(rows)
        self.posts_list.update()
