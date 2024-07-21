from lib.utils.config_utils import *
check_requirements('requirements.txt')

from lib.utils.reddit_utils import *
from lib.utils.youtube_utils import *
from lib.utils.video_utils import *
from lib.utils.subtitles_utils import *
from lib.utils.file_utils import *
from lib.utils.audio_utils import *
from lib.utils.interface_utils import selection_menu, cls
from lib.utils.data_utils import save_to_json
from blessed import Terminal
import moviepy.editor as mp
import uuid, gc, os, sys

# Função principal
def main():
    # Verifica se os arquivos de configuração estão disponíveis e os cria se não estiverem
    # Os arquivos criados são para os serviços aws, aai e reddit
    check_configs('text')
    os.environ["TOKENIZERS_PARALLELISM"] = "false" # Disabilita paralelismo para uso do BeRT
                                                   # na verificação ortográfica 
    cls()
    term = Terminal()
    while True:
        selected_story = None
        choice = selection_menu()
        if choice: # Caso a escolha seja válida processe 
            if choice[0] == 'video': # Se a escolha for um vídeo do registro
                choice[1]['videos'].sort(key=lambda x:x['video']) # Ordena os videos existentes
                i = 1
                for v in choice[1]['videos']:
                    print(f"Caminho para parte {i}: {v['video']}")
                    i += 1
                input("Pressione ENTER para continuar")
                continue
            else:
                selected_story = choice[1]

        if not selected_story:
            continue

        # Cria as pastas temporárias e de saída somente após a escolha da história
        subtitle_path = os.path.join('tmp','subtitles')
        audio_path = os.path.join('tmp','audio')
        mk_dirs()

        unclean_text = selected_story['title'] + ". " + selected_story['text']
        
        # Escolhe o sexo do narrador
        voice = get_random_voice(set_gender(unclean_text))
        print_msg(f"Voz escolhida: {voice}")

        # Gerar narração
        print_msg("Preparando narração, aguarde...")
        text = prepare_text(unclean_text)

        paragraphs = []
        # Estima o tempo de duração com base na contagem de palavras
        estimate = estimate_time(text)
        print_msg("Estimativa de tempo {:.2f}".format(estimate))

        # Divide o texto em partes se o tempo for superior a 3 minutos
        parts = 1 if int(estimate // 180) <= 1 else int(estimate // 180)
        if estimate > 180.0 and parts == 1: # Certifica que o video terá pelo menos
            parts += 1                      # 2 partes, caso seja maior que 3 minutos
    
        # Prepara o texto para processamento, separando em segmentos de paragrafos
        if parts == 1:
            paragraphs.append(text)
        else:
            paragraphs = split_paragraphs(text, parts)

    
        # Prepara a narração
        print_msg(f'Video em 1 parte, gerando narração...' if len(paragraphs) == 1 else f'Video em {len(paragraphs)} partes, processando as partes')
        
        for i in range(0, len(paragraphs)):
            print_msg(f"Gerando áudio da parte {i + 1}")
            audio_part_name = f'__part_{i}__.mp3'
            narration_filename = os.path.join(audio_path, audio_part_name)
            text_to_speech(paragraphs[i], narration_filename, voice, "en-US", "mp3", engine='neural')
        
        # Baixar vídeo de gameplay do YouTube
        print_msg("Baixando o video de fundo")
        youtube_url = get_random_background_video()
        download_youtube_video(youtube_url, output_dir='tmp')
        
        # Carregar vídeo de gameplay
        gameplay_video = mp.VideoFileClip(os.path.join("tmp","__yt1__.mp4"))

        # Preparar diretório de saída do do vídeo pronto
        output_path = os.path.join('output', str(uuid.uuid4()))
        os.mkdir(output_path)

        # Criar videos prontos 
        for i in range(len(paragraphs)):
            audio_part_name = os.path.join(audio_path, f"__part_{i}__.mp3")
            narration_audio = mp.AudioFileClip(audio_part_name)
            print_msg(f'Video em 1 parte (tempo de {narration_audio.duration:.2f}s), processando...' if len(paragraphs) == 1 else f'Parte em {i + 1} processamento, tempo total {narration_audio.duration:.2f}s')
            
            # Certifique-se de que a mensagem é exibida corretamente
            sys.stdout.flush()
            
            video_with_audio = gameplay_video.set_audio(narration_audio) # Inclui o áudio no video de fundo
            print_msg("Formatando para o formato do tiktok") 
            sys.stdout.flush()
            formatted_video = format_video_to_9x16(video_with_audio) # Recorta o vídeo para o formato 9x16
            
            print_msg("Adicionando legendas ao video")
            sys.stdout.flush()
            subtitle_part_name = os.path.join(subtitle_path, f'__part_{i}.srt')
            generate_subtitles(audio_part_name, subtitle_part_name)

            # Cria a camada de legendas e caption da parte
            video_with_subtitles = add_subtitles_to_video(formatted_video, 
                                                        subtitle_part_name,
                                                        i + 1, 
                                                        len(paragraphs))

            generated_videos = []
            output_filename = os.path.join(output_path, f'output_part_{i+1}.mp4')
            print_msg(f"Exportando parte {i+1} com {narration_audio.duration:.2f}s")
            export_single(video_with_subtitles, 
                        narration_audio.duration, 
                        output_filename,
                        logger='bar')

        
        remove_tmp() # Remove arquivos temporários
        
        for filename in os.listdir(output_path):
            filepath = os.path.join(output_path,filename)
            print(f"Arquivo {filepath} gerado")
            generated_videos.append({'video': filepath}) # Gera referência do caminho do ultimo video gerado

        # Salvar os detalhes do vídeo no arquivo JSON
        video_data = {
            'title': selected_story['title'],
            'videos': generated_videos
        }
        save_to_json(video_data)

        with open(os.path.join(output_path,"fulltext.txt"), 'w') as fp:
            fp.write(text)
        
        notify() # Toca uma notificação ao fim do processamento da tarefa de geração atual

        sys.stdout.flush()
        input(term.bold("Pressione ENTER para continuar"))
        
        gc.collect()

if __name__ == '__main__':
    main()
