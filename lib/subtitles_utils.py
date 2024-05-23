# import srt, os

import os, configparser, time
import assemblyai as aai

def return_aai_key():
    config_file = os.path.join(os.path.dirname(__file__),'..','config', 'aai.ini')
    aai_config = configparser.ConfigParser()
    aai_config.read(config_file)
    return aai_config.get('aai_settings','key')

def generate_subtitles():
    aai.settings.api_key = return_aai_key()
    transcriber = aai.Transcriber()

    print("Iniciando transcrição...")
    transcript = transcriber.transcribe('tmp/__narration__.mp3')
    
    # Verifica o status do job até que esteja completo
    while transcript.status not in ['completed', 'failed']:
        transcript = transcriber.get_transcript(transcript.id)
        if transcript.status == 'completed':
            break
        elif transcript.status == 'failed':
            raise Exception("Transcription failed")
        print("Not ready yet...")
        time.sleep(10)

    srt_response = transcript.export_subtitles_srt(chars_per_caption=24)
    with open("tmp/__subtitles__.srt", 'w') as file:
        file.write(srt_response)
    print("Legendas baixadas!")