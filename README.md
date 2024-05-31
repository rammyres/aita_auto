# AITA Video Maker

Este é um script Python para criar vídeos automáticos com histórias do subreddit "Am I the Asshole?" (AITA) do Reddit.

  - A correção de texto é feita através do modelo BeRT. 

  - A geração de audio usa a AWS Polly.

  - As legendas são geradas através da Assembly.ai

Credenciais de acesso a esse serviços sáo necessárias (todos os serviços tem tiers gratuítos generosos)

## Funcionalidades

- Baixa vídeos do YouTube para serem usados como background.
- Gera narração automática a partir das histórias selecionadas.
- Formata os vídeos para o formato TikTok (9x16).
- Adiciona legendas e divide os vídeos em segmentos dependendo da duração estimada do texto
- Exporta os segmentos com legendas para TikTok.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - moviepy
  - praw (Python Reddit API Wrapper)
  - boto3
  - protobuf 
  - yt_dlp
  - opencv-python
  - wand
  - assemblyai
  - pydub
  - playsound
  - spacy
  - contextualSpellCheck

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/rammyres/aita_auto.git
   cd aita_auto
   ```

2. Instale os requisitos:
    ```sh
    pip install -r requirements.txt
    ```
3. Instale o modelo de correção de texto 
    ```sh
    python -m spacy download en_core_web_lg
    ```
4. Execute o script main:
    ```sh
    python main.py
    ```

Na primeira execução serão configuradas as credenciais Reddit, Assembly.ai e AWS