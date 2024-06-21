import flet as ft
from lib.reddit_utils import *

class PostScreen(ft.View):
    def generate_button(self, post_name, post_url, post_text):
        return ft.Card(content=ft.Row(
                            controls=[
                                ft.ElevatedButton(text=post_name),
                                ft.TextButton(text="Link do post", on_click=lambda e: self.page.launch_url(post_url))
                            ]
                            )
                       )
                       

    def get_posts_buttons(self, sub_name=None, mode='top_10'):
        posts = []
        if mode == 'top_10':
            posts.extend([p for p in get_stories(sub_name=sub_name)])
        if mode == 'random_top':
            posts.extend([p for p in get_stories(sub_name=sub_name, sample_size=500)])
        if mode == 'recent_stories':
            posts.extend([p for p in get_stories(sub_name=sub_name, time_limit='week')])
        if mode == 'top_recent_stories':
            posts.extend([p for p in get_stories(sub_name=sub_name, sample_size=100, time_limit='week')])
        rows = []
        for post in posts:
            rows.append(ft.Row(controls=[
                self.generate_button(post['title'], post['url'], post['text']),
                ]
                )
            )
        
        return rows
    
    

    def __init__(self, 
                 sub_name,
                 go_home, 
                 ):
        
        self.sub_name = sub_name
        self.column = ft.Column()
    
        def top_posts(e):
            rows = self.get_posts_buttons(self.sub_name, mode='top_10')
            self.column.controls.clear()
            self.column.update()
            self.column.controls.extend(rows)
            self.column.update()
        
        def top_random_posts(e):
            rows = self.get_posts_buttons(sub_name=self.sub_name, mode='random_top')
            self.column.controls.clear()
            self.column.update()
            self.column.controls.extend(rows)
            self.column.update()
        
        def recent_posts(e):
            rows = self.get_posts_buttons(sub_name=self.sub_name, mode='recent_stories')
            self.column.controls.clear()
            self.column.update()
            self.column.controls.extend(rows)
            self.column.update()

        def random_recent_posts(e):
            rows = self.get_posts_buttons(sub_name=self.sub_name, mode='top_recent_stories')
            self.column.controls.clear()
            self.column.update()
            self.column.controls.extend(rows)
            self.column.update()
        
        self.top_posts_button = ft.Card(ft.TextButton(text="10 postagens mais populares", on_click=top_posts))
        self.top_random_posts_button = ft.ElevatedButton(text="10 post aleatórios entre os 500 mais populares", on_click=top_random_posts)
        self.recent_posts_button = ft.ElevatedButton(text="10 postagens mais populares da ultima semana", on_click=recent_posts)
        self.random_recent_posts_button = ft.ElevatedButton(text="10 postagens entre as 100 mais populares da ultima semana", on_click=random_recent_posts)


        self.button_row = ft.GridView(
            expand=1,
            runs_count=5,
            max_extent=150,
            # child_aspect_ratio=1.0,
            spacing=5,
            run_spacing=5,
            controls=[
                self.top_posts_button,
                self.top_random_posts_button,
                self.recent_posts_button,
                self.random_recent_posts_button,
                ft.ElevatedButton(text="Voltar para home", on_click=go_home),
            ]
        )

        super().__init__(route="/post_screen", 
                         controls=[
                             ft.Text(sub_name, font_family="roboto", size=50, weight=ft.FontWeight.BOLD),
                             self.button_row,
                             self.column
                             ]
                         )
        

        
        
        