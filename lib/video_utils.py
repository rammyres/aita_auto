import boto3
import moviepy.editor as mp
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
import os


# Função para gerar narração de texto usando Amazon Polly
def text_to_speech(text, filename, voice_id, language_code, output_format='mp3', engine='standard'):
    polly = boto3.client('polly', region_name='us-west-2')
    
    # Quebrar o texto em partes de até 1500 caracteres (considerando o limite de Polly)
    chunks = [text[i:i+1500] for i in range(0, len(text), 1500)]
    method='bilinear'
    # Gerar áudios para cada parte do texto
    audio_streams = []
    for i, chunk in enumerate(chunks):
        response = polly.synthesize_speech(
            Text=chunk,
            OutputFormat=output_format,
            LanguageCode=language_code,
            VoiceId=voice_id,
            Engine=engine,
            TextType='text'
        )
        
        # Salvar o áudio sintetizado temporariamente
        temp_filename = 'tmp/temp_chunk_{}.mp3'.format(i)
        with open(temp_filename, 'wb') as f:
            f.write(response['AudioStream'].read())
            print(f'Conteúdo de áudio para o segmento {i} escrito no arquivo "{temp_filename}"')
        
        # Adicionar o stream de áudio ao array
        audio_streams.append(mp.AudioFileClip(temp_filename))
        
        # Remover o arquivo temporário após adicionar ao array
        os.remove(temp_filename)
    
    # Combinar todos os áudios em um único arquivo
    final_audio = mp.concatenate_audioclips(audio_streams)
    final_audio.write_audiofile(filename)
    print(f'Narração salva em "{filename}"')

# # Função para adicionar texto ao vídeo
def add_subtitles_to_video(video, subtitles):
    # Função geradora para criar clipes de texto
    generator = lambda txt: mp.TextClip(txt,font='Metropolis-black', 
                                        fontsize=70, 
                                        color='white',
                                        stroke_color='black', 
                                        method='label')
    
    # Criar SubtitlesClip
    subs = SubtitlesClip(subtitles, generator)
    
    # Adicionar legendas ao vídeo
    video_with_subs = mp.CompositeVideoClip([video, subs.set_position(('center', 'center'))])
    
    return video_with_subs

# Função para dividir vídeo em segmentos de 1 minuto e 1 segundo

def split_video(video, total_duration, segment_duration):
    segments = []
    # total_duration = mp.AudioFileClip(narration).duration  # Duração total do vídeo
    
    # Verificar se segment_duration é maior que a duração do vídeo
    if segment_duration > total_duration:
        segment_duration = total_duration
    
    start_time = 0
    while start_time < total_duration:
        end_time = min(start_time + segment_duration, total_duration)
        segment = video.subclip(start_time, end_time)
        segments.append(segment)
        start_time = end_time
    
    return segments

def export_single(video, total_time, output_file):
    print("export_single")
    start_time = 0 
    # end_time = min(start_time, total_time)
    output = video.subclip(start_time, total_time)
    output.write_videofile(output_file, codec='libx264', fps=24)

def export_sync(video, total_time):
    print("export_sync")
    export_single(video, total_time, 'tmp/__sync__.mp4')

def export_segments(segments):
    for j, segment in enumerate(segments):
        output_filename = f"output/output_segment_{j}.mp4"
        segment.write_videofile(output_filename, codec='libx264', fps=24)
        print(f"Parte {j} salva como {output_filename}")

# Função para formatar vídeo para 9x16
# def format_video_to_9x16(video):
#     video.write_videofile('tmp/__sync__.mp4', codec='libx264', fps=24)
#     return video.resize(height=1920).resize(width=1080)
def format_video_to_9x16(video, duration):

    (w, h) = video.size

    crop_width = h * 9/16
    # x1,y1 is the top left corner, and x2, y2 is the lower right corner of the cropped area.

    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h
    cropped_clip = crop(video, x1=x1, y1=y1, x2=x2, y2=y2)

    # cropped_clip.write_videofile('tmp/__sync__.mp4', codec='libx264', fps=24)
    export_sync(cropped_clip, duration)
    
    return cropped_clip.resize(height=1920).resize(width=1080)

# Função para remover arquivo de áudio temporário
def remove_temp_audio(filename):
    os.remove(filename)
