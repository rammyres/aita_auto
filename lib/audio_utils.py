import json, boto3, random, os
import moviepy.editor as mp

# Função para criar um segmento de áudio com silêncio
def get_random_voice(gender):
    with open("config/voices.json") as voices_file:
        voices = json.load(voices_file)

        if gender == "male" or gender == "males":
            male_voices = [voice["name"] for voice in voices["males"]]
            return random.choice(male_voices)
        if gender == "female" or gender == "females":
            female_voices = [voice["name"] for voice in voices["females"]]
            return random.choice(female_voices)

# Função para gerar narração de texto usando Amazon Polly
def text_to_speech(text, filename, voice, language_code, output_format='mp3', engine='standard'):
    polly = boto3.client('polly', region_name='us-west-2')
    
    if voice == 'ruth' or voice == 'matthew':
        engine = 'generative'

    # Quebrar o texto em partes de até 1500 caracteres (considerando o limite de Polly)
    chunks = [text[i:i+1500] for i in range(0, len(text), 1500)]
    # method='bilinear'
    # Gerar áudios para cada parte do texto
    audio_streams = []
    for i, chunk in enumerate(chunks):
        response = polly.synthesize_speech(
            Text=chunk,
            OutputFormat=output_format,
            SampleRate='24000',
            LanguageCode=language_code,
            VoiceId=voice,
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