import uuid
import os
import flet as ft
import moviepy.editor as mp
from lib.utils.reddit_utils import *
from lib.utils.video_utils import *
from lib.utils.audio_utils import *
from lib.utils.subtitles_utils import *
from lib.utils.youtube_utils import *
from lib.utils.data_utils import *
from lib.utils.file_utils import mk_dirs, remove_tmp
from lib.widgets.processing_card import ProcessingCard

class GenerateScreen(ft.View):
    def __init__(self, page, title, text, gender, go_video_screen, go_home):
        super().__init__(route="/generate")
        self.page = page  # Referência à página
        self.go_video_screen = go_video_screen
        self.title = title
        self.text = ' '.join([title, text])
        self.voice = get_random_voice(gender)
        self.audio_path = os.path.join("tmp", "audio")
        self.subtitles_path = os.path.join("tmp", "subtitles")
        self.bgvideo = os.path.join("tmp","__yt1__.mp4")
        self.video_cards = []
        self.generated_videos = []
        self.generated_videos_buttons = []
        self.gv_column = ft.Column(alignment=ft.MainAxisAlignment.START)
        self.processing_column = ft.Column(alignment=ft.MainAxisAlignment.START)

        self.processing_narration = ProcessingCard("Processando narração")
        self.processing_subtitles = ProcessingCard("Gerando legendas")
        self.processing_bgvideo = ProcessingCard("Baixando video de fundo")
        
        self.processing_column.controls.extend([
            self.processing_narration, 
            self.processing_subtitles,
            self.processing_bgvideo
        ])
        
        self.go_home_button = ft.IconButton(
            icon=ft.icons.HOME_FILLED, 
            icon_color=ft.colors.WHITE,
            on_click=go_home
        )

        self.appbar = ft.AppBar(
                title=ft.Text(
                    "Gerando seu video", 
                    font_family="roboto",
                    weight=ft.FontWeight.BOLD, 
                    color=ft.colors.WHITE
                ),
                center_title=True, 
                bgcolor=ft.colors.BLUE
            )

        self.controls = [
            self.appbar,
            ft.Container(height=500, content=self.processing_column),
            self.gv_column
        ]

    def sb_notify(self, text):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(text),
            duration=5000, 
            show_close_icon=True
        )
        self.page.snack_bar.open = True
        self.page.update()

    def process_narration(self):
        self.text_parts = []

        if self.number_parts == 1:
            self.text_parts.append(self.text)
        else:
            self.text_parts.extend(split_paragraphs(text=self.text, number_of_parts=self.number_parts))

        self.processing_narration.toggle_loading(True)

        for i, part in enumerate(self.text_parts):
            self.sb_notify(f"Gerando audio da parte {i+1}")
            narration_filename = os.path.join(self.audio_path, f"__part_{i}__.mp3")
            text_to_speech(part, narration_filename, self.voice, "en-US", "mp3", engine='neural')
        self.processing_narration.update_check(is_complete=True)
        self.processing_narration.toggle_loading(False)

    def process_subtitles(self):
        self.sb_notify("Gerando as legendas")
        self.processing_subtitles.toggle_loading(True)
        for i in range(len(self.text_parts)): 
            _audio_path=os.path.join(self.audio_path, f"__part_{i}__.mp3")
            _subtitle_path= os.path.join(self.subtitles_path, f"__part_{i}.srt")
            generate_subtitles(_audio_path, _subtitle_path)
        self.processing_subtitles.update_check(is_complete=True)
        self.processing_subtitles.toggle_loading(False)

    def download_bgvideo(self):
        self.sb_notify("Baixando video de fundo")
        self.processing_bgvideo.toggle_loading(True)
        bg_video = get_random_background_video()
        download_youtube_video(bg_video)
        self.processing_bgvideo.update_check(is_complete=True)
        self.processing_bgvideo.toggle_loading(False)

    def processing_videos(self):
        bgvideo = mp.VideoFileClip(self.bgvideo)
        output_path = os.path.join("output", str(uuid.uuid4()))
        os.mkdir(output_path)
        for i in range(len(self.text_parts)):
            self.sb_notify(f"Gerando video parte {i+1}")
            self.video_cards[i].toggle_loading(True)
            narration_audio = mp.AudioFileClip(os.path.join(self.audio_path, f"__part_{i}__.mp3")) 
            video_with_audio = bgvideo.set_audio(narration_audio) # Inclui o áudio no video de fundo
            formatted_video = format_video_to_9x16(video_with_audio)
            video_with_subtitles = add_subtitles_to_video(formatted_video, 
                                                          os.path.join(self.subtitles_path, f"__part_{i}.srt"),
                                                          i + 1, 
                                                          len(self.text_parts))
            output_filename = os.path.join(output_path, f"output_part_{i + 1}.mp4")
            export_single(video_with_subtitles, 
                        narration_audio.duration, 
                        output_filename)
            self.video_cards[i].update_check(is_complete=True)
            self.video_cards[i].toggle_loading(False)

        for i, filename in enumerate(os.listdir(output_path)):
            filepath = f'{output_path}/{filename}'
            button = ft.TextButton(f"Parte {i+1}", on_click=lambda e, path=filepath: self.go_video_screen(path))
            self.generated_videos_buttons.append(button)
            self.generated_videos.append({'video': filepath}) # Gera referência do caminho do ultimo video gerado

        self.gv_column.controls.extend(self.generated_videos_buttons)

        # Atualize a página para refletir as novas alterações nos controles
        self.page.update()

        # Salvar os detalhes do vídeo no arquivo JSON
        video_data = {
            'title': self.title,
            'videos': self.generated_videos
        }
        
        save_to_json(video_data)

        with open(os.path.join(output_path, "fulltext.txt"), 'w') as fp:
            fp.write(self.text)
        
        notify()

    def did_mount(self):
        mk_dirs()
        self.estimate = estimate_time(self.text)

        self.number_parts = int(self.estimate // 180)
        if self.number_parts == 0:
            self.number_parts = 1
        if self.number_parts <= 1 and self.estimate > 180.0:
            self.number_parts = 2
        
        for i in range(self.number_parts):
            card = ProcessingCard(f"Video: parte {i+1}")
            self.video_cards.append(card)
            self.processing_column.controls.append(card)

        self.process_narration()
        self.process_subtitles()
        self.download_bgvideo()
        self.processing_videos()
        self.appbar.actions.append(self.go_home_button)
        self.appbar.update()
        remove_tmp()
