# AITA Video Maker

Este é um script Python para criar vídeos automáticos com histórias de vários subreddits (incluindo "Am I the Asshole?" (AITA)) do Reddit.

  - A geração de audio usa a AWS Polly.

  - As legendas são geradas através da Assembly.ai

  - Não há correção de texto por padrão, mas alguns erros na geração do texto provocadas pela PRAW são minimizadas através de NLTK

  - Também é possível editar o texto antes da geração da narração em modo gráfico (veja a sessão GUI abaixo)

Credenciais de acesso (API keys) a AWS, Assembly.ai e Reddit sáo necessárias (todos os serviços tem tiers gratuítos generosos)

## Novidades

Agora o Aita VideoMaker conta com uma interface gráfica feita

## Funcionalidades

- Baixa vídeos do YouTube para serem usados como background.
- Gera narração automática a partir das histórias selecionadas.
- Formata os vídeos para o formato TikTok (9x16).
- Adiciona legendas e divide os vídeos em segmentos dependendo da duração estimada do texto
- Exporta os segmentos com legendas para TikTok.

## Requisitos

- Python 3.x
- Bibliotecas Python:
  - assemblyai
  - blessed
  - boto3
  - flet
  - lxml
  - moviepy
  - mysmallutils
  - nltk
  - playsound
  - praw
  - tqdm
  - yt_dlp


## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/rammyres/aita_auto.git
   cd aita_auto
   ```

2. Instale os requisitos:
    ```bash
    pip install -r requirements.txt
    ```
3. Instale o ffmpeg e o Image Magick (de acordo com sua distribuição)
    - Debian/Ubuntu 
    ```
    sudo apt install ffmpeg imagemagick
    ```

    - CentOS/RedHat
    ```
    sudo yum install ffmpeg ffmpeg-devel ImageMagick ImageMagick-devel

    ```

    - Arch Linux
    ```
    sudo pacman -S ffmpeg imagemagick
    ```

    - OpenSUSE
    ```
    sudo zypper install ffmpeg-4 ImageMagick
    ```

    - Gentoo
    ```
    sudo emerge --ask media-video/ffmpeg 
    sudo emerge --ask media-gfx/imagemagick
    ```

4. Execute o script main:
    ```sh
    python main.py
    ```

Na primeira execução serão configuradas as credenciais Reddit, Assembly.ai e AWS

## Outras configurações
O script possui listas de palavrões (config/profanities.json) e siglas (config/acronyms.json) que podem ser ajustadas para correção automática do texto. 

Há também uma lista de videos do youtube (config/videos.json) para plano de fundo (sem copyright ou comentários, com tempo minimo de 3 minutos), que também pode ser ajustada de acordo com a necessidade.

As vozes em config/voices.json são uma questão pessoal, mas todas as vozes disponíveis podem ser utilizadas. 

## GUI 

A interface gráfica pode ser acessada usando o seguinte script:
    ```bash
    python gui.py
    ```

Todas as funções da versão em modo texto estão disponíveis, incluindo funcionalidades novas como:
  - Edição do texto da postagem antes da geração da narração
  - Edição das configurações
  - Prévia dos videos gerados 
  - Cópia do caminho dos videos gerados a partir da lista de videos disponíveis

  ## Screenshots
  <img src="https://github.com/rammyres/aita_auto/assets/17151666/b71370e3-ab51-4c96-9b3e-281e73bbfb6b" width="23%"></img> <img src="https://github.com/rammyres/aita_auto/assets/17151666/8f609d4f-2c19-4d78-b9b1-2cfabdda6dd0" width="23%"></img> <img src="https://github.com/rammyres/aita_auto/assets/17151666/1566d7fa-ffa3-47d1-bf55-695d49c32c44" width="23%"></img> <img src="https://github.com/rammyres/aita_auto/assets/17151666/06a556a3-5d17-4b58-93a5-3c1e0bdcb691" width="23%"></img> <img src="https://github.com/rammyres/aita_auto/assets/17151666/32cb7df5-f90f-486f-820a-59dec203f7c5" width="23%"></img> <img src="https://github.com/rammyres/aita_auto/assets/17151666/c9b77c45-07a8-4266-bdf7-5f239182dbdd" width="23%"></img> <img src="https://github.com/rammyres/aita_auto/assets/17151666/1c07fe74-a4cb-4787-b456-ee51c312686d" width="23%"></img> <img src="https://github.com/rammyres/aita_auto/assets/17151666/3c7e2cf7-db4f-4b75-a501-ee451179b3e9" width="23%"></img> 

