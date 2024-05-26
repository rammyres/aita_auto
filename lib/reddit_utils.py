import praw, configparser, os, json
from nltk.tokenize import word_tokenize

# Caminho para o arquivo de configuração
config_file = os.path.join(os.path.dirname(__file__),'..','config', 'reddit_config.ini')

# Estima o tempo da narração
def estimate_time(text):
    return (len(text.split())/150)*60

# Divide o tempo em segmentos para narração
def split_paragraphs(text, number_of_parts):
    _paragraphs = text.split("* *") # Divide o texto em parágrafos 

    # Divige os parágrafos em listas de partes de acordo com a estimativa de partes 
    _split_parts = [_paragraphs[i:i+number_of_parts] for i in range(0, len(_paragraphs), number_of_parts)]

    # Transforma as listas de partes em partes de texto
    _paragraph_parts = []
    for i in range(len(_split_parts)):
        _paragraph_parts.append(' '.join(_split_parts[i]))
        
    return _paragraph_parts
                  
# Função para carregar configurações do Reddit
def load_reddit_config():
    config = configparser.ConfigParser()
    config.read(config_file)
    return {
        'client_id': config.get('reddit', 'client_id'),
        'client_secret': config.get('reddit', 'client_secret'),
        'user_agent': config.get('reddit', 'user_agent')
    }

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

def replace_profanities(text):
    profanities_dict = dict()
    with open("config/profanities.json") as file:
        profanities_dict = json.load(file)
        
    words = word_tokenize(text)
    
    # Replace profanities with euphemisms
    cleaned_words = [profanities_dict.get(word.lower(), word) for word in words]
    
    # Reconstruct the text
    cleaned_text = ' '.join(cleaned_words)
    return cleaned_text