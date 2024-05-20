import os 

# Remove arquivos temporários
def remove_tmp():
    for filename in os.listdir('tmp'):
        if filename.endswith(".mp4") or filename.endswith(".mp3") or filename.endswith(".srt"):
            filepath = os.path.join('tmp', filename)
            os.remove(filepath)
    os.rmdir('tmp')
    print("Arquivos temporários removidos")