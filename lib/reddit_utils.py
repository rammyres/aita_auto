import praw, json, re, random, nltk
from lib.config_utils import *
from tqdm import tqdm
from mysutils.text import remove_urls
from nltk.tokenize import word_tokenize, sent_tokenize
# import spacy, contextualSpellCheck

# Estima o tempo da narração
def estimate_time(text):
    return (len(text.split())/150)*60

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

def get_random_stories(sub_name = 'amitheasshole', num_posts=10):
    
    # Buscar as 500 postagens mais populares do subreddit AITA
    subreddit = reddit.subreddit(sub_name)
    top_posts = subreddit.top(limit=500)  # Limitar à 500 postagens mais populares
    
    # Selecionar aleatoriamente 'num_posts' postagens
    selected_posts = random.sample(list(top_posts), num_posts)
    
    # Extrair informações de título e URL para cada post selecionado
    stories = []
    for post in selected_posts:
        story = {
            'title': post.title,
            'url': post.url,
            'text': post.selftext
        }
        stories.append(story)
    
    return stories

def get_random_recent_stories(sub_name = 'amitheasshole', num_posts=10):
    
    # Buscar as 500 postagens mais populares do subreddit AITA
    subreddit = reddit.subreddit(sub_name)
    top_posts = subreddit.top(limit=100, time_filter = 'week')  # Limitar à 500 postagens mais populares
    
    # Selecionar aleatoriamente 'num_posts' postagens
    selected_posts = random.sample(list(top_posts), num_posts)
    
    # Extrair informações de título e URL para cada post selecionado
    stories = []
    for post in selected_posts:
        story = {
            'title': post.title,
            'url': post.url,
            'text': post.selftext
        }
        stories.append(story)
    
    return stories

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

    return text