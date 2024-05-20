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

def split_video(video, narration, segment_duration):
    segments = []
    total_duration = mp.AudioFileClip(narration).duration  # Duração total do vídeo
    
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

def export_segments(segments):
    for j, segment in enumerate(segments):
        output_filename = f"output/output_segment_{j}.mp4"
        segment.write_videofile(output_filename, codec='libx264', fps=24)
        print(f"Parte {j} salva como {output_filename}")

# Função para formatar vídeo para 9x16
# def format_video_to_9x16(video):
#     video.write_videofile('tmp/__sync__.mp4', codec='libx264', fps=24)
#     return video.resize(height=1920).resize(width=1080)
def format_video_to_9x16(video):
    """
    Formata o vídeo para 9x16 cortando a área central do vídeo original.
    
    Args:
    video (VideoClip): O clipe de vídeo original.
    
    Returns:
    VideoClip: O clipe de vídeo formatado para 9x16.
    """
    # Calcular a nova largura e altura mantendo a proporção 9x16
    width, height = video.size
    new_height = 1920
    new_width = 1080
    
    if width > new_width:
        # Recortar a área central do vídeo para se ajustar ao novo tamanho
        x_center = width // 2
        x1 = x_center - (new_width // 2)
        x2 = x_center + (new_width // 2)
        video = crop(video, x1=x1, x2=x2)
    else:
        # Caso o vídeo seja mais estreito que o novo tamanho, apenas redimensione
        video = video.resize(height=new_height)
    
    video.write_videofile('tmp/__sync__.mp4', codec='libx264', fps=24)
    
    return video.resize(height=new_height)

# Função para remover arquivo de áudio temporário
def remove_temp_audio(filename):
    os.remove(filename)
