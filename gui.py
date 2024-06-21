import flet as ft
from lib.screens.main_screen import MainScreen
from lib.screens.selection_screen import SelectionScreen
from lib.screens.post_screen import PostScreen
def main(page: ft.Page):
    page.title = "Aita Auto VideoMaker"
    page.theme_mode = ft.ThemeMode.DARK
    
    def go_home(e=None):
        page.views.clear()
        page.views.append(MainScreen(show_selection=show_selection))
        page.update()

    def show_selection(e=None):
        page.views.clear()
        page.views.append(SelectionScreen(go_home=go_home, go_select_post=show_select_post))
        page.update()

    def show_select_post(sub_name):
        page.views.clear()
        page.views.append(PostScreen(sub_name=sub_name, go_home=go_home))
        page.update()


    # Start the app with the home view
    go_home()

ft.app(target=main)
