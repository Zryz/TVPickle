from engine import TVPickle
from pathlib import Path
import tmdbsimple as tmdb
import json
from utils import *

_cache = Path("./cache/search_history.json")
_genres = Path("./cache/genres.json")

class API(TVPickle):
    current = None #Holds the current request - we can strip from this as needed without additional requests
    cache = {} #An {pointer:result} format cache to store and traverse changes when new requests are sent
    pointer = 0
    stack = 0

    def __init__(self) -> None:
        if not _cache.is_file():
            _cache.touch(438)
        tmdb.API_KEY = API_KEY
        
    def _updateGenres(self):
        if not _genres.is_file():
            _genres.touch(438)
        if not hasattr(self, "genres"):
            setattr(self, "genres", None)
        with _genres.open("r+") as file:
            print(_genres.stat().st_size)
            if _genres.stat().st_size > 0:
                q = json.loads(file.read())
                self.genres = q
            else:
                self.genres = tmdb.Genres().movie_list()["genres"]
                json.dump(self.genres, file)
    
    def fprint(self, object, Index=False, Padding=4)->str: #Creates formated strings for lists or dictionarys with new lines and optional indexing
        z, r, t = "", "", 1
        if isinstance(object, list):
            m = len(object)
            for q in range(m):
                if Index:
                    z = str(t)
                    t+=1
                r += z + " " * (Padding-len(z)) + object[q] + "\n"
            return r
        elif isinstance(object, dict):
            for key in object.keys():
                if Index:
                    z = str(t)
                    t+=1
                r += z + " " * (Padding-len(z)) + object[key] + "\n" 
            return r

    def get_genre_names(self):
        if not hasattr(self, "genres"):
            self._updateGenres()
        val = {x["id"]:x["name"] for x in self.genres}
        return self.fprint(val, True)
    
    def choiceToGenre(self, choice:int)->dict:
        self._updateGenres()
        return tmdb.Discover.movie(with_genres=self.genres[choice]["id"])

    def getTitle(self, title):
        search = tmdb.Search()
        result = search.movie(query=title)
        self.cacheResults({title:result})
        print(result)

    def cacheResults(self, data:dict):
        with _cache.open("w") as file:
            json.dump(data, file)

    def readCache(self, query):
        if _cache.is_file():
            with _cache.open("r") as file:
                setattr(self, "cached",  json.load(file)) 

