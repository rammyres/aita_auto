import flet as ft
import os
from lib.screens.main_screen import MainScreen
from lib.screens.selection_screen import SelectionScreen
from lib.screens.postlist_screen import PostListScreen
from lib.screens.post_screen import PostScreen
from lib.screens.generate_screen import GenerateScreen
from lib.screens.video_screen import VideoView
from lib.screens.video_list_screen import VideoListView
from lib.screens.url_post_screen import UrlScreen
from lib.screens.config_screen import ConfigScreen
from lib.utils.reddit_utils import check_configs

def main(page: ft.Page):
    page.title = "Aita Auto VideoMaker"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.navigation_bar = ft.NavigationBar()

    def go_home(e=None):
        page.go('/')

    def show_selection(e=None):
        page.go('/selection')

    def show_select_post(e=None):
        page.go(f'/postlist/{e}')

    def show_post_screen(e=None):
        print(e)
        title, text = e.split('|', 1)
        page.go(f'/post/{title}/{text}')

    def show_generate_screen(e=None):
        title, text, gender = e.split('|', 2)
        page.go(f'/generate/{title}/{text}/{gender}')

    def show_video_screen(e=None):
        page.go(f'/video/{e}')

    def show_video_list(e=None):
        page.go('/video_list')

    def show_url_screen(e=None):
        page.go('/url')

    def show_config_screen(e=None):
        page.go('/config')

    # Handling route changes
    def route_change(route):
        if page.route == '/':
            page.views.clear()
            page.views.append(MainScreen(
                show_selection=show_selection, 
                show_video_list=show_video_list,
                show_url_screen=show_url_screen,
                show_config_screen=show_config_screen
            ))
        elif page.route == '/selection':
            page.views.append(SelectionScreen(
                page, 
                go_home=go_home, 
                go_select_post=show_select_post
            ))
        elif page.route.startswith('/postlist/'):
            sub_name = page.route.split('/')[2]
            page.views.append(PostListScreen(
                sub_name=sub_name, 
                go_post_screen=show_post_screen, 
                go_home=go_home
            ))
        elif page.route.startswith('/post/'):
            parts = page.route.split('/')[2:]
            print(parts[2:])
            post_title, post_text = parts[0], " ".join(parts[1:])
            page.views.append(PostScreen(
                post_title=post_title, 
                post_text=post_text, 
                go_generate=show_generate_screen, 
                go_home=go_home
            ))
        elif page.route.startswith('/generate/'):
            parts = page.route.split('/')[2:]
            title, text, gender = parts[0], parts[1], parts[2]
            page.views.append(GenerateScreen(
                page, 
                title=title, 
                text=text, 
                gender=gender, 
                go_video_screen=show_video_screen, 
                go_home=go_home
            ))
        elif page.route.startswith('/video/'):
            video_path = os.path.join(*page.route.split('/')[2:])
            
            page.views.append(VideoView(
                page, 
                video_path=video_path, 
                go_home=go_home
            ))
        elif page.route == '/video_list':
            page.views.append(VideoListView(
                page, 
                go_home=go_home, 
                go_video_screen=show_video_screen
            ))
        elif page.route == '/url':
            page.views.append(UrlScreen(
                page, 
                go_post_screen=show_post_screen,
                go_home=go_home
            ))
        elif page.route == '/config':
            page.views.append(ConfigScreen(
                page, 
                go_home=go_home
            ))

        page.update()

    # Handling view pop
    def view_pop(view):
        page.views.pop()
        page.update()

    # Start the app with the home view
    if not check_configs('gui'):
        page.go('/config')
    else:
        go_home()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

ft.app(target=main)
