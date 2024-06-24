import os, json 

database_path = 'output/videos_db.json'

# Atualiza a lista de videos existentes
def save_to_json(data, filepath=database_path):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                existing_data = json.load(f)
            except json.JSONDecodeError:
                existing_data = []
    else:
        existing_data = []

    existing_data.append(data)

    with open(filepath, 'w') as f:
        json.dump(existing_data, f, indent=4)


# Lista os videos existentes
def list_videos(filepath=database_path):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
                return data
            except json.JSONDecodeError:
                return []
    else:
        return []
    
def delete_video(index, filepath=database_path):
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Erro ao ler o arquivo JSON.")
                return
        
        if 0 <= index < len(data):
            # Deletar os arquivos de vídeo referenciados
            video_data = data.pop(index)
            folder = ''
            for video in video_data['videos']:
                video_path = video['video']
                folder = video_path.split('/') # atualiza a pasta para posterior deleção
                if os.path.exists(video_path):
                    os.remove(video_path)
                    print(f"Arquivo {video_path} deletado.")
                else:
                    print(f"Arquivo {video_path} não encontrado.")

            # monta o caminho para a pasta
            folderpath = os.path.join(*[fp for fp in folder[:-1]])
            os.remove(f'{folderpath}/fulltext.txt') # remove o arquivo do texto da história
            os.removedirs(folderpath) # apaga a pasta

            # Salvar os dados atualizados no JSON
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            
            print("Vídeo e dados deletados com sucesso.")
            return
        else:
            print("Índice inválido.")
    else:
        print("Arquivo JSON não encontrado.")