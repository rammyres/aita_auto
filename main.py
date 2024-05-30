from lib.reddit_utils import *
from lib.youtube_utils import *
from lib.video_utils import *
from lib.subtitles_utils import *
from lib.file_utils import *
from lib.audio_utils import *
from lib.interface_utils import *
import moviepy.editor as mp
import uuid, gc

# Função principal
def main():
    # Verifica se os arquivos de configuração estão disponíveis e os cria se não estiverem
    # Os arquivos criados são para os serviços aws, aai e reddit
    check_configs()

    while True:
        selected_story = select_story()
        if not selected_story:
            return

        # Cria as pastas temporárias e de saída somente após a escolha da história
        subtitle_path = 'tmp/subtitles'
        audio_path = 'tmp/audio'
        mk_dirs()

        # Escolhe o sexo do narrador
        voice = get_random_voice(set_gender())
        print_msg(f"Voz escolhida: {voice}")
        
        # Baixar vídeo de gameplay do YouTube
        print_msg("Baixando o video de fundo")
        youtube_url = get_random_background_video()
        download_youtube_video(youtube_url, output_dir='tmp')

        # Gerar narração
        print_msg("Preparando narração, aguarde...")

        unclean_text = selected_story['title'] + ". " + selected_story['text']
        text = replace_profanities(unclean_text)

        paragraphs = []
        estimate = estimate_time(text)

        print_msg(f"Estimativa de tempo {estimate}")

        if estimate<180.0:
            paragraphs.append(text)
        else:
            parts = 2 if int(estimate//180) == 1 else int(estimate//180)
            paragraphs = split_paragraphs(text, parts)

        print_msg(f'Video em 1 parte, gerando narração...' if len(paragraphs) == 1 else f'Video em {len(paragraphs)} partes, processando as partes')

        for i in range(0, len(paragraphs)):
            print_msg(f"Gerando áudio da parte {i+1}")
            narration_filename = f"{audio_path}/__part_{i}__.mp3"
            text_to_speech(paragraphs[i], narration_filename, voice, "en-US", "mp3", engine='neural')
        
        # Carregar vídeo de gameplay
        gameplay_video = mp.VideoFileClip("tmp/__yt1__.mp4")

        print_msg(f'Video em 1 parte (tempo estimado de {estimate}s), processando...' if len(paragraphs) == 1 else f'Video em {len(paragraphs)} partes, processando as partes')

        # Preparar diretório de saída do do vídeo pronto
        output_path = f'output/{uuid.uuid4()}'
        os.mkdir(output_path)

        # Criar videos prontos 
        for i in range(len(paragraphs)):
            # Cria o clipe de narração para inclusão do video a partir do audio gerado pela Polly
            narration_audio = mp.AudioFileClip(f"{audio_path}/__part_{i}__.mp3") 
            video_with_audio = gameplay_video.set_audio(narration_audio) # Inclui o áudio no video de fundo
            print_msg("Formatando para o formato do tiktok") 
            formatted_video = format_video_to_9x16(video_with_audio) # Recorta o vídeo para o formato 9x16
            print_msg("Adicionando legendas ao video")
            
            # Gera as legendas a partir do áudio de cada uma as partes
            generate_subtitles(f'{audio_path}/__part_{i}__.mp3', f'{subtitle_path}/__part_{i}.srt')

            # Cria a camada de legendas e caption de parte
            video_with_subtitles = add_subtitles_to_video(formatted_video, 
                                                        f'{subtitle_path}/__part_{i}.srt', 
                                                        i+1, 
                                                        len(paragraphs))
            
            # Exporta o video pronto
            export_single(video_with_subtitles, 
                        narration_audio.duration, 
                        f'{output_path}/output_part_{i+1}.mp4')
            
        
        remove_tmp() # Remove arquivos temporários
        
        for filename in os.listdir(output_path):
            print(f"Arquivo {output_path}/{filename} gerado")

        input("Pressione ENTER para continuar")

if __name__ == '__main__':
    main()
