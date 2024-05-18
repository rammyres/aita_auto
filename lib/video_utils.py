import boto3
import moviepy.editor as mp
import os

# Função para gerar narração de texto usando Amazon Polly
def text_to_speech(text, filename='speech.mp3', voice_id='Joanna', language_code='en-US', output_format='mp3'):
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
            VoiceId=voice_id,
            TextType='text'
        )
        
        # Salvar o áudio sintetizado temporariamente
        temp_filename = f'temp_chunk_{i}.mp3'
        with open(temp_filename, 'wb') as f:
            f.write(response['AudioStream'].read())
            print(f'Audio content for chunk {i} written to file "{temp_filename}"')
        
        # Adicionar o stream de áudio ao array
        audio_streams.append(mp.AudioFileClip(temp_filename))
        
        # Remover o arquivo temporário após adicionar ao array
        os.remove(temp_filename)
    
    # Combinar todos os áudios em um único arquivo
    final_audio = mp.concatenate_audioclips(audio_streams)
    final_audio.write_audiofile(filename)
    print(f'Narração salva em "{filename}"')

# Função para adicionar texto ao vídeo
def add_text_to_video(video, text, start_time, duration, position='center'):
    txt_clip = mp.TextClip(text, fontsize=24, color='white')
    txt_clip = txt_clip.set_position(position).set_duration(duration).set_start(start_time)
    return mp.CompositeVideoClip([video, txt_clip])

# Função para dividir vídeo em segmentos de 1 minuto e 1 segundo
def split_video(video, narration, segment_duration):
    
    segments = []
    current_duration = mp.AudioFileClip(narration).duration
    
    # Verificar se segment_duration é maior que a duração do vídeo
    if segment_duration > current_duration:
        segment_duration = current_duration
    
    while current_duration > 0:
        if current_duration > segment_duration:
            start_time = current_duration - segment_duration
        else:
            start_time = 0
        
        end_time = current_duration
        segment = video.subclip(start_time, end_time)
        segments.append(segment)
        current_duration -= segment_duration
    
    return segments


def export_segments(segments):
    for j, segment in enumerate(segments):
        output_filename = f"output_segment_{j}.mp4"
        segment.write_videofile(output_filename, codec='libx264', fps=24)
        print(f"Parte {j} salva como {output_filename}")

# Função para formatar vídeo para 9x16
def format_video_to_9x16(video):
    return video.resize(height=1920).resize(width=1080)

# Função para remover arquivo de áudio temporário
def remove_temp_audio(filename):
    os.remove(filename)
