import os 
from lib.interface_utils import *

# Remove arquivos temporários
def remove_tmp():
    for filename in os.listdir('tmp/audio'):
        
        filepath = os.path.join('tmp/audio', filename)
        os.remove(filepath)
    os.rmdir('tmp/audio')
    
    for filename in os.listdir('tmp/subtitles'):
        if filename.endswith(".srt"):
            filepath = os.path.join('tmp/subtitles', filename)
            os.remove(filepath)
    os.rmdir('tmp/subtitles')

    for filename in os.listdir('tmp'):
        if any(
            (filename.endswith(".mp4"), 
               filename.endswith(".mp3"), 
               filename.endswith(".srt"), 
               filename.endswith(".part"),
               filename.endswith(".ytdl")
               )
            ):
        # if filename.endswith(".mp4") or filename.endswith(".mp3") or filename.endswith(".srt") or filename.endswith(".part"):
            filepath = os.path.join('tmp', filename)
            os.remove(filepath)
    os.rmdir('tmp')
    print_msg("Arquivos temporários removidos")

def mk_dirs():
    # Verifica se o diretório temporário existe
    if not os.path.exists('tmp'):
        os.mkdir('tmp')

# Verifica se o diretório de saida existe
    if not os.path.exists('output'):
        os.mkdir('output')
    
# verifica se o diretório de audios existe
    if not os.path.exists("tmp/audio"):
        os.mkdir('tmp/audio')
    
# verificar se o diretório de legendas existe
    if not os.path.exists("tmp/subtitles"):
        os.mkdir('tmp/subtitles')