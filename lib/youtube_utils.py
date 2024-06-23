import os, yt_dlp, json, random

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

def download_youtube_video(youtube_url, output_dir='tmp'):
    try:
        ydl_opts = {
            # 'format': 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]',
            'format': 'bestvideo[ext=mp4][height<=2160]+bestaudio[ext=m4a]/best[ext=mp4][height<=2160]',
            'outtmpl': f'{output_dir}/__yt1__.mp4',
            'merge_output_format': 'mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except yt_dlp.utils.DownloadError:
        print("O ffmpeg não está instalado! Instale conforme sua distribuição")

