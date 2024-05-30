# import srt, os

import time
import assemblyai as aai
from lib.interface_utils import *
from lib.config_utils import return_aai_key

def generate_subtitles(narration_file, output_file):
    config = aai.TranscriptionConfig(speech_model=aai.SpeechModel.best)
    aai.settings.api_key = return_aai_key()
    transcriber = aai.Transcriber(config=config)

    print_msg("Iniciando transcrição...")
    transcript = transcriber.transcribe(narration_file)
    
    # Verifica o status do job até que esteja completo
    while transcript.status not in ['completed', 'failed']:
        transcript = transcriber.get_transcript(transcript.id)
        if transcript.status == 'completed':
            break
        elif transcript.status == 'failed':
            raise Exception("Transcription failed")
        print("Not ready yet...")
        time.sleep(10)

    srt_response = transcript.export_subtitles_srt(chars_per_caption=20)
    with open(output_file, 'w') as file:
        file.write(srt_response)
    print("Legendas baixadas!")