import flet as ft
from lib.widgets.subreddit_card import SubredditCard
import json

class SelectionScreen(ft.View):
    def get_subreddits(self) -> list:
        with open("config/subreddits.json") as f:
            subreddits_json = json.load(f)
        return subreddits_json['subreddits']
        
    def __init__(self, page, go_home, go_select_post):
        self.page = page
        grid = ft.GridView(
            spacing=20,
            # scroll=ft.ScrollMode.ALWAYS,
            # alignment=ft.MainAxisAlignment.CENTER
            padding=10,
            max_extent=250,
        )
        subreddits = self.get_subreddits()
        for sr in subreddits:
            grid.controls.append(SubredditCard(sr['name'], sr['description'], go_select_post))

        super().__init__(
            route="/selection",
            controls=[
                ft.AppBar(
                    title=ft.Text("Escolha um subreddit", color=ft.colors.WHITE), 
                    actions=[ft.IconButton(
                        icon=ft.icons.HOME_FILLED, 
                        icon_size=30,
                        icon_color=ft.colors.WHITE,
                        on_click=go_home,
                    )],
                    center_title=True, 
                    bgcolor=ft.colors.BLUE),
                ft.Container(
                    content=grid,
                    padding=20,
                    alignment=ft.alignment.center,
                    
                )
            ]
        )
        self.scroll = ft.ScrollMode.ALWAYS