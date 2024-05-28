from lib.reddit_utils import *

# Imprime uma mensagem no padrão do aplicativo
def print_msg(msg):
    print("==================##################==================")
    print(msg)
    print("==================##################==================")


# Define o genero da narração 
def set_gender():
    while(True):
        try:
            
                print("Qual o gênero do narrador? ")
                gender_input = input("1-Masc./2-Fem.: ")
                
                if int(gender_input) == 1:
                    return 'male'
                elif int(gender_input) == 2:
                    return 'female'
                else:
                    print("Opção inválida")
        except(ValueError):
            print("Escolha 1 ou 2")

# Menu de escolha da história
def select_story():
    print("Selecione uma história para processar:")
    print("1. Escolher entre os 10 posts mais populares")
    print("2. Escolher entre 10 posts aleatórios entre os 500 mais populares")
    print("3. Escolher entre 10 posts aleatórios entre os 100 mais populares da última semana")
    print("4. Inserir URL de um post específico")
    print("99 - Sair")

    while(True):
        try:    
            choice = int(input("Digite o número da opção desejada: "))
            
            if choice == 1:
                stories = get_popular_aita_stories(10)
                print("Escolha um dos seguintes posts:")
                for i, story in enumerate(stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input("Digite o número da história desejada: ")) - 1
                return stories[story_choice]
            
            if choice == 2:
                stories = get_random_aita_stories(10)
                print("Escolha um dos seguintes posts:")
                for i, story in enumerate(stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input("Digite o número da história desejada: ")) - 1
                return stories[story_choice]
            
            if choice == 3:
                stories = get_random_recent_aita_stories(10)
                print("Escolha um dos seguintes posts:")
                for i, story in enumerate(stories):
                    print(f"{i + 1}. {story['title']}")
                    print(f"   Link: {story['url']}")
                story_choice = int(input("Digite o número da história desejada: ")) - 1
                return stories[story_choice]
            
            elif choice == 4:
                url = input("Insira a URL do post específico: ")
                story = get_story_from_url(url)
                if story:
                    return story
                else:
                    print("URL inválida ou post não encontrado.")
                    return None
                
            elif choice == 99:
                print("Encerrando...")
                quit()
            
            else:
                print("Opção inválida.")
                # return None
        except ValueError:
            print("Escolha uma opção numérica")


