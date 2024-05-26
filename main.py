from lib.reddit_utils import *
from lib.youtube_utils import *
from lib.video_utils import *
from lib.subtitles_utils import *
from lib.file_utils import *
from lib.audio_utils import *
from lib.interface_utils import *
import moviepy.editor as mp
import uuid

# Função principal
def main():
    mk_dirs()
    subtitle_path = 'tmp/subtitles'
    audio_path = 'tmp/audio'

    selected_story = select_story()
    if not selected_story:
        return

    # Escolhe o sexo do narrador
    voice = get_random_voice(set_gender())
    
    # Baixar vídeo de gameplay do YouTube
    print("Baixando o video de fundo")
    youtube_url = get_random_background_video()
    download_youtube_video(youtube_url, output_dir='tmp')

    # Gerar narração
    print_msg("Preparando narração, aguarde...")

    unclean_text = selected_story['title'] + ". " + selected_story['text']
    text = replace_profanities(unclean_text)

    paragraphs = []
    estimate = estimate_time(text)

    if estimate<180.0:
        paragraphs.append(text)
    else:
        print(int(estimate//180))
        paragraphs = split_paragraphs(text,int(estimate//180))

    print_msg(f'Video em 1 parte, gerando narração...' if len(paragraphs) == 1 else f'Video em {len(paragraphs)} partes, processando as partes')

    for i in range(0, len(paragraphs)):
        print_msg(f"Gerando áudio da parte {i+1}")
        narration_filename = f"{audio_path}/__part_{i}__.mp3"
        text_to_speech(paragraphs[i], narration_filename, voice, "en-US", "mp3", engine='neural')
    
    # narration_filename = "tmp/__narration__.mp3"
    # text_to_speech(text, narration_filename, gender, "en-US", "mp3", engine='neural')
    # Carregar vídeo de gameplay
    gameplay_video = mp.VideoFileClip("tmp/__yt1__.mp4")
    
    # Adicionar narração ao vídeo
    
    narrations = [ f for f in os.listdir(audio_path) if f.endswith('.mp3') ]

    print_msg(f'Video em 1 parte, processando...' if len(narrations) == 1 else f'Video em {len(narrations)} partes, processando as partes')

    output_path = f'output/{uuid.uuid4()}'

    os.mkdir(output_path)

    for i in range(len(paragraphs)):
        narration_audio = mp.AudioFileClip(f"{audio_path}/__part_{i}__.mp3")
        video_with_audio = gameplay_video.set_audio(narration_audio)
        print_msg("Formatando para o formato do tiktok")
        formatted_video = format_video_to_9x16(video_with_audio)
        print_msg("Adicionando legendas ao video")
        generate_subtitles(f'{audio_path}/__part_{i}__.mp3', f'{subtitle_path}/__part_{i}.srt')
        video_with_subtitles = add_subtitles_to_video(formatted_video, 
                                                      f'{subtitle_path}/__part_{i}.srt', 
                                                      i+1, 
                                                      len(paragraphs))
        export_single(video_with_subtitles, 
                      narration_audio.duration, 
                      f'{output_path}/output_part_{i+1}.mp4')
        
    
    # Formatar vídeo para 9x16
    
    # Adiciona legendas ao video 
    
    # generate_subtitles(text, narration.duration)
    
    
    # sync_subtitles()

    # video_with_subtitles = add_subtitles_to_video(formatted_video, 'tmp/__subtitles__.srt')

    # if narration.duration>120:
        
    #     print_msg(f"Duração total do video original é {narration.duration}\nDividindo em 2 partes")
        
    #     segments = split_video(video_with_subtitles, narration.duration, narration.duration/2)
    #     export_segments(segments, output_path)
    # else:
        
    #     print_msg("Exportando video")
        
    #     export_single(video_with_subtitles, narration.duration, f'{output_path}/output.mp4')
    
    remove_tmp()
    
    for filename in os.listdir('output'):
        print(f"Arquivo {filename} gerado")

if __name__ == '__main__':
    main()
