#Everything that handles files read and write processes and disk locations

import os, json

HOME_DIR = os.path.join(os.path.expanduser('~'), ".tvpickle")
CACHE_DIR = 'cache'
GENRE_DIR = 'genres'
CACHE_PATH = os.path.join(HOME_DIR, CACHE_DIR)
GENRE_PATH = os.path.join(HOME_DIR, GENRE_DIR)
CACHE_FILE = os.path.join(CACHE_PATH, 'cache.json')
GENRE_FILE = os.path.join(GENRE_PATH, 'genres.json')


def gen_files(locs:dict):
    for directory, file in locs.items():
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(file):
            with open(file, 'w') as file:
                file.write('')

def check_for_file(file)->bool:
    if os.path.isfile(file) and os.path.getsize(file) > 0:
        return False
    else:
        return True
    
def join_paths(*paths):
    return os.path.join(HOME_DIR, *paths)

    #Load data from a file
def load_data(file)->json:
    if os.path.getsize(file) == 0: return
    with open(file, 'r') as local:
        return json.load(local)

def dump_data(file, data=None):
    with open(file, 'w') as file:
        json.dump(data, file)
