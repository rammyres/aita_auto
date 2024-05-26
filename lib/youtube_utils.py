import os, yt_dlp, json, random
from pytube import YouTube

def rename(directory, new_name):
    # Verifica se o diretório existe
    if not os.path.isdir(directory):
        print(f'Diretório "{directory}" não encontrado.')
        return
    
    # Lista todos os arquivos no diretório
    files = os.listdir(directory)
    
    # Encontra o primeiro arquivo (ignorando subdiretórios)
    for file in files:
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path):
            # Renomeia o primeiro arquivo encontrado
            os.rename(file_path, os.path.join(directory, new_name))
            print(f'Arquivo renomeado para "{new_name}".')
            return
    
    print('Nenhum arquivo encontrado para renomear.')

def get_random_background_video():
    with open("config/videos.json") as voices_file:
        videos = json.load(voices_file)
        video = random.choice(videos['videos'])
        return video['video']


# def download_youtube_video(url, sequence_number=1, output_dir='downloads'):
#     # Limpa o diretório de downloads se já existir
#     if os.path.exists(output_dir):
#         files = os.listdir(output_dir)
#         for file in files:
#             os.remove(os.path.join(output_dir, file))
#     else:
#         os.makedirs(output_dir)

#     yt = YouTube(url)
#     stream = yt.streams.filter(file_extension='mp4').get_highest_resolution()
#     # filename = f'yt{sequence_number}.mp4'  # Nome do arquivo usando um número sequencial
#     # output_path = os.path.join(output_dir, filename)
#     stream.download(output_path=output_dir)

#     rename(output_dir, "__yt1__.mp4")

#     return output_dir

def download_youtube_video(youtube_url, output_dir='tmp'):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',
        'outtmpl': f'{output_dir}/__yt1__.mp4',
        'merge_output_format': 'mp4'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # for file in os.listdir(output_dir):
    #     if file.startswith('__yt1__') and not file.endswith('.mp4'):
    #         old_path = os.path.join(output_dir, file)
    #         new_path = os.path.join(output_dir, '__yt1__.mp4')
    #         os.rename(old_path, new_path)
    #         break

