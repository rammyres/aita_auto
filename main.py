from lib.reddit_utils import *
from lib.youtube_utils import download_youtube_video
from lib.video_utils import *

import moviepy.editor as mp

# Função para exibir menu e selecionar história
def select_story():
    print("Selecione uma história para processar:")
    print("1. Escolher entre os 10 posts mais populares")
    print("2. Escolher entre 10 posts aleatórios entre os 200 mais populares")
    print("3. Inserir URL de um post específico")
    choice = int(input("Digite o número da opção desejada: "))
    
    if choice == 1:
        stories = get_popular_aita_stories(10)
        print("Escolha um dos seguintes posts:")
        for i, story in enumerate(stories):
            print(f"{i + 1}. {story['title']}")
            print(f"   Link: {story['url']}")
        story_choice = int(input("Digite o número da história desejada: ")) - 1
        return stories[story_choice]
    
    if choice == 2:
        stories = get_random_aita_stories(10)
        print("Escolha um dos seguintes posts:")
        for i, story in enumerate(stories):
            print(f"{i + 1}. {story['title']}")
            print(f"   Link: {story['url']}")
        story_choice = int(input("Digite o número da história desejada: ")) - 1
        return stories[story_choice]
    
    elif choice == 3:
        url = input("Insira a URL do post específico: ")
        story = get_story_from_url(url)
        if story:
            return story
        else:
            print("URL inválida ou post não encontrado.")
            return None
    
    else:
        print("Opção inválida.")
        return None

# Função principal
def main():
    selected_story = select_story()
    if not selected_story:
        return

    youtube_url = input("Link do video de fundo (youtube): ")  
    print("Baixando o video de fundo")
    
    # Baixar vídeo de gameplay do YouTube com nome personalizado
    downloaded_video_path = download_youtube_video(youtube_url, sequence_number=1, output_dir='downloads')
    
    # Gerar narração
    print("Gerando narração, aguarde...")
    narration_filename = "narration.mp3"
    text = selected_story['title'] + ". " + selected_story['text']
    text_to_speech(text, narration_filename, "Joanna", "en-US", "mp3")
    
    # Carregar vídeo de gameplay
    gameplay_video = mp.VideoFileClip("{}/yt1.mp4".format(downloaded_video_path))
    
    # Adicionar narração ao vídeo

    print("Adicionando narração ao video")
    narration = mp.AudioFileClip(narration_filename)
    video_with_audio = gameplay_video.set_audio(narration)
    
    # Formatar vídeo para 9x16
    print("Formatando para o formato do tiktok")
    formatted_video = format_video_to_9x16(video_with_audio)
    

    # Adicionar título no início do vídeo
    print("Adicionando legendas ao video")
    subtitles = generate_subtitles(text, narration.duration)
    print(subtitles)
    video_with_subtitles = formatted_video
    for subtitle, start, end in subtitles:
        video_with_subtitles = add_text_to_video(video_with_subtitles, 
                                                 subtitle, 
                                                 start, 
                                                 end - start, 
                                                 position=('center', 'bottom'))
    
    # Dividir vídeo em segmentos de 1 minuto e 1 segundo
    print("Dividindo em segmentos de 1min e 1 segundo")
    segments = split_video(video_with_subtitles, "narration.mp3", 61)
    
    # Exportar segmentos com legendas para TikTok
    export_segments(segments)
    
    # Remover arquivo de narração temporário
    remove_temp_audio(narration_filename)

if __name__ == '__main__':
    main()
