#Everything that handles files read and write processes and disk locations

import os

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


def create_genre_files()->bool:
    if os.path.isfile(GENRE_FILE) and os.path.getsize(GENRE_FILE) > 0:
        return False
    elif os.path.isfile(CACHE_FILE) and os.path.getsize(CACHE_FILE) > 0:
        return False
    else:
        gen_files({CACHE_PATH:CACHE_FILE, GENRE_PATH:GENRE_FILE})
        return True
    
def join_paths(*paths):
    return os.path.join(HOME_DIR, *paths)
