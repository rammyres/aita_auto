import praw, configparser, os

# Caminho para o arquivo de configuração
config_file = os.path.join(os.path.dirname(__file__),'..','config', 'reddit_config.ini')

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
    reddit = praw.Reddit(client_id='YOUR_CLIENT_ID',
                         client_secret='YOUR_CLIENT_SECRET',
                         user_agent='YOUR_USER_AGENT')
    
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
    # Inicializar o cliente PRAW
    reddit = praw.Reddit(client_id='seu_client_id',
                         client_secret='seu_client_secret',
                         user_agent='Descrição do seu script')
    
    # Buscar as 200 postagens mais populares do subreddit AITA
    subreddit = reddit.subreddit('amitheasshole')
    top_posts = subreddit.top(limit=200)  # Limitar à 200 postagens mais populares
    
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

