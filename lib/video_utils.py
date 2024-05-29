import moviepy.editor as mp
from moviepy.video.fx.all import crop
from moviepy.video.tools.subtitles import SubtitlesClip
import os

# Função para adicionar texto ao vídeo
def add_subtitles_to_video(video, subtitles, part, total_parts):
    # Função geradora para criar clipes de texto
    generator = lambda txt: mp.TextClip(txt,font='Metropolis-black', 
                                        fontsize=90, 
                                        color='yellow',
                                        stroke_color='black', 
                                        method='label')
    subs = SubtitlesClip(subtitles, generator)
    # Adicionar legendas ao vídeo
    video_with_subs = mp.CompositeVideoClip([video, subs.set_position(('center', 'center'))])

    
    part_label = mp.TextClip("Complete story" if total_parts==1 else f'Part {part}/{total_parts}',
                             font='Metropolis-black', 
                             fontsize=70, 
                             color='yellow',
                             stroke_color='black', 
                             method='label')
    part_label.set_duration(video.duration)
    video_with_subs_and_parts = mp.CompositeVideoClip([video_with_subs, part_label.set_position(('center', 'bottom'))])
    video_with_subs_and_parts = video_with_subs_and_parts.set_duration(video_with_subs_and_parts.duration)

    return video_with_subs_and_parts

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
    start_time = 0 
    output = video.subclip(start_time, total_time)
    output.write_videofile(output_file, codec='libx264', fps=24)

def export_sync(video, total_time):
    export_single(video, total_time, 'tmp/__sync__.mp4')

def export_segments(segments, output_path):
    for j, segment in enumerate(segments):
        part_label = mp.TextClip(f"Part {j+1}/2",font='Metropolis-black', 
                                        fontsize=70, 
                                        color='yellow',
                                        stroke_color='black', 
                                        method='label')
        part_label.set_duration(segment.duration)
        _segment = mp.CompositeVideoClip([segment, part_label.set_position(('center', 'bottom'))])
        output_filename = f"{output_path}/output_segment_{j}.mp4"
        _segment = _segment.set_duration(segment.duration)
        _segment.write_videofile(output_filename, codec='libx264', fps=24)
        print(f"Parte {j} salva como {output_filename}")

# Função para formatar vídeo para 9x16
def format_video_to_9x16(video):
    (w, h) = video.size
    crop_width = h * 9/16
    x1, x2 = (w - crop_width)//2, (w+crop_width)//2
    y1, y2 = 0, h
    cropped_clip = crop(video, x1=x1, y1=y1, x2=x2, y2=y2)
    
    return cropped_clip.resize(height=1920).resize(width=1080)

# Função para remover arquivo de áudio temporário
def remove_temp_audio(filename):
    os.remove(filename)
