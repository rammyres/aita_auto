import srt

def generate_subtitles(text, narration_duration, max_chars_per_subtitle=40):
    subtitles = []
    words = text.split()
    current_subtitle = ""
    start_time = 0
    duration_per_subtitle = narration_duration / (len(text) / max_chars_per_subtitle)
    index = 1  # Inicializa o índice das legendas
    
    for word in words:
        if len(current_subtitle) + len(word) + 1 <= max_chars_per_subtitle:
            if current_subtitle:
                current_subtitle += " "
            current_subtitle += word
        else:
            subtitle = srt.Subtitle(
                index=index,
                start=srt.timedelta(seconds=start_time),
                end=srt.timedelta(seconds=start_time + duration_per_subtitle),
                content=current_subtitle
            )
            subtitles.append(subtitle)
            start_time += duration_per_subtitle
            current_subtitle = word
            index += 1
    
    # Adiciona a última legenda, se houver
    if current_subtitle:
        subtitle = srt.Subtitle(
            index=index,
            start=srt.timedelta(seconds=start_time),
            end=srt.timedelta(seconds=start_time + duration_per_subtitle),
            content=current_subtitle
        )
        subtitles.append(subtitle)
    
    sub_srt = srt.compose(subtitles)

    with open("tmp/subtitles.srt", 'w+') as file:
        file.write(sub_srt) 
    # return subtitles

