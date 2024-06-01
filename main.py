from lib.reddit_utils import *
from lib.youtube_utils import *
from lib.video_utils import *
from lib.subtitles_utils import *
from lib.file_utils import *
from lib.audio_utils import *
from lib.interface_utils import selection_menu
from lib.data_utils import save_to_json
import moviepy.editor as mp
import uuid, gc, os

# Função principal
def main():
    # Verifica se os arquivos de configuração estão disponíveis e os cria se não estiverem
    # Os arquivos criados são para os serviços aws, aai e reddit
    check_configs()
    os.environ["TOKENIZERS_PARALLELISM"] = "false" # Disabilita paralelismo para uso do BeRT
                                                   # na verificação ortográfica 

    while True:
        selected_story = None
        choice = selection_menu()
        if choice: # Caso a escolha seja válida processe 
            if choice[0] == 'video': # Se a escolha for um vídeo do registro
                choice[1]['videos'].sort(key=lambda x:x['video']) # Ordena os videos existentes
                i = 1
                for v in choice[1]['videos']:
                    print(f"Caminho para parte {i}: {v['video']}")
                    i+=1
                input("Pressione ENTER para continuar")
                continue
            else:
                selected_story = choice[1]

        if not selected_story:
            continue

        # Cria as pastas temporárias e de saída somente após a escolha da história
        subtitle_path = 'tmp/subtitles'
        audio_path = 'tmp/audio'
        mk_dirs()

        # Escolhe o sexo do narrador
        voice = get_random_voice(set_gender())
        print_msg(f"Voz escolhida: {voice}")

        # Gerar narração
        print_msg("Preparando narração, aguarde...")

        unclean_text = selected_story['title'] + ". " + selected_story['text']
        text = prepare_text(unclean_text)

        paragraphs = []
        # Estima o tempo de duração com base na contagem de palavras
        estimate = estimate_time(text)
        print_msg("Estimativa de tempo {:.2f}".format(estimate))

        # Divide o texto em partes se o tempo for superior a 3 minutos
        parts = 1 if int(estimate//180) <= 1 else int(estimate//180)
        if estimate>180.0 and parts == 1: # Certifica que o video terá pelo menos
            parts+=1                      # 2 partes, caso seja maior que 3 minutos
    
        # Prepara o texto para processamento, separando em segmentos de paragrafos
        if parts == 1:
            paragraphs.append(text)
        else:
            paragraphs = split_paragraphs(text, parts)

    
        # Prepara a narração
        print_msg(f'Video em 1 parte, gerando narração...' if len(paragraphs) == 1 else f'Video em {len(paragraphs)} partes, processando as partes')
        for i in range(0, len(paragraphs)):
            print_msg(f"Gerando áudio da parte {i+1}")
            narration_filename = f"{audio_path}/__part_{i}__.mp3"
            text_to_speech(paragraphs[i], narration_filename, voice, "en-US", "mp3", engine='neural')
        
        # Baixar vídeo de gameplay do YouTube
        print_msg("Baixando o video de fundo")
        youtube_url = get_random_background_video()
        download_youtube_video(youtube_url, output_dir='tmp')
        
        # Carregar vídeo de gameplay
        gameplay_video = mp.VideoFileClip("tmp/__yt1__.mp4")

        # Preparar diretório de saída do do vídeo pronto
        output_path = f'output/{uuid.uuid4()}'
        os.mkdir(output_path)

        # Criar videos prontos 
        for i in range(len(paragraphs)):
            # Cria o clipe de narração para inclusão do video a partir do audio gerado pela Polly
            narration_audio = mp.AudioFileClip(f"{audio_path}/__part_{i}__.mp3") 
            print_msg(f'Video em 1 parte (tempo de {narration_audio.duration}s), processando...' if len(paragraphs) == 1 else f'Parte em {i+1} processamento, tempo total {narration_audio.duration}')
            video_with_audio = gameplay_video.set_audio(narration_audio) # Inclui o áudio no video de fundo
            print_msg("Formatando para o formato do tiktok") 
            formatted_video = format_video_to_9x16(video_with_audio) # Recorta o vídeo para o formato 9x16
            
            # Gera as legendas a partir do áudio de cada uma as partes
            print_msg("Adicionando legendas ao video")
            generate_subtitles(f'{audio_path}/__part_{i}__.mp3', f'{subtitle_path}/__part_{i}.srt')

            # Cria a camada de legendas e caption da parte
            video_with_subtitles = add_subtitles_to_video(formatted_video, 
                                                        f'{subtitle_path}/__part_{i}.srt', 
                                                        i+1, 
                                                        len(paragraphs))
            
            generated_videos = []
            # Exporta o video pronto
            output_filename = f'{output_path}/output_part_{i+1}.mp4'
            export_single(video_with_subtitles, 
                        narration_audio.duration, 
                        output_filename)
        
        remove_tmp() # Remove arquivos temporários
        
        for filename in os.listdir(output_path):
            filepath = f'{output_path}/{filename}'
            print(f"Arquivo {filepath} gerado")
            generated_videos.append({'video':filepath}) # Gera referência do caminho do ultimo video gerado

        # Salvar os detalhes do vídeo no arquivo JSON
        video_data = {
            'title': selected_story['title'],
            'videos': generated_videos
        }
        save_to_json(video_data)

        with open(f"{output_path}/fulltext.txt", 'w') as fp:
            fp.write(text)
        
        notify() # Toca uma notificação ao fim do processamento da tarefa de geração atual

        input("Pressione ENTER para continuar")
        gc.collect()

if __name__ == '__main__':
    main()
