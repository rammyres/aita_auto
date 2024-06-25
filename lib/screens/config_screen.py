import configparser, os, json
import flet as ft

class ConfigScreen(ft.View):
    def __init__(self, page, go_home):
        super().__init__(route='/config_screen')
        self.aws_config_file = os.path.join(os.path.expanduser('~'), '.aws', 'credentials')
        self.aai_config_file = os.path.join(os.getcwd(), 'config', 'aai.ini')
        self.reddit_config_file = os.path.join(os.getcwd(), 'config', 'reddit_config.ini')
        self.acronyms_file = os.path.join(os.getcwd(), 'config', 'acronyms.json')
        self.common_combinations_file = os.path.join(os.getcwd(), 'config', 'common_combinations.json')
        self.contractions_file = os.path.join(os.getcwd(), 'config', 'contractions.json')
        self.profanities_file = os.path.join(os.getcwd(), 'config', 'profanities.json')
        self.subreddits_file = os.path.join(os.getcwd(), 'config', 'subreddits.json')
        self.videos_file = os.path.join(os.getcwd(), 'config', 'videos.json')
        self.voices_file = os.path.join(os.getcwd(), 'config', 'voices.json')
        
        self.page = page
        self.go_home = go_home
        
        self.reddit_config = configparser.ConfigParser()
        self.aai_config = configparser.ConfigParser()
        self.credentials_config = configparser.ConfigParser()
        self.acronyms = {}
        self.common_combinations = {}
        self.contractions = {}
        self.profanities = {}
        self.subreddits = []
        self.videos = []
        self.voices = {"females": [], "males": []}

        self.read_configs()

        self.reddit_client_id = ft.TextField(label="Reddit Client ID", value=self.reddit_config.get('reddit', 'client_id', fallback=''))
        self.reddit_client_secret = ft.TextField(label="Reddit Client Secret", value=self.reddit_config.get('reddit', 'client_secret', fallback=''))
        self.reddit_user_agent = ft.TextField(label="Reddit User Agent", value=self.reddit_config.get('reddit', 'user_agent', fallback=''))

        self.aai_key = ft.TextField(label="AAI Key", value=self.aai_config.get('aai_settings', 'key', fallback=''))

        self.aws_access_key_id = ft.TextField(label="AWS Access Key ID", value=self.credentials_config.get('default', 'aws_access_key_id', fallback=''))
        self.aws_secret_access_key = ft.TextField(label="AWS Secret Access Key", value=self.credentials_config.get('default', 'aws_secret_access_key', fallback=''))

        self.save_button = ft.ElevatedButton(text="Salvar", on_click=self.save_configs)
        self.home_button = ft.ElevatedButton(text="Home", on_click=go_home)

        self.acronym_key = ft.TextField(label="Acrônimo")
        self.acronym_value = ft.TextField(label="Descrição")
        self.add_acronym_button = ft.ElevatedButton(text="Adicionar", on_click=self.add_acronym)
        self.acronyms_list = ft.ListView(expand=True)

        self.common_combination_key = ft.TextField(label="Combinacão Comum")
        self.common_combination_value = ft.TextField(label="Descrição")
        self.add_common_combination_button = ft.ElevatedButton(text="Adicionar", on_click=self.add_common_combination)
        self.common_combinations_list = ft.ListView(expand=True)

        self.contraction_key = ft.TextField(label="Contração")
        self.contraction_value = ft.TextField(label="Descrição")
        self.add_contraction_button = ft.ElevatedButton(text="Adicionar", on_click=self.add_contraction)
        self.contractions_list = ft.ListView(expand=True)

        self.profanity_key = ft.TextField(label="Palavrão")
        self.profanity_value = ft.TextField(label="Descrição")
        self.add_profanity_button = ft.ElevatedButton(text="Adicionar", on_click=self.add_profanity)
        self.profanities_list = ft.ListView(expand=True)
        
        self.subreddit_name = ft.TextField(label="Nome do Subreddit")
        self.subreddit_description = ft.TextField(label="Descrição")
        self.add_subreddit_button = ft.ElevatedButton(text="Adicionar", on_click=self.add_subreddit)
        self.subreddits_list = ft.ListView(expand=True)

        self.video_url = ft.TextField(label="URL do Vídeo")
        self.add_video_button = ft.ElevatedButton(text="Adicionar", on_click=self.add_video)
        self.videos_list = ft.ListView(expand=True)

        self.voice_female_name = ft.TextField(label="Nome da Voz Feminina")
        self.add_voice_female_button = ft.ElevatedButton(text="Adicionar", on_click=lambda e: self.add_voice(e, 'females'))
        self.voice_male_name = ft.TextField(label="Nome da Voz Masculina")
        self.add_voice_male_button = ft.ElevatedButton(text="Adicionar", on_click=lambda e: self.add_voice(e, 'males'))
        self.voices_list = ft.ListView(expand=True)

        self.controls.append(
            ft.AppBar(
                title=ft.Text("Configurações", color=ft.colors.WHITE),
                actions=[self.home_button],
                center_title=True,
                bgcolor=ft.colors.BLUE,
            )
        )
        
        self.controls.append(
            ft.Tabs(
                scrollable=True,
                expand=1,
                tabs=[
                    ft.Tab(
                        text="APIs e Credenciais",
                        content=ft.Column(
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
                    ),
                    ft.Tab(
                        text="Acrônimos",
                        content=ft.Container(
                            height=500,
                            content=ft.Column(
                                controls=[
                                    self.acronym_key,
                                    self.acronym_value,
                                    self.add_acronym_button,
                                    self.acronyms_list
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            )
                        )
                    ),
                    ft.Tab(
                        text="Combinações Comuns",
                        content=ft.Container(
                            height=500,
                            content=ft.Column(
                                controls=[
                                    self.common_combination_key,
                                    self.common_combination_value,
                                    self.add_common_combination_button,
                                    self.common_combinations_list
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            )
                        )
                    ),
                    ft.Tab(
                        text="Contrações",
                        content=ft.Container(
                            height=500,
                            content=ft.Column(
                                controls=[
                                    self.contraction_key,
                                    self.contraction_value,
                                    self.add_contraction_button,
                                    self.contractions_list
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            )
                        )
                    ),
                    ft.Tab(
                        text="Palavrões",
                        content=ft.Container(
                            height=500,
                            content=ft.Column(
                                controls=[
                                    ft.Text("Coloque aqui palavrões que devem ser filtrados durante o tratamento do texto. Eles serão substituidos pelo eufemismo inclusos."),
                                    self.profanity_key,
                                    self.profanity_value,
                                    self.add_profanity_button,
                                    self.profanities_list
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            )
                        )
                    ),
                    ft.Tab(
                        text="Subreddits",
                        content=ft.Container(
                            height=500,
                            content=ft.Column(
                                controls=[
                                    self.subreddit_name,
                                    self.subreddit_description,
                                    self.add_subreddit_button,
                                    self.subreddits_list
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                            )
                        )
                    ),
                    ft.Tab(
                        text="Vídeos",
                        content=ft.Column(
                                controls=[
                                    self.video_url,
                                    self.add_video_button,
                                    self.videos_list
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.START,
                                horizontal_alignment=ft.CrossAxisAlignment.START,
                        )
                    ),
                    ft.Tab(
                        text="Vozes",
                        content=ft.Column(
                            controls=[
                                ft.Row(controls=[
                                    ft.Text("Você pode adicionar qualquer foz da AWS, em en-us"),
                                    ft.TextButton("Vozes disponíveis", on_click=lambda e: self.page.launch_url("https://docs.aws.amazon.com/polly/latest/dg/available-voices.html"))
                                ]),
                                
                                self.voice_female_name,
                                self.add_voice_female_button,
                                self.voice_male_name,
                                self.add_voice_male_button,
                                self.voices_list
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        )
                    )
                ]
            )
        )

        self.load_acronyms()
        self.load_common_combinations()
        self.load_contractions()
        self.load_profanities()
        self.load_subreddits()
        self.load_videos()
        self.load_voices()

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

    def load_acronyms(self):
        try:
            with open(self.acronyms_file, 'r') as file:
                self.acronyms = json.load(file)
                self.update_acronyms_list()
        except Exception as e:
            print(f"Erro ao carregar acrônimos: {e}")

    def save_acronyms(self):
        try:
            with open(self.acronyms_file, 'w') as file:
                json.dump(self.acronyms, file, indent=4)
                sb = ft.SnackBar(content=ft.Text("Acrônimos salvos com sucesso!"), 
                                 duration=6000,
                                 show_close_icon=True 
                                 )
                self.page.snack_bar = sb
                self.page.snack_bar.open=True
                self.page.update()
        except Exception as e:
            print(f"Erro ao salvar acrônimos: {e}")

    def update_acronyms_list(self):
        self.acronyms_list.controls.clear()
        for key, value in self.acronyms.items():
            self.acronyms_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{key}: {value}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, k=key: self.remove_acronym(k)
                    )
                )
            )
        self.page.update()

    def add_acronym(self, e):
        key = self.acronym_key.value.strip()
        value = self.acronym_value.value.strip()
        if key and value:
            self.acronyms[key] = value
            self.update_acronyms_list()
            self.save_acronyms()
            self.acronym_key.value = ""
            self.acronym_value.value = ""
            self.page.update()

    def remove_acronym(self, key):
        if key in self.acronyms:
            del self.acronyms[key]
            self.update_acronyms_list()
            self.save_acronyms()

    def load_common_combinations(self):
        try:
            with open(self.common_combinations_file, 'r') as file:
                self.common_combinations = json.load(file)
                self.update_common_combinations_list()
        except Exception as e:
            print(f"Erro ao carregar combinações comuns: {e}")

    def save_common_combinations(self):
        try:
            with open(self.common_combinations_file, 'w') as file:
                json.dump(self.common_combinations, file, indent=4)
                sb = ft.SnackBar(content=ft.Text("Combinações comuns salvas com sucesso!"), 
                                 duration=6000,
                                 show_close_icon=True 
                                 )
                self.page.snack_bar = sb
                self.page.snack_bar.open=True
                self.page.update()
        except Exception as e:
            print(f"Erro ao salvar combinações comuns: {e}")

    def update_common_combinations_list(self):
        self.common_combinations_list.controls.clear()
        for key, value in self.common_combinations.items():
            self.common_combinations_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{key}: {value}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, k=key: self.remove_common_combination(k)
                    )
                )
            )
        self.page.update()

    def add_common_combination(self, e):
        key = self.common_combination_key.value.strip()
        value = self.common_combination_value.value.strip()
        if key and value:
            self.common_combinations[key] = value
            self.update_common_combinations_list()
            self.save_common_combinations()
            self.common_combination_key.value = ""
            self.common_combination_value.value = ""
            self.page.update()

    def remove_common_combination(self, key):
        if key in self.common_combinations:
            del self.common_combinations[key]
            self.update_common_combinations_list()
            self.save_common_combinations()

    def load_contractions(self):
        try:
            with open(self.contractions_file, 'r') as file:
                self.contractions = json.load(file)
                self.update_contractions_list()
        except Exception as e:
            print(f"Erro ao carregar contrações: {e}")

    def save_contractions(self):
        try:
            with open(self.contractions_file, 'w') as file:
                json.dump(self.contractions, file, indent=4)
                sb = ft.SnackBar(content=ft.Text("Contrações salvas com sucesso!"), 
                                 duration=6000,
                                 show_close_icon=True 
                                 )
                self.page.snack_bar = sb
                self.page.snack_bar.open=True
                self.page.update()
        except Exception as e:
            print(f"Erro ao salvar contrações: {e}")

    def update_contractions_list(self):
        self.contractions_list.controls.clear()
        for key, value in self.contractions.items():
            self.contractions_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{key}: {value}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, k=key: self.remove_contraction(k)
                    )
                )
            )
        self.page.update()

    def add_contraction(self, e):
        key = self.contraction_key.value.strip()
        value = self.contraction_value.value.strip()
        if key and value:
            self.contractions[key] = value
            self.update_contractions_list()
            self.save_contractions()
            self.contraction_key.value = ""
            self.contraction_value.value = ""
            self.page.update()

    def remove_contraction(self, key):
        if key in self.contractions:
            del self.contractions[key]
            self.update_contractions_list()
            self.save_contractions()

    def load_profanities(self):
        try:
            with open(self.profanities_file, 'r') as file:
                self.profanities = json.load(file)
                self.update_profanities_list()
        except Exception as e:
            print(f"Erro ao carregar palavrões: {e}")

    def save_profanities(self):
        try:
            with open(self.profanities_file, 'w') as file:
                json.dump(self.profanities, file, indent=4)
                sb = ft.SnackBar(content=ft.Text("Palavrões salvos com sucesso!"), 
                                 duration=6000,
                                 show_close_icon=True 
                                 )
                self.page.snack_bar = sb
                self.page.snack_bar.open=True
                self.page.update()
        except Exception as e:
            print(f"Erro ao salvar palavrões: {e}")

    def update_profanities_list(self):
        self.profanities_list.controls.clear()
        for key, value in self.profanities.items():
            self.profanities_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{key}: {value}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, k=key: self.remove_profanity(k)
                    )
                )
            )
        self.page.update()

    def add_profanity(self, e):
        key = self.profanity_key.value.strip()
        value = self.profanity_value.value.strip()
        if key and value:
            self.profanities[key] = value
            self.update_profanities_list()
            self.save_profanities()
            self.profanity_key.value = ""
            self.profanity_value.value = ""
            self.page.update()

    def remove_profanity(self, key):
        if key in self.profanities:
            del self.profanities[key]
            self.update_profanities_list()
            self.save_profanities()

    def load_subreddits(self):
        try:
            with open(self.subreddits_file, 'r') as file:
                data = json.load(file)
                self.subreddits = data['subreddits']
                self.update_subreddits_list()
        except Exception as e:
            print(f"Erro ao carregar subreddits: {e}")

    def save_subreddits(self):
        try:
            with open(self.subreddits_file, 'w') as file:
                json.dump({"subreddits": self.subreddits}, file, indent=4)
                sb = ft.SnackBar(content=ft.Text("Subreddits salvos com sucesso!"), 
                                 duration=6000,
                                 show_close_icon=True 
                                 )
                self.page.snack_bar = sb
                self.page.snack_bar.open=True
                self.page.update()
        except Exception as e:
            print(f"Erro ao salvar subreddits: {e}")

    def update_subreddits_list(self):
        self.subreddits_list.controls.clear()
        for item in self.subreddits:
            self.subreddits_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{item['name']}: {item['description']}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, i=item: self.remove_subreddit(i)
                    )
                )
            )
        self.page.update()

    def add_subreddit(self, e):
        name = self.subreddit_name.value.strip()
        description = self.subreddit_description.value.strip()
        if name and description:
            self.subreddits.append({"name": name, "description": description})
            self.update_subreddits_list()
            self.save_subreddits()
            self.subreddit_name.value = ""
            self.subreddit_description.value = ""
            self.page.update()

    def remove_subreddit(self, item):
        if item in self.subreddits:
            self.subreddits.remove(item)
            self.update_subreddits_list()
            self.save_subreddits()

    def load_videos(self):
        try:
            with open(self.videos_file, 'r') as file:
                data = json.load(file)
                self.videos = data['videos']
                self.update_videos_list()
        except Exception as e:
            print(f"Erro ao carregar vídeos: {e}")

    def save_videos(self):
        try:
            with open(self.videos_file, 'w') as file:
                json.dump({"videos": self.videos}, file, indent=4)
                sb = ft.SnackBar(content=ft.Text("Vídeos salvos com sucesso!"), 
                                 duration=6000,
                                 show_close_icon=True 
                                 )
                self.page.snack_bar = sb
                self.page.snack_bar.open=True
                self.page.update()
        except Exception as e:
            print(f"Erro ao salvar vídeos: {e}")

    def update_videos_list(self):
        self.videos_list.controls.clear()
        for item in self.videos:
            self.videos_list.controls.append(
                ft.ListTile(
                    title=ft.Text(f"{item['video']}"),
                    trailing=ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=lambda e, i=item: self.remove_video(i)
                    )
                )
            )
        self.page.update()

    def add_video(self, e):
        url = self.video_url.value.strip()
        if url:
            self.videos.append({"video": url})
            self.update_videos_list()
            self.save_videos()
            self.video_url.value = ""
            self.page.update()

    def remove_video(self, item):
        if item in self.videos:
            self.videos.remove(item)
            self.update_videos_list()
            self.save_videos()

    def load_voices(self):
        try:
            with open(self.voices_file, 'r') as file:
                self.voices = json.load(file)
                self.update_voices_list()
        except Exception as e:
            print(f"Erro ao carregar vozes: {e}")

    def save_voices(self):
        try:
            with open(self.voices_file, 'w') as file:
                json.dump(self.voices, file, indent=4)
                sb = ft.SnackBar(content=ft.Text("Vozes salvas com sucesso!"), 
                                 duration=6000,
                                 show_close_icon=True 
                                 )
                self.page.snack_bar = sb
                self.page.snack_bar.open=True
                self.page.update()
        except Exception as e:
            print(f"Erro ao salvar vozes: {e}")

    def update_voices_list(self):
        self.voices_list.controls.clear()
        for gender, voices in self.voices.items():
            for voice in voices:
                self.voices_list.controls.append(
                    ft.ListTile(
                        title=ft.Text(f"{voice['name']} ({gender})"),
                        trailing=ft.IconButton(
                            icon=ft.icons.DELETE,
                            on_click=lambda e, v=voice, g=gender: self.remove_voice(g, v)
                        )
                    )
                )
        self.page.update()

    def add_voice(self, e, gender):
        name = self.voice_female_name.value.strip() if gender == 'females' else self.voice_male_name.value.strip()
        if name:
            self.voices[gender].append({"name": name})
            self.update_voices_list()
            self.save_voices()
            if gender == 'females':
                self.voice_female_name.value = ""
            else:
                self.voice_male_name.value = ""
            self.page.update()

    def remove_voice(self, gender, voice):
        if voice in self.voices[gender]:
            self.voices[gender].remove(voice)
            self.update_voices_list()
            self.save_voices()
