import configparser
import os
import subprocess
import sys
import pkg_resources

# Caminho para o arquivo de configuração
reddit_config_file = os.path.join(os.getcwd(),'config', 'reddit_config.ini')
aai_config_file = os.path.join(os.getcwd(),'config', 'aai.ini')
aws_config_file = os.path.join(os.path.expanduser('~'),'.aws', 'credentials')
main_configs_file = os.path.join(os.getcwd(),'config', 'aita_auto.ini')

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

        with open(reddit_config_file, 'w+', encoding="utf-8") as f:
            config.write(f)
            print("Arquivo de configuração escrito\n Se você estiver usando um repositório git inclua suas credenciais no .gitignore!")

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
        
        config.add_section('aai_settings')
        config.set('aai_settings','KEY', key)

        with open(aai_config_file, 'w+') as f:
            config.write(f)
            print("Arquivo de configuração escrito\n Se você estiver usando um repositório git inclua suas credenciais no .gitignore!")

def get_aai_key():
    aai_config = configparser.ConfigParser()
    aai_config.read(aai_config_file)
    return aai_config.get('aai_settings','key')

def check_aws_config():
    if not os.path.exists(aws_config_file):
        config = configparser.ConfigParser()
        
        print("O arquivo de configuração da AWS não existe")
        aws_id = input("Insira a id de acesso (aws access key id): ")
        aws_key = input("Insira a chave de acesso (aws access secret key): ")
        
        config.add_section('default')
        config.set('default','aws_access_key_id', aws_id)
        config.set('default', 'aws_secret_access_key', aws_key)
        
        aws_dir = os.path.join(os.path.expanduser('~'),".aws")
        os.mkdir(aws_dir)

        with open(aws_config_file, 'w+') as f:
            config.write(f)
            print("Arquivo de configuração escrito\n Se você estiver usando um repositório git inclua suas credenciais no .gitignore!")

def check_configs(mode):
    _reddit_conf = not os.path.exists(reddit_config_file)
    _aws_conf = not os.path.exists(aws_config_file)
    _aai_conf = not os.path.exists(aai_config_file)

    if mode == 'gui' and any([_reddit_conf, _aws_conf, _aai_conf]):
        return False
    else:
        print("Verificando arquivos de configuração...")
        check_reddit_config()
        check_aii_config()
        check_aws_config()
    return True

def check_requirements(requirements_file):
    with open(requirements_file, 'r') as f:
        requirements = f.readlines()

    # Obter os pacotes instalados
    installed_packages = {pkg.key for pkg in pkg_resources.working_set}

    missing_packages = []

    for requirement in requirements:
        package_name = requirement.strip().split('==')[0]
        if package_name not in installed_packages:
            missing_packages.append(requirement.strip())

    if missing_packages:
        print("Os seguintes pacotes estão faltando:")
        for pkg in missing_packages:
            print(pkg)
        
        install = input("Deseja instalar os pacotes faltantes? (s/n): ").strip().lower()
        if install == 's':
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', requirements_file])

