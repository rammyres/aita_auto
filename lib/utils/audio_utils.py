import json, boto3, random, os
import moviepy.editor as mp
from playsound import playsound
from lxml import etree
from lib.utils.reddit_utils import convert_to_ssml

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

def split_text_into_chunks(text, max_chars):
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_chars:  # +1 for space
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

# def convert_to_ssml(text):
#     # Função simples para converter texto em SSML
#     return f'<speak>{text}</speak>'

def validate_ssml(ssml_text):
    try:
        etree.fromstring(ssml_text)
        return True
    except etree.XMLSyntaxError as e:
        print(f"Erro de validação SSML: {e}")
        return False

def text_to_speech(text, filename, voice, language_code, output_format='mp3', engine='standard'):
    polly = boto3.client('polly', region_name='us-west-2')
    silence_seg = mp.AudioFileClip('assets/audio/silence.mp3')  # 1s de silêncio ao final de cada parte
    
    if voice == 'ruth' or voice == 'matthew':
        engine = 'generative'

    # Quebrar o texto em partes de até 1500 caracteres
    chunks = split_text_into_chunks(text, 1500)
    
    # Gerar áudios para cada parte do texto
    audio_streams = []
    for i, chunk in enumerate(chunks):
        ssml_chunk = convert_to_ssml(chunk)
        if not validate_ssml(ssml_chunk):
            raise ValueError(f"SSML inválido para o segmento {i}: {ssml_chunk}")

        response = polly.synthesize_speech(
            Text=ssml_chunk,
            OutputFormat=output_format,
            SampleRate='24000',
            LanguageCode=language_code,
            VoiceId=voice,
            Engine=engine,
            TextType='ssml'
        )
        
        # Salvar o áudio sintetizado temporariamente
        temp_filename = f'tmp/temp_chunk_{i}.mp3'
        with open(temp_filename, 'wb') as f:
            f.write(response['AudioStream'].read())
            print(f'Conteúdo de áudio para o segmento {i} escrito no arquivo "{temp_filename}"')
        
        # Adicionar o stream de áudio ao array
        audio_streams.append(mp.AudioFileClip(temp_filename))
        audio_streams.append(silence_seg)
    
        # Remover o arquivo temporário após adicionar ao array
        os.remove(temp_filename)
    
    # Combinar todos os áudios em um único arquivo
    final_audio = mp.concatenate_audioclips(audio_streams)
    
    final_audio.write_audiofile(filename)
    print(f'Narração salva em "{filename}"')

def notify():
    playsound('assets/audio/notification.mp3')
