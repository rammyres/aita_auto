import flet as ft
from lib.screens.main_screen import MainScreen
from lib.screens.selection_screen import SelectionScreen
from lib.screens.postlist_screen import PostListScreen
from lib.screens.post_screen  import PostScreen
from lib.screens.generate_screen import GenerateScreen
from lib.screens.video_screen import VideoView

def main(page: ft.Page):
    page.title = "Aita Auto VideoMaker"
    page.theme_mode = ft.ThemeMode.LIGHT
    
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
        page.views.append(PostListScreen(
            sub_name=sub_name, 
            go_post_screen=show_post_screen, 
            go_home=go_home))
        page.update()

    def show_post_screen(post_title, post_text):
        page.views.clear()
        page.views.append(PostScreen(
            post_title=post_title, 
            post_text=post_text, 
            go_generate = show_generate_screen, 
            go_home=go_home))
        page.update()

    def show_generate_screen(title, text, gender):
        page.views.clear()
        page.views.append(GenerateScreen(page, 
                                         title=title, 
                                         text=text, 
                                         gender=gender, 
                                         go_video_screen=show_video_screen, 
                                         go_home=go_home
                                         )
                         )
        page.update()

    def show_video_screen(video_path):
        page.views.clear()
        page.views.append(VideoView(page, video_path=video_path, go_home=go_home))
        page.update()

    # Start the app with the home view
    go_home()

ft.app(target=main)
