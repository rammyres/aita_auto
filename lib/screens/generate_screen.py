import flet as ft
from lib.reddit_utils import *
from lib.video_utils import *
from lib.audio_utils import *
from lib.subtitles_utils import *
from lib.youtube_utils import *
from lib.widgets.processing_card import ProcessingCard

class GenerateScreen(ft.View):
    def __init__(self, page, text, gender, go_home):
        super().__init__(route="/generate_screen")
        self.page = page  # Referência à página

        def sb_notify(text):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(text), 
                show_close_icon=True
            )
            self.page.snack_bar.open = True
            self.page.update()

        self.text = text
        self.voice = get_random_voice(gender)
        self.audio_path = 'output/tmp/audio'
        self.processing_column = ft.Column(alignment=ft.MainAxisAlignment.START)

        self.processing_narration = ProcessingCard("Processando narração")
        self.processing_subtitles = ProcessingCard("Gerando legendas")
        self.processing_bgvideo = ProcessingCard("Baixando video de fundo")
        
        self.processing_column.controls.extend([
            self.processing_narration, 
            self.processing_subtitles,
            self.processing_bgvideo
        ])
        
        self.estimate = estimate_time(self.text)

        self.number_parts = int(self.estimate // 180)
        if self.number_parts == 0:
            self.number_parts = 1
        if self.number_parts <= 1 and self.estimate > 180.0:
            self.number_parts = 2
        
        for i in range(self.number_parts):
            self.processing_column.controls.append(ProcessingCard(f"Video: parte {i+1}"))

        self.text_parts = []

        if self.number_parts == 1:
            self.text_parts.append(self.text)
        else:
            self.text_parts.extend(split_paragraphs(text=text, number_of_parts=self.number_parts))

        self.controls = [
            ft.AppBar(
                title=ft.Text(
                    "Gerando seu video", 
                    font_family="roboto",
                    weight=ft.FontWeight.BOLD, 
                    color=ft.colors.WHITE
                ), 
                center_title=True, 
                bgcolor=ft.colors.BLUE
            ),
            ft.Container(height=500, content=self.processing_column),
            ft.Column(
                controls=[
                    ft.ElevatedButton(
                        text="Voltar para home", 
                        bgcolor=ft.colors.BLUE,
                        color=ft.colors.WHITE,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                        on_click=go_home
                    ),
                    # ft.ElevatedButton(text="Mostrar lista de videos disponíveis", on_click=show_videos),
                ],
                alignment=ft.MainAxisAlignment.END
            )
        ]

        for i, part in enumerate(self.text_parts):
            sb_notify(f"Gerando audio da parte {i+1}")
            narration_filename = f"{self.audio_path}/__part_{i}__.mp3"
            text_to_speech(part, narration_filename, self.voice, "en-US", "mp3", engine='neural')
        self.processing_narration.update_check(is_complete=True)
