import praw, json, re, random, nltk
from lib.config_utils import *
from tqdm import tqdm
from mysutils.text import remove_urls
from nltk.tokenize import word_tokenize, sent_tokenize
import pysbd
import spacy, contextualSpellCheck

# Estima o tempo da narração
def estimate_time(text):
    return (len(text.split())/180)*60

def merge_accidental_splits(text):
    common_combinations = []
    with open('config/common_combinations.json') as f:
        common_combinations = json.load(f)['combinations']
    
    words = word_tokenize(text)
    corrected_words = []
    skip_next = False

    for i in range(len(words) - 1):
        if skip_next:
            skip_next = False
            continue
        
        # Verificar se a combinação está na lista de combinações comuns
        combined_phrase = words[i] + ' ' + words[i + 1]
        if combined_phrase in common_combinations:
            corrected_words.append(words[i])
        else:
            # Unir palavras separadas acidentalmente
            combined_word = words[i] + words[i + 1]
            if combined_word.lower() in nltk.corpus.words.words():
                corrected_words.append(combined_word)
                skip_next = True
            else:
                corrected_words.append(words[i])
    
    if not skip_next:
        corrected_words.append(words[-1])
    
    return ' '.join(corrected_words)


# Divide o tempo em segmentos para narração
def split_paragraphs(text, number_of_parts):
    nltk.download('punkt')
    # Verifica se o texto contém o divisor '* *'
    if '* *' in text:
        paragraphs = text.split('* *')  # Divide o texto em parágrafos
    else:
        # Se não há divisores '* *', divide o texto em frases
        sentences = sent_tokenize(text)
        total_sentences = len(sentences)
        sentences_per_part = max(1, total_sentences // number_of_parts)
        split_parts = [sentences[i:i + sentences_per_part] for i in range(0, total_sentences, sentences_per_part)]

        # Garante que split_parts não tenha mais partes do que number_of_parts
        while len(split_parts) > number_of_parts:
            last_part = split_parts.pop()
            split_parts[-1].extend(last_part)
        
        # Transforma as listas de partes em partes de texto
        paragraph_parts = [' '.join(part) for part in split_parts]
        return paragraph_parts

    # Ajusta o número de partes de acordo com a estimativa
    num_paragraphs_per_part = max(1, len(paragraphs) // number_of_parts)
    split_parts = [paragraphs[i:i + num_paragraphs_per_part] for i in range(0, len(paragraphs), num_paragraphs_per_part)]

    # Garante que split_parts não tenha mais partes do que number_of_parts
    while len(split_parts) > number_of_parts:
        last_part = split_parts.pop()
        split_parts[-1].extend(last_part)
    
    # Transforma as listas de partes em partes de texto
    paragraph_parts = [' '.join(part) for part in split_parts]

    return paragraph_parts

# Configuração do Reddit
reddit_config = load_reddit_config()
reddit = praw.Reddit(   
    client_id=reddit_config['client_id'],
    client_secret=reddit_config['client_secret'],
    user_agent=reddit_config['user_agent']
)


# Função para buscar histórias populares no subreddit AITA
def get_popular_stories(sub_name='amitheasshole', limit=10):
    subreddit = reddit.subreddit(sub_name)
    top_posts = subreddit.top(limit=limit)
    stories = []
    for post in top_posts:
        stories.append({'title': post.title, 'text': post.selftext, 'url': post.url})
    return stories

def get_story_from_url(url):
    submission = reddit.submission(url=url)
    
    # Extrair informações relevantes do post
    story = {
        'title': submission.title,
        'text': submission.selftext,
        'url': submission.url
    }
    
    return story


# Função para buscar histórias populares de acordo com os parametros
def get_stories(sub_name='amitheasshole', sample_size=None, return_limit=10, time_limit=None):
    """
    Retorna stories de acordo com os parametros

    sub_name indica o subreddit de onde retirar a amostragem (padrão amitheasshole)

    sample_size indica quantos posts devem ser puxados pela API para sorteio

    return_limit indica quatas historias devem ser retornadas do sample
    
    time_limit indica o periodo de tempo de busca as postagens mais comentadas
    
    get_stories() retorna as 10 postagens mais populares do amitheasshole
    
    get_stories(sub_name='trueoffmychest') retorna as 10 postagens mais populares de TrueOffMyChest

    get_stories(sub_name='trueoffmychest', sample_size = 500, time_limit = 'week') retorna 10 entre 
    as 500 histórias mais populares do subreddit trueoffmychest da ultima semana
    """
    subreddit = reddit.subreddit(sub_name)
    posts = []
    if time_limit and sample_size:
        _posts = subreddit.top(limit=sample_size, time_filter=time_limit)
        posts = random.sample(list(_posts), return_limit)
    
    if time_limit and not sample_size: 
        _posts = subreddit.top(limit=10, time_filter=time_limit)
        posts = random.sample(list(_posts), return_limit)
    
    if not time_limit and sample_size:
        _posts = subreddit.top(limit=sample_size)
        posts = random.sample(list(_posts), return_limit)
    
    if not time_limit and not sample_size: 
        posts = subreddit.top(limit=10)
    
    stories = []
    
    for post in posts:
        stories.append({'title': post.title, 'text': post.selftext, 'url': post.url})
    
    return stories

def get_story_from_url(url):
    submission = reddit.submission(url=url)
    
    # Extrair informações relevantes do post
    story = {
        'title': submission.title,
        'text': submission.selftext,
        'url': submission.url
    }
    
    return story

# Usa IA para separar as sentenças
def split_sentences(text):
    seg = pysbd.Segmenter(language='en', clean=False)
    return seg.segment(text)

# Usa IA para fazer a verificação de texto 
def spellCheck(text):

    # phrases = nltk.sent_tokenize(text)
    phrases = split_sentences(text)
    nlp = spacy.load('en_core_web_lg')
    contextualSpellCheck.add_to_pipe(nlp)
    
    for i, phrase in enumerate(phrases):
        doc = nlp(phrase)
        print(f'{i+1} - {phrase}')
        if doc._.performed_spellCheck:
            phrases[i] = doc._.outcome_spellCheck
            print(f'{i+1} - Corrected - {phrases[i]}')
    
    return ' '.join(phrases)

def convert_to_ssml(text):
    """
    Converte um texto longo para SSML.

    Args:
    text (str): O texto a ser convertido.

    Returns:
    str: O texto formatado em SSML.
    """
    # Adiciona a tag SSML de abertura
    ssml_text = "<speak>"

    # Divide o texto em sentenças para adicionar pausas
    sentences = text.split('.')
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            # Adiciona a sentença e uma pausa após ela
            ssml_text += f"{sentence}. <break time='100ms'/> "

    # Adiciona a tag SSML de fechamento
    ssml_text += "</speak>"

    return ssml_text

def prepare_text(text):
    print("Removendo tags")
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    
    print("Ajustando contrações comuns")
    # List of common contractions
    contractions = dict()
    with open('config/contractions.json') as f:
        contractions = json.load(f)
    
    # Repair contractions
    for contraction, replacement in tqdm(contractions.items()):
        text = re.sub(re.escape(contraction), replacement, text)

    
    print("Removendo espaços em palavras")
    # Remove unwanted single character spaces (e.g., "e xample" -> "example")
    text = re.sub(r'(\b\w) (\w\b)', r'\1\2', text)
    
    print("Quebrando texto unido por engano")
    # Insert a space between joined words (e.g., "exampleanother" -> "example another")
    text = re.sub(r'(\w)([A-Z][a-z])', r'\1 \2', text)

    print("Removendo texto invisível")
    # Remove #x200b do texto 
    text = re.sub(r'&\s*#\s*x200B', '', text)
    text = re.sub(r'\s*x200B', '', text)
    text = text.replace('\u200b', '').replace('#x200b', '')

    print("Trocando siglas pelos seus significados")
    # Troca siglas pelos seus significados
    acronyms_dict = dict()
    with open('config/acronyms.json', 'r') as file:
        acronyms_dict = json.load(file)

    for k, v in tqdm(acronyms_dict.items()):
        text = re.sub(rf'\b{k}\b', v, text)

    print("Removendo palavrões")
    # Remove palavrões e troca por eufemismos
    profanities = dict()
    with open('config/profanities.json') as f:
        profanities = json.load(f)
    
    for profanity, replacement in tqdm(profanities.items()):
        text = re.sub(r'\b' + re.escape(profanity) + r'\b', replacement, text, flags=re.IGNORECASE)

    print("Unindo textos indevidamente quebrados pelos processos anteriores")
    # List of common combiantions
    common_combinations = dict()
    with open('config/common_combinations.json') as f:
        common_combinations = json.load(f)
    
    # Repair common combinations
    for combination, replacement in tqdm(common_combinations.items()):
        text = re.sub(re.escape(combination), replacement, text)

    print("Removendo URLs")
    remove_urls(text)

    # print("Correção de texto por IA")
    # text = spellCheck(text)
    # input()
    
    return text


