from blessed import Terminal
from lib.reddit_utils import *
from lib.data_utils import list_videos, delete_video
import json

term = Terminal()

def print_msg(msg):
    """
    Imprime uma mensagem no padrão do aplicativo.
    
    Args:
    msg (str): A mensagem a ser impressa.
    """
    print(term.clear())
    print(term.center("==================##################=================="))
    print(term.center(msg))
    print(term.center("==================##################=================="))

def suggest_gender(text):
    pattern = re.compile(r'(\d+[mfMF]|[mfMF]\d+)')
    match = pattern.search(text)
    if match:
        grupo = match.group(0)
        if grupo[-1].lower() in 'mf':
            sexo = grupo[-1].lower()
        else:
            sexo = grupo[0].lower()
        
        if sexo == 'm':
            return 'masculino'
        elif sexo == 'f':
            return 'feminino'
    return None

def set_gender(text):
    """
    Solicita ao usuário para definir o gênero do narrador.

    Returns:
    str: 'male' para masculino ou 'female' para feminino.
    """
    
    while True:
        try:
            print(term.clear())
            print(term.bold("Qual o gênero do narrador? "))
            gender = suggest_gender(text)
            if gender:
                print(f"Genero sugerido: {gender}")
            print(term.bold("1 - Masculino"))
            print(term.bold("2 - Feminino"))
            gender_input = input(term.bold("Escolha (1/2): "))
            
            if int(gender_input) == 1:
                return 'male'
            elif int(gender_input) == 2:
                return 'female'
            else:
                print(term.bold_red("Opção inválida"))
        except ValueError:
            print(term.bold_red("Escolha 1 ou 2"))

def set_subreddit():
    """
    Exibe um menu para o usuário selecionar um subreddit.

    Returns:
    str: O nome do subreddit escolhido.
    """
    with open('config/subreddits.json') as f:
        subreddits = json.load(f)['subreddits']
        
    while True:
        print(term.clear())
        print(term.bold("Escolha o subreddit ou outra opção:"))
        for i, subreddit in enumerate(subreddits):
            print(f"{i + 1} - {subreddit['name']} | {subreddit['description']}")
        print(f"{len(subreddits) + 1} - Listar vídeos existentes")
        print(f"{len(subreddits) + 2} - Excluir vídeos existentes")
        print("99 - Sair")

        try:
            choice = int(input(term.bold("Escolha a opção desejada: ")))
            if 1 <= choice <= len(subreddits):
                return subreddits[choice - 1]['name']
            elif choice == len(subreddits) + 1:
                video_paths = list_videos()
                if video_paths:
                    print("Vídeos disponíveis:")
                    for i, video in enumerate(video_paths):
                        print(f"{i + 1}. {video['title']}")
                    video_choice = int(input(term.bold("Digite o número do vídeo desejado: "))) - 1
                    return ['video', video_paths[video_choice]]
                else:
                    print(term.bold_red("Nenhum vídeo disponível."))
                    input(term.bold("Pressione ENTER para continuar"))
                    continue
            elif choice == len(subreddits) + 2:
                # Listar vídeos e excluir o selecionado
                videos = list_videos()
                if videos:
                    for idx, video in enumerate(videos):
                        print(f"{idx}. {video['title']}")
                    print("99 - Voltar")
                    delete_index = int(input(term.bold("Escolha o índice do vídeo para deletar: ")))
                    if delete_index == 99:
                        continue
                    else:
                        delete_video(delete_index)
                        print(term.bold_green("Vídeo deletado com sucesso."))
                else:
                    print(term.bold_red("Nenhum vídeo encontrado."))
                input(term.bold("Pressione ENTER para continuar"))
                continue
            elif choice == 99:
                print(term.bold("Encerrando..."))
                quit()
            else:
                print(term.bold_red("Opção inválida"))
        except ValueError:
            print(term.bold_red("Escolha uma opção numérica válida"))

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
    print(term.clear())
    print(term.bold("Selecione uma história para processar:"))
    print("1. Escolher entre os 10 posts mais populares")
    print("2. Escolher entre 10 posts aleatórios entre os 500 mais populares")
    print("3. Escolher entre 10 posts aleatórios entre os 100 mais populares da última semana")
    print("4. Inserir URL de um post específico")
    print("99. Voltar para o menu inicial")

    while True:
        try:
            choice = int(input(term.bold("Digite o número da opção desejada: ")))

            if choice == 1:
                # Obtém os 10 posts mais populares do subreddit
                stories = get_popular_stories(sub_name=sub_name, limit=10)
                valid_stories = filter_valid_stories(stories)
                if not valid_stories:
                    print(term.bold_red("Nenhuma história válida encontrada."))
                    return None
                print(term.bold("Escolha um dos seguintes posts:"))
                for i, story in enumerate(valid_stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input(term.bold("Digite o número da história desejada: "))) - 1
                return ["story", valid_stories[story_choice]]

            elif choice == 2:
                # Obtém 10 posts aleatórios entre os 500 mais populares do subreddit
                stories = get_random_stories(sub_name=sub_name, num_posts=10)
                valid_stories = filter_valid_stories(stories)
                if not valid_stories:
                    print(term.bold_red("Nenhuma história válida encontrada."))
                    return None
                print(term.bold("Escolha um dos seguintes posts:"))
                for i, story in enumerate(valid_stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input(term.bold("Digite o número da história desejada: "))) - 1
                return ["story", valid_stories[story_choice]]

            elif choice == 3:
                # Obtém 10 posts aleatórios entre os 100 mais populares da última semana do subreddit
                stories = get_random_recent_stories(sub_name=sub_name, num_posts=10)
                valid_stories = filter_valid_stories(stories)
                if not valid_stories:
                    print(term.bold_red("Nenhuma história válida encontrada."))
                    return None
                print(term.bold("Escolha um dos seguintes posts:"))
                for i, story in enumerate(valid_stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input(term.bold("Digite o número da história desejada: "))) - 1
                return ["story", valid_stories[story_choice]]

            elif choice == 4:
                # Insere URL de um post específico
                url = input(term.bold("Insira a URL do post específico: "))
                story = get_story_from_url(url)
                if story and is_valid_story(story):
                    return ['story', story]
                else:
                    print(term.bold_red("URL inválida ou post não encontrado."))
                    return None
            
            elif choice == 99:
                # Volta para o menu inicial
                break

            else:
                print(term.bold_red("Opção inválida."))
        except ValueError:
            print(term.bold_red("Escolha uma opção numérica"))

def cls():
    print(term.clear())
