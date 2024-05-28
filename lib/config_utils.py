import configparser, os

# Caminho para o arquivo de configuração
reddit_config_file = os.path.join(os.path.dirname(__file__),'..','config', 'reddit_config.ini')
aai_config_file = os.path.join(os.path.dirname(__file__),'..','config', 'aai.ini')
aws_config_file = os.path.join(os.path.dirname(__file__), os.path.expanduser('~'),'.aws', 'credentials')
main_configs_file = os.path.join(os.path.dirname(__file__),'..','config', 'aita_auto.ini')

def check_reddit_config():
    if not os.path.exists(reddit_config_file):
        config = configparser.ConfigParser()
        
        print("O arquivo de configuração do reddit não existe")
        client_id = input("Insira o client_id do Reddit: ")
        client_secret = input("Insira o client_secret/key do Reddit: ")
        user_agent = input("Insira nome/versão do user agent (ex: meu_script:v1): ")
        
        config.add_section('reddit')
        config.set('reddit','client_id', client_id)
        config.set('reddit','client_secret', client_secret)
        config.set('reddit','user_agent', user_agent)

        with open(reddit_config_file, 'w+') as f:
            config.write(f)
            print("Arquivo de configuração escrito\n Se você estiver usando github inclua suas credenciais no .gitignore!")

# Função para carregar configurações do Reddit
def load_reddit_config():
    check_reddit_config()
    config = configparser.ConfigParser()
    config.read(reddit_config_file)
    return {
        'client_id': config.get('reddit', 'client_id'),
        'client_secret': config.get('reddit', 'client_secret'),
        'user_agent': config.get('reddit', 'user_agent')
    }

def check_aii_config():
    if not os.path.exists(aai_config_file):
        config = configparser.ConfigParser()
        
        print("O arquivo de configuração da Assembly.ai não existe")
        key = input("Insira a key: ")
        
        config.add_section('aai')
        config.set('aai','KEY', key)

        with open(aai_config_file, 'w+') as f:
            config.write(f)
            print("Arquivo de configuração escrito\n Se você estiver usando github inclua suas credenciais no .gitignore!")

def check_aws_config():
    if not os.path.exists(aws_config_file):
        config = configparser.ConfigParser()
        
        print("O arquivo de configuração da Assembly.ai não existe")
        aws_id = input("Insiera a id de acesso (aws access key id): ")
        aws_key = input("Insira a chave de acesso (aws access secret key): ")
        
        config.add_section('default')
        config.set('default','aws_access_key_id', aws_id)
        config.set('default', 'aws_secret_access_key', aws_key)

        with open(aai_config_file, 'w+') as f:
            config.write(f)
            print("Arquivo de configuração escrito\n Se você estiver usando github inclua suas credenciais no .gitignore!")

def check_configs():
    print("Verificando arquivos de configuração...")
    check_reddit_config()
    check_aii_config()
    check_aws_config()

