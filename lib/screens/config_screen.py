import configparser, os
import flet as ft

class ConfigScreen(ft.View):
    def __init__(self, page, go_home):
        super().__init__(route='/config_screen')
        self.aws_config_file = os.path.join(os.path.expanduser('~'),'.aws', 'credentials')
        self.aai_config_file = os.path.join(os.getcwd(), 'config', 'aai.ini')
        self.reddit_config_file = os.path.join(os.getcwd(), 'config', 'reddit_config.ini')
        self.page = page
        self.go_home = go_home
        
        self.reddit_config = configparser.ConfigParser()
        self.aai_config = configparser.ConfigParser()
        self.credentials_config = configparser.ConfigParser()

        self.read_configs()

        self.reddit_client_id = ft.TextField(label="Reddit Client ID", value=self.reddit_config.get('reddit', 'client_id', fallback=''))
        self.reddit_client_secret = ft.TextField(label="Reddit Client Secret", value=self.reddit_config.get('reddit', 'client_secret', fallback=''))
        self.reddit_user_agent = ft.TextField(label="Reddit User Agent", value=self.reddit_config.get('reddit', 'user_agent', fallback=''))

        self.aai_key = ft.TextField(label="AAI Key", value=self.aai_config.get('aai_settings', 'key', fallback=''))

        self.aws_access_key_id = ft.TextField(label="AWS Access Key ID", value=self.credentials_config.get('default', 'aws_access_key_id', fallback=''))
        self.aws_secret_access_key = ft.TextField(label="AWS Secret Access Key", value=self.credentials_config.get('default', 'aws_secret_access_key', fallback=''))

        self.save_button = ft.ElevatedButton(text="Salvar", on_click=self.save_configs)
        self.home_button = ft.ElevatedButton(text="Home", on_click=go_home)

        self.controls.append(
            ft.AppBar(
                title=ft.Text("Configurações", color=ft.colors.WHITE),
                actions=[self.home_button],
                center_title=True,
                bgcolor=ft.colors.BLUE,
            )
        )
        
        self.controls.append(
            ft.Column(
                controls=[
                    ft.Text("Configurações da API Reddit", size=20, weight=ft.FontWeight.BOLD),
                    self.reddit_client_id,
                    self.reddit_client_secret,
                    self.reddit_user_agent,
                    ft.Text("Configurações da API Assembly.ai", size=20, weight=ft.FontWeight.BOLD),
                    self.aai_key,
                    ft.Text("Configurações de credenciais AWS", size=20, weight=ft.FontWeight.BOLD),
                    self.aws_access_key_id,
                    self.aws_secret_access_key,
                    self.save_button,
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
            )
        )

    def read_configs(self):
        self.reddit_config.read(self.reddit_config_file)
        self.aai_config.read(self.aai_config_file)
        self.credentials_config.read(self.aws_config_file)

    def save_configs(self, e):
        self.reddit_config['reddit'] = {
            'client_id': self.reddit_client_id.value,
            'client_secret': self.reddit_client_secret.value,
            'user_agent': self.reddit_user_agent.value,
        }
        self.aai_config['aai_settings'] = {
            'key': self.aai_key.value,
        }
        self.credentials_config['default'] = {
            'aws_access_key_id': self.aws_access_key_id.value,
            'aws_secret_access_key': self.aws_secret_access_key.value,
        }
        
        with open(self.reddit_config_file, 'w') as configfile:
            self.reddit_config.write(configfile)
        with open(self.aai_config_file, 'w') as configfile:
            self.aai_config.write(configfile)
        with open(self.aws_config_file, 'w') as configfile:
            self.credentials_config.write(configfile)

        sb = ft.SnackBar(content=ft.Text("Configurações salvas com sucesso!"), 
                         duration=6000,
                         show_close_icon=True 
                         )
        self.page.snack_bar = sb
        self.page.snack_bar.open=True
        self.page.update()

    def did_mount(self):
        self.read_configs()