import praw, json, re, random
from lib.config_utils import *
import nltk
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

def repair_broken_words(text):
    # Repair hyphenated line breaks
    repaired_text = re.sub(r'-\n\s*', '', text)
    # Repair line breaks without hyphens (if they occur within words)
    repaired_text = re.sub(r'(\S)\n(\S)', r'\1\2', repaired_text)
    # Repair common contraction splits
    contractions = [
        (r'\bwas\s+n\'t\b', "wasn't"),
        (r'\bwh\s+o\'s\b', "who's"),
        (r'\bcan\s+n\'t\b', "can't"),
        (r'\bdo\s+n\'t\b', "don't"),
        (r'\bdoes\s+n\'t\b', "doesn't"),
        (r'\bdid\s+n\'t\b', "didn't"),
        (r'\bshould\s+n\'t\b', "shouldn't"),
        (r'\bwould\s+n\'t\b', "wouldn't"),
        (r'\bcould\s+n\'t\b', "couldn't"),
        (r'\bhe\s+is\b', "he's"),
        (r'\bshe\s+is\b', "she's"),
        (r'\bit\s+is\b', "it's"),
        (r'\bthat\s+is\b', "that's"),
        (r'\bthere\s+is\b', "there's"),
        (r'\bwhat\s+is\b', "what's"),
        (r'\bwhere\s+is\b', "where's"),
        (r'\bwho\s+is\b', "who's"),
        (r'\bwe\s+are\b', "we're"),
        (r'\byou\s+are\b', "you're"),
        (r'\bthey\s+are\b', "they're"),
        (r'\bi\s+am\b', "I'm"),
        (r'\bwe\s+will\b', "we'll"),
        (r'\byou\s+will\b', "you'll"),
        (r'\bthey\s+will\b', "they'll"),
        (r'\bhe\s+will\b', "he'll"),
        (r'\bshe\s+will\b', "she'll"),
        (r'\bit\s+will\b', "it'll"),
        (r'\bthat\s+will\b', "that'll"),
        (r'\bthere\s+will\b', "there'll"),
        (r'\bwhat\s+will\b', "what'll"),
        (r'\bwhere\s+will\b', "where'll"),
        (r'\bwho\s+will\b', "who'll")
    ]
    for pattern, replacement in contractions:
        repaired_text = re.sub(pattern, replacement, repaired_text, flags=re.IGNORECASE)

    return repaired_text


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
    """
    Esta função preprocessa o texto para remover
    clutter (simbolos indevidos, urls) e também
    remove palavrões comuns, substituindo por 
    eufemismos e troca siglas pelos seus signi-
    ficados.
    """

    text = merge_accidental_splits(text)
    # Substitui palavrões pelos eufemismos
    profanities_dict = dict()
    with open("config/profanities.json") as file:
        profanities_dict = json.load(file)
    
    for k, v in profanities_dict.items():
        text = re.sub(rf'\b{k}\b', v, text)
    
    # Substitui siglas pela seus significados:
    acronyms_dict = dict()
    with open('config/acronyms.json', 'r') as file:
        acronyms_dict = json.load(file)

    for k, v in acronyms_dict.items():
        text = re.sub(rf'\b{k}\b', v, text)
    
    # Retira caracteres indesejados
    pattern = r"\s*’\s*"
    text = re.sub(pattern, "'", text)

    # Remove urls do texto
    text = re.sub(r"http\S+", "", text)

    # Remove #x200b do texto 
    text = re.sub(r'&\s*#\s*x200B', '', text)

    # text = repair_broken_words(text)

    # Usa NLTK para verificar se algum palavrão escapou
    words = word_tokenize(text) # Transforma o texto em tokens

    cleaned_words = [profanities_dict.get(word.lower(), word) for word in words]
    
    # Reconstroi o texto
    cleaned_text = ' '.join(cleaned_words)
    
    return cleaned_text
