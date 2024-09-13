import json, os, api
from urllib.parse import urlencode

from .http import http_request
from common.paths import check_for_file, load_data, dump_data, GENRE_FILE


#URL Helpers
DEFAULTS = {'include_adult':'false', 'language':'en-US', 'sort_by':'popularity.desc', 'page':'1'}

ID_LOOKUP = { '/discover':{
                    '/movie':{'with_cast':'/person'},
                    '/tv/':{'with_keywords', '/keyword', 'with_companies', '/company'}}
}

ID_SIMPLE = {'with_cast':'/person', 'with_genres':'/'}

FORMATS = ['/tv', '/person', '/movie']

"""This can be used by Menu elements to understand what query key their data is setting.
For example when working with the Genre menu it will append the selected genre to the with_genres.
There needs to be additional logic for determining if AND or OR combining is used via relevant | or , joiners"""


class TMDB_API:
    _PARAMS =  {'/search':{
                    '/movie':{'Query':'query', 'Include Adult':'include_adult', 'Release Year':'primary_release_year'}, 
                    '/tv':{'Query':'query', 'Incluse Adult':'include_adult', 'Release Year':'primary_release_year'},
                    '/person':{'Query':'query', 'Language':'language'}}, 
                '/discover':{
                    '/movie':{'Include Adult':'include_adult', 'Show Video':'include_video', 'Sort By':'sort_by', 'By Cast':'with_cast', 'By Genre/s':'with_genres', 'Release Year':'primary_release_year', 'Released Before':'primary_release_date.lte', 'Released After':'primary_release_date.gte'},
                    '/tv':{'First Air Date':'first_air_date_year', 'First Aired Before':'first_air_date.lte', 'First Aired After':'first_air_date.gte','Minimum Vote Average':'vote_average.gte', 'Keywords':'with_keywords', 'Companies':'with_companies'}
                            }
                }

    _DEFAULT_PARAMS = {'include_adult':False}
    _RENDERED_DATA = ['title', 'release_date', 'genre_ids', 'vote_average', 'overview']
    _BASEURL = 'https://api.themoviedb.org/3'
    _IMG_BASE = 'http://image.tmdb.org/t/p/'
    _IMG_SIZE = 'w300'
    _IMAGE = {
    "base_url": "http://image.tmdb.org/t/p/", "secure_base_url": "https://image.tmdb.org/t/p/",
    "backdrop":"w300","logo":"w154","poster": "w154", "profile":"w185","still":"w185" }

    _GENRE_MOVIE_LIST_URL = 'https://api.themoviedb.org/3/genre/movie/list'
    _GENRE_TV_LIST_URL = 'https://api.themoviedb.org/3/genre/tv/list'

    """Adds the param key when using the discover mode - the key is the current app mode"""
    _DISCOVER_LOOKUP = {'Genres':'with_genres'}

    def __init__(self) -> None:
        self.mode = '/discover'
        self.format = '/movie'
        self.url = ''
        self.params = {}
        self.page = '1'
        self.response = None
        self.header = ['accept:application/json','Authorization: Bearer ' + os.environ['API_TOKEN']]
        self.title_ref = 'title'

    def next_page(self):
        self.page = str(int(self.page)+1)
    
    def prev_page(self):
        self.page = str(int(self.page)-1)

    def add_to_params(self, param_key, value, join_logic='|'):
        if param_key not in self.params:
            self.params[param_key] = value
        else:
            current = self.params[param_key]
            if current.count(',') > 0:
                housing = current.split(',')
                #If a comma we switch to that for the join method later
                join_logic = ','
            elif current.count('|') > 0:
                housing = current.split('|')
            else:
                housing = [current]
            #Check for duplicates
            if value not in housing:
                housing.append(value)
            self.params[param_key] = join_logic.join(housing)

    def change_mode(self, mode):
        if mode not in self._PARAMS:
            print('mode not found - defaulting to discover')
            mode = '/discover'
        self.mode = mode

    def change_format(self, format):
        if format not in FORMATS:
            print('format not valid - setting to default /movie')
        self.format = format

    #Extract from _Params valid modes that can be chosen by the user based on format and append an * to indicate currently selected
    def get_valid_modes(self):
        modes = [key[1:].title() for key in self._PARAMS.keys() if self.format in self._PARAMS[key]]
        return modes
    
    def set_query(self, query):
        self.params['query'] = query

    def parse_params(self):
        id_lookups = []
        #Set page to load
        self.params['page'] = self.page
        for key, val in self.params.items():
            #Check whether the mode we're in contains an ID based lookup and not purely by text e.g Genres require ID's
            if self.mode == '/discover':
                self.check_id_lookup(key, val)
            #If we search for a genre we convert it to it's ID counterpart via genre lookup
            if key == 'with_genres':
                if self.genres['name_to_id'].get(val.title()) == None:
                    print("Can't find genre " + val)
                    return
                self.params[key] = self.genres['name_to_id'][val.title()]
            
    #Check keys in params against the lookup and ammend their value with their counterpart ID
    def check_id_lookup(self, key, query):
        if ID_LOOKUP[self.mode].get(self.format):
            if ID_LOOKUP[self.mode][self.format].get(key):
                format = ID_LOOKUP[self.mode][self.format][key]
                self.params[key] = self.get_value_id(format, query)

    #Rendering Tools
    def numerate_choices(self, choice:list) -> dict:
        return {str(idx):val for idx, val in enumerate(choice)}

    def get_choices(self):
        return self._PARAMS[self.mode][self.format]
        
    def fold_params(self, params:dict)->str:
        r = ""
        for key, value in params.items():
            if len(value) == 0:
                continue
            r += key + '=' + value + "&"
        return r

    def get_value_id(self, format, query, result_filter='results', return_size=1, logic_map:str='or'):
        #Define housing list r of id's and save prior API state for later reapplication
        r, save_state = [], (self.mode, self.format, self.params)
        self.params = {}
        self.mode = '/search' #We always use the search API to lookup ID's by their name
        self.format = format # 
        self.params['query'] = query
        self.build_url()
        response = self.http_request()[result_filter]

        for _ in range(len(response)):
            if _ == return_size: break
            r.append(response[_]['id'])
        self.mode, self.format, self.params = save_state[0], save_state[1], save_state[2]

        if logic_map == 'or': return "|".join(r)
        elif logic_map == 'and': return '&'.join(r)
        return "|".join(r)

    def input_parser(self, val:str)->str:
        if val.count('=') == 0 or val[:-1] == "=":
            raise SyntaxError('Invalid format of input given to parser', val)
        i, t, k, r = 0, '', None, {}
        while i < len(val):
            if val[i] not in " =":
                t+=val[i]
            else:
                if val[i] == "=":
                    if self._PARAMS[self.mode][self.format].get(t) != None:
                        self._PARAMS[self.mode][self.format][t]
                    else:
                        print('Invalid key!')
                        return r
                elif val[i] == " ":
                    r[k]=t
                t=''
            i+=1
        r[k]=t
        return r

    #Combine the core stages and logic for the API to get and fetchd data responses
    def run_cycle(self, query=None, mode=None, format=None, params:dict=None, url=None)->json:
        if mode: self.mode = mode
        if format: self.format = format
        if params: self.params = params
        if query: self.params['query'] = query
        if url: self.url = url
        else: self.build_url()
        return http_request(self.url, self.header)

    #Base user input around specifying the options to a mode in traditional console format 'a=this b=that'
    #This uses a space as markers to differentiate requests
    def build_url(self)->str:
        #folded_params = self.fold_params(self.params)
        folded_params = urlencode(self.params)
        #print(folded_params)
        self.url = self._BASEURL + self.mode + self.format + '?' + folded_params
        #if url[-1] == '&': url = url[:-1]
        #return url

    def abbreviate_options(self, data:list):
        r = {}
        for g in range(len(data)):
            i = 0
            while i < len(data[g])-1:
                if not r.get(data[g][0:i+1]):
                    r[data[g][0:i+1]] = data[g]
                    break
                i+=1
            continue
        return r
    
    def generate_image(self, result):
        #Fetch the poster_path image data from a result and return it's raw image
        if not result['poster_path']: return
        url = TMDB_API._IMG_BASE + TMDB_API._IMG_SIZE + result['poster_path']
        image = http_request(url, direct=True)
        return image

    def overide_url(self, url):
        self.url = url

    def api_set_mode(self, mode):
        self.mode = mode
    
    def readResponse(self, params=None, response=None):
        if not response: return self.response
        else:
            if isinstance(params, list):
                for x in params:
                    response = response[x]
        return response

    def api_render_results(self):
        r = ''
        if not self.response: return
        for response in self.response:
            for x in self._RENDERED_DATA:
                v = response[x]
                if not isinstance(v, str):
                    v = str(v)
                r += '\n'
                r += v
                if x != self._RENDERED_DATA[-1]: r += ' - \n'
                r  += '\n'

    #Check whether a temporary cache of genres already exists and populate self.genres
    #TO DO - Make the validaty of genres expire after every 2 weeks
    def init_genres(self) -> dict:
        if not check_for_file(GENRE_FILE):
            r = load_data(GENRE_FILE)
            return r
        genre_lookup = {'Movie':{}, 'TV':{}}
        self.url = self._GENRE_MOVIE_LIST_URL
        result = http_request()['genres']
        genre_lookup['Movie']['name_to_id'] = {x['name']:str(x['id']) for x in result}
        genre_lookup['Movie']['id_to_name'] = {str(x['id']):x['name'] for x in result}
        self.url = self._GENRE_TV_LIST_URL
        result = http_request()['genres']
        genre_lookup['TV']['name_to_id'] = {x['name']:str(x['id']) for x in result}
        genre_lookup['TV']['id_to_name'] = {str(x['id']):x['name'] for x in result}
        dump_data(GENRE_FILE, genre_lookup)
        return genre_lookup
