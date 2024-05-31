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