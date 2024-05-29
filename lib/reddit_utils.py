import praw, json, re
from lib.config_utils import *
from nltk.tokenize import word_tokenize

# Estima o tempo da narração
def estimate_time(text):
    return (len(text.split())/150)*60

# Divide o tempo em segmentos para narração
def split_paragraphs(text, number_of_parts):
    if number_of_parts == 1:
        number_of_parts+=1

    # Verifica se o texto contém o divisor '* *'
    if '* *' in text:
        _paragraphs = text.split('* *')  # Divide o texto em parágrafos
    else:
        # Se não há divisores '* *', divide o texto em partes iguais
        total_length = len(text)
        part_length = total_length // number_of_parts
        _paragraphs = [text[i:i + part_length] for i in range(0, total_length, part_length)]

    # Ajusta o número de partes de acordo com a estimativa
    num_paragraphs_per_part = max(1, len(_paragraphs) // number_of_parts)
    _split_parts = [_paragraphs[i:i + num_paragraphs_per_part] for i in range(0, len(_paragraphs), num_paragraphs_per_part)]

    # Garante que _split_parts não tenha mais partes do que number_of_parts
    while len(_split_parts) > number_of_parts:
        last_part = _split_parts.pop()
        _split_parts[-1].extend(last_part)
    
    # Transforma as listas de partes em partes de texto
    _paragraph_parts = [' '.join(part) for part in _split_parts]

    return _paragraph_parts

# Configuração do Reddit
reddit_config = load_reddit_config()
reddit = praw.Reddit(   
    client_id=reddit_config['client_id'],
    client_secret=reddit_config['client_secret'],
    user_agent=reddit_config['user_agent']
)


# Função para buscar histórias populares no subreddit AITA
def get_popular_aita_stories(limit):
    subreddit = reddit.subreddit('AmItheAsshole')
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

import praw
import random

def get_random_aita_stories(num_posts=10):
    
    # Buscar as 500 postagens mais populares do subreddit AITA
    subreddit = reddit.subreddit('amitheasshole')
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

def get_random_recent_aita_stories(num_posts=10):
    
    # Buscar as 500 postagens mais populares do subreddit AITA
    subreddit = reddit.subreddit('amitheasshole')
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

def replace_profanities(text):
    profanities_dict = dict()
    with open("config/profanities.json") as file:
        profanities_dict = json.load(file)
        
    words = word_tokenize(text)
    
    # Replace profanities with euphemisms
    cleaned_words = [profanities_dict.get(word.lower(), word) for word in words]

    for key, value in profanities_dict.items():
        pattern = re.compile(r'\b' + re.escape(key) + r'\b', re.IGNORECASE)
        text = pattern.sub(value, text)
    
    # Reconstruct the text
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text