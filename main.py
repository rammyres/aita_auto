from lib.reddit_utils import *
from lib.youtube_utils import download_youtube_video
from lib.video_utils import *
from lib.subtitles_utils import *
from lib.file_utils import remove_tmp
import moviepy.editor as mp
import uuid

def print_msg(msg):
    print("==================##################==================")
    print(msg)
    print("==================##################==================")


# Função para exibir menu e selecionar história
def select_story():
    print("Selecione uma história para processar:")
    print("1. Escolher entre os 10 posts mais populares")
    print("2. Escolher entre 10 posts aleatórios entre os 500 mais populares")
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
# Verifica se o diretório temporário existe
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

# Verifica se o diretório de saida existe
    if not os.path.exists('output'):
        os.mkdir('output')

    selected_story = select_story()
    if not selected_story:
        return

    youtube_url = input("Link do video de fundo (youtube): ")  
    print("Baixando o video de fundo")
    
    # Baixar vídeo de gameplay do YouTube com nome personalizado
    # downloaded_video_path = download_youtube_video(youtube_url, sequence_number=1, output_dir='tmp')
    downloaded_video_path = download_youtube_video(youtube_url, output_dir='tmp')
    
    # Gerar narração
    
    print_msg("Gerando narração, aguarde...")
    
    narration_filename = "tmp/__narration__.mp3"
    text = selected_story['title'] + ". " + selected_story['text']
    # text_to_speech(text, narration_filename, "Joanna", "en-US", "mp3", engine='neural')
    text_to_speech(text, narration_filename, "Matthew", "en-US", "mp3", engine='neural')
    # Carregar vídeo de gameplay
    gameplay_video = mp.VideoFileClip("tmp/__yt1__.mp4")
    
    # Adicionar narração ao vídeo
    
    print_msg("Adicionando narração ao video")
    
    narration = mp.AudioFileClip(narration_filename)
    video_with_audio = gameplay_video.set_audio(narration)
    
    # Formatar vídeo para 9x16
    
    print_msg("Formatando para o formato do tiktok")
    
    formatted_video = format_video_to_9x16(video_with_audio)
    
    # Adiciona legendas ao video 
    print_msg("Adicionando legendas ao video")
    # generate_subtitles(text, narration.duration)
    generate_subtitles()
    print_msg("Sincronizando texto")
    
    # sync_subtitles()

    video_with_subtitles = add_subtitles_to_video(formatted_video, 'tmp/__subtitles__.srt')
    
    output_path = f'output/{uuid.uuid4()}'

    os.mkdir(output_path)

    if narration.duration>120:
        
        print_msg(f"Duração total do video original é {narration.duration}\nDividindo em 2 partes")
        
        segments = split_video(video_with_subtitles, narration.duration, narration.duration/2)
        export_segments(segments, output_path)
    else:
        
        print_msg("Exportando video")
        
        export_single(video_with_subtitles, narration.duration, f'{output_path}/output.mp4')
    
    remove_tmp()
    
    for filename in os.listdir('output'):
        print(f"Arquivo {filename} gerado")

if __name__ == '__main__':
    main()
