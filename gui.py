import flet as ft
from lib.screens.main_screen import MainScreen
from lib.screens.selection_screen import SelectionScreen

def main(page: ft.Page):
    page.title = "Aita Auto VideoMaker"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    def go_home(e=None):
        page.views.clear()
        page.views.append(MainScreen(show_selection=show_selection))
        page.update()

    def show_selection(e=None):
        page.views.clear()
        page.views.append(SelectionScreen(go_home=go_home))
        page.update()


    # Start the app with the home view
    go_home()

ft.app(target=main)
