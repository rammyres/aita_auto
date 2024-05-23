import os 

# Remove arquivos temporários
def remove_tmp():
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
    print("Arquivos temporários removidos")