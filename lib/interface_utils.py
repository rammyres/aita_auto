from lib.reddit_utils import *
from lib.data_utils import *
import json

def print_msg(msg):
    """
    Imprime uma mensagem no padrão do aplicativo.
    
    Args:
    msg (str): A mensagem a ser impressa.
    """
    print("==================##################==================")
    print(msg)
    print("==================##################==================")

def set_gender():
    """
    Solicita ao usuário para definir o gênero do narrador.

    Returns:
    str: 'male' para masculino ou 'female' para feminino.
    """
    while True:
        try:
            print("Qual o gênero do narrador? ")
            gender_input = input("1-Masc./2-Fem.: ")
            
            if int(gender_input) == 1:
                return 'male'
            elif int(gender_input) == 2:
                return 'female'
            else:
                print("Opção inválida")
        except ValueError:
            print("Escolha 1 ou 2")

def set_subreddit():
    """
    Exibe um menu para o usuário selecionar um subreddit.

    Returns:
    str: O nome do subreddit escolhido.
    """
    with open('config/subreddits.json') as f:
        subreddits = json.load(f)['subreddits']
        
    print("Escolha o subreddit ou outra opção:")
    for i, subreddit in enumerate(subreddits):
        print(f"{i + 1} - {subreddit['name']} | {subreddit['description']}")
    print(f"{len(subreddits) + 1} - Listar vídeos existentes")
    print("99 - Sair")

    while True:
        try:
            choice = int(input("Escolha a opção desejada: "))
            if 1 <= choice <= len(subreddits):
                return subreddits[choice - 1]['name']
            elif choice == len(subreddits) + 1:
                video_paths = list_videos()
                if video_paths:
                    print("Vídeos disponíveis:")
                    for i, video in enumerate(video_paths):
                        print(f"{i + 1}. {video['title']}")
                    video_choice = int(input("Digite o número do vídeo desejado: ")) - 1
                    return ['video', video_paths[video_choice]]
                else:
                    print("Nenhum vídeo disponível.")
                    return None
            elif choice == 99:
                print("Encerrando...")
                quit()
            else:
                print("Opção inválida")
        except ValueError:
            print("Escolha uma opção numérica válida")

def is_valid_story(story):
    """
    Verifica se o post é apenas uma imagem ou vídeo.

    Args:
    story (dict): O dicionário contendo informações do post.

    Returns:
    bool: False se for uma imagem ou vídeo, True caso contrário.
    """
    if story['url'].endswith(('.jpg', '.jpeg', '.png', '.gif', '.mp4', '.mov', '.webm')):
        return False
    return True

def filter_valid_stories(stories):
    """
    Filtra histórias válidas que não são apenas imagens ou vídeos.

    Args:
    stories (list): Lista de dicionários contendo informações dos posts.

    Returns:
    list: Lista filtrada com posts válidos.
    """
    return [story for story in stories if is_valid_story(story)]

def selection_menu():
    """
    Exibe o menu de seleção de histórias e permite ao usuário escolher uma opção.

    Returns:
    list: Uma lista contendo o tipo e o conteúdo escolhido pelo usuário.
    """
    subreddit_selection = set_subreddit()
    if subreddit_selection is None:
        return None
    elif subreddit_selection[0] == 'video':
        return subreddit_selection
    
    sub_name = subreddit_selection
    print()
    print("Selecione uma história para processar:")
    print("1. Escolher entre os 10 posts mais populares")
    print("2. Escolher entre 10 posts aleatórios entre os 500 mais populares")
    print("3. Escolher entre 10 posts aleatórios entre os 100 mais populares da última semana")
    print("4. Inserir URL de um post específico")

    while True:
        try:
            choice = int(input("Digite o número da opção desejada: "))

            if choice == 1:
                # Obtém os 10 posts mais populares do subreddit
                stories = get_popular_stories(sub_name=sub_name, limit=10)
                valid_stories = filter_valid_stories(stories)
                if not valid_stories:
                    print("Nenhuma história válida encontrada.")
                    return None
                print("Escolha um dos seguintes posts:")
                for i, story in enumerate(valid_stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input("Digite o número da história desejada: ")) - 1
                return ["story", valid_stories[story_choice]]

            elif choice == 2:
                # Obtém 10 posts aleatórios entre os 500 mais populares do subreddit
                stories = get_random_stories(sub_name=sub_name, num_posts=10)
                valid_stories = filter_valid_stories(stories)
                if not valid_stories:
                    print("Nenhuma história válida encontrada.")
                    return None
                print("Escolha um dos seguintes posts:")
                for i, story in enumerate(valid_stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input("Digite o número da história desejada: ")) - 1
                return ["story", valid_stories[story_choice]]

            elif choice == 3:
                # Obtém 10 posts aleatórios entre os 100 mais populares da última semana do subreddit
                stories = get_random_recent_stories(sub_name=sub_name, num_posts=10)
                valid_stories = filter_valid_stories(stories)
                if not valid_stories:
                    print("Nenhuma história válida encontrada.")
                    return None
                print("Escolha um dos seguintes posts:")
                for i, story in enumerate(valid_stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input("Digite o número da história desejada: ")) - 1
                return ["story", valid_stories[story_choice]]

            elif choice == 4:
                # Insere URL de um post específico
                url = input("Insira a URL do post específico: ")
                story = get_story_from_url(url)
                if story and is_valid_story(story):
                    return ['story', story]
                else:
                    print("URL inválida ou post não encontrado.")
                    return None

            else:
                print("Opção inválida.")
        except ValueError:
            print("Escolha uma opção numérica")