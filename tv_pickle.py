import signal
import curses
import threading

from utils import *
from ui import UIEngine, Title, Menu, BLACK_7, BLOCK_ALPHABET, TINY
from api import API


startup = True

HOME_DIR = os.path.join(os.path.expanduser('~'), ".tvpickle")
CACHE_DIR = 'cache'
GENRE_DIR = 'genres'
CACHE_PATH = os.path.join(HOME_DIR, CACHE_DIR)
GENRE_PATH = os.path.join(HOME_DIR, GENRE_DIR)
CACHE_FILE = os.path.join(CACHE_PATH, 'cache.json')
GENRE_FILE = os.path.join(GENRE_PATH, 'genres.json')

#TMDB Modes
MODES = {'s':'/search', 'd':'/discover'}
FORMATS = {'m':'/movie', 't':'/tv', 'a':'/actor'}

TELEVISION = """___________
|  _______  |
| |       | |
| |       | |
| |       | |
| |_______| |
|  (o) (o)  |
|___________|"""

CINEMA = """ øoOoOooø
ooøOøOoOoo
||||||||||
||||||||||
||||||||||
||||||||||
||||||||||
⌞||||||||⌟"""

ACTOR = """    _______   
   |       |  
 __|_______|__
   / .   . \  
   w  / \  w  
   \ ##### /  
  __\  ^  /__ 
 |   \_V_/   |"""


INTRO_TITLE = """                                        ▄▄                     ▄▄          
███▀▀██▀▀███████▀   ▀███▀   ▀███▀▀▀██▄  ██        ▀███       ▀███          
█▀   ██   ▀█ ▀██     ▄█       ██   ▀██▄             ██         ██          
     ██       ██▄   ▄█        ██   ▄██▀███  ▄██▀██  ██  ▄██▀   ██   ▄▄█▀██ 
     ██        ██▄  █▀        ███████   ██ ██▀  ██  ██ ▄█      ██  ▄█▀   ██
     ██        ▀██ █▀         ██        ██ ██       ██▄██      ██  ██▀▀▀▀▀▀
     ██         ▄██▄          ██        ██ ██▄    ▄ ██ ▀██▄    ██  ██▄    ▄
   ▄████▄        ██         ▄████▄    ▄████▄█████▀▄████▄ ██▄▄▄████▄ ▀█████▀
                                                                           
                                                                           """



HEADER_TITLE = """░▀█▀░█▒█░░▒█▀▄░█░▄▀▀░█▄▀░█▒░▒██▀
░▒█▒░▀▄▀▒░░█▀▒░█░▀▄▄░█▒█▒█▄▄░█▄▄"""


MODE_SELECT = """▄▀▀ ██▀ █   ██▀ ▄▀▀ ▀█▀   █▄ ▄█ ▄▀▄ █▀▄ ██▀
▄██ █▄▄ █▄▄ █▄▄ ▀▄▄  █    █ ▀ █ ▀▄▀ █▄▀ █▄▄"""

TV_MODE = """▀█▀ █ █   █▄ ▄█ ▄▀▄ █▀▄ ██▀
█  ▀▄▀   █ ▀ █ ▀▄▀ █▄▀ █▄▄"""

MOVIE_MODE = """█▄ ▄█ ▄▀▄ █ █ █ ██▀   █▄ ▄█ ▄▀▄ █▀▄ ██▀
█ ▀ █ ▀▄▀ ▀▄▀ █ █▄▄   █ ▀ █ ▀▄▀ █▄▀ █▄▄"""

ACTOR_MODE = """▄▀▄ ▄▀▀ ▀█▀ ▄▀▄ █▀▄   █▄ ▄█ ▄▀▄ █▀▄ ██▀
█▀█ ▀▄▄  █  ▀▄▀ █▀▄   █ ▀ █ ▀▄▀ █▄▀ █▄▄"""

MODE_LOOKUP = {'tv':TV_MODE, 'movie':MOVIE_MODE, 'actor':ACTOR_MODE}

def gen_files(locs:dict):
    for directory, file in locs.items():
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(file):
            with open(file, 'w') as file:
                file.write('')

QUERY_CONTROLS = 'Tab: Change /: Enter Text Query, '

#Engine that holds together moving between modes and selection
class TVPickle():

    def __init__(self) -> None:
        self.api = API()
        self.ui = UIEngine()

        self.refresh_screen = True

        self.app_mode = '#'
        self.controls =  self.page_control_logic()
        self.refresh_mode = 'full' #Determine whether to run a full render
        self.input_idx = None #Determines whether a window is to be used to capture string input - Set to None out of cycle.

        self.function = self.cycle
        self.init_genres()

        signal.signal(signal.SIGWINCH, self.handle_resize)
        curses.curs_set(0)
        curses.cbreak()
        curses.noecho()

    def refresh(self):
        for window in self.ui.current_page.sections:
            window.refresh()

    def handle_resize(self, signum, frame):
        self.ui.resize_windows()
        self.ui.init_colors()
        self.cycle()

    def clear(self):
        self.ui.current_page.clear()
    
       #Based on current state relay what query parameters can be set
    def get_query_options(self)->str:
        render_text = ""  
        menu = self.api._PARAMS
        val = [[key, val] for key, val in menu[self.api.mode][self.api.format].items()]
        return '\n'.join([item[0] +": " + item[1] for item in val])
    
    def build_query_options(self):
        form = self.ui.format_text
        panel_content = [form()]

    def init_actor_mode(self):
        self.app_mode = 'Actor'
        self.select_screen('query')

    #Check whether a temporary cache of genres already exists and populate self.genres
    #TO DO - Make the validaty of genres expire after every 2 weeks
    def init_genres(self) -> dict:
        if not self.create_genre_files():
            self.genres = self.api.load_data(GENRE_FILE)
            return
        genre_lookup = {'Movie':{}, 'TV':{}}
        self.api.url = self.api._GENRE_MOVIE_LIST_URL
        result = self.api.http_request()['genres']
        genre_lookup['Movie']['name_to_id'] = {x['name']:str(x['id']) for x in result}
        genre_lookup['Movie']['id_to_name'] = {str(x['id']):x['name'] for x in result}
        self.api.url = self.api._GENRE_TV_LIST_URL
        result = self.api.http_request()['genres']
        genre_lookup['TV']['name_to_id'] = {x['name']:str(x['id']) for x in result}
        genre_lookup['TV']['id_to_name'] = {str(x['id']):x['name'] for x in result}
        self.genres = genre_lookup
        self.api.dump_data(GENRE_FILE, genre_lookup)
    
    def select_screen(self, screen):
        self.ui.current_page = self.ui.pages[screen]

    def parse_input(self, input):
        return self.page_control_logic[self.current_page][input]

    def create_genre_files(self)->bool:
        if os.path.isfile(GENRE_FILE) and os.path.getsize(GENRE_FILE) > 0:
            return False
        elif os.path.isfile(CACHE_FILE) and os.path.getsize(CACHE_FILE) > 0:
            return False
        else:
            gen_files({CACHE_PATH:CACHE_FILE, GENRE_PATH:GENRE_FILE})
            return True

    def generate_mode_options(self):
        return self.api.get_query_options(MODES)

    def init_decorate(self):
        self.ui.start_decorate()

    def resume_decorate(self):
        self.ui.stop_event.clear()

    def pause_decorate(self):
        self.ui.stop_event.set()

    ###########################################
    """CONTROL LOGIC FOR THE DIFFERENT MODES"""
    ###########################################

    def change_controls(self, controls):
        if not callable(controls): return
        self.controls = controls()

    #Specifies user flow of movement aroud the app
    def page_control_logic(self)->dict:
        control_logic = {
        'intro':{' ':[self.select_screen, {'screen':'mode'}], 'q': [exit], 'Q': [exit]},
        'mode':{' ':[self.select_screen, {'screen':'results'}], 'a':[self.init_discover_mode, {'app_mode':'Actor'}], 'A':[self.init_discover_mode, {'app_mode':'Actor'}], 'm':[self.init_discover_mode, {'app_mode':'Movie'}], 'M':[self.init_discover_mode, {'app_mode':'Movie'}], 't':[self.init_discover_mode, {'app_mode':'TV'}], 'T':[self.init_discover_mode, {'app_mode':'TV'}] },
        'results':{'q': [exit], '\x08':[self.select_screen, {'screen':'mode'}]},
        'discover':{'q': [exit], 'Q':[exit],'\x08':[self.select_screen,{'screen':'mode'}],'\x1b':[self.select_screen,{'screen':'mode'}], 'g':[self.change_controls, {'controls':self.genre_control_logic}]}
        }   
        return control_logic
    
    def genre_control_logic(self)->dict:
        genre_control = {'discover':{']':[self.ui.increment_menu, {'menu_name':'Genres'}], '[':[self.ui.decrement_menu, {'menu_name':'Genres'}],'q':[self.change_controls, {'controls':self.page_control_logic}], ' ':[self.add_selected_to_api, {'menu_name':'Genres'}]}}
        return genre_control

    #Used to export Menu UIElement seletions into the API
    def add_selected_to_api(self, menu_name, join_logic='|'):
        housing = []
        menu = self.ui.get_menu_by_name(menu_name)
        param_key = self.api._DISCOVER_LOOKUP[menu.title]
        value = menu.values[menu.selected]
        if self.api.params.get(param_key):
            current:str = self.api.params[param_key]
            if current.count(',') > 0:
                housing = current.split(',')
                join_logic = ','
            elif current.count('|') > 0:
                housing = current.split('|')
            else:
                housing = [current]
            if value not in housing:
                housing.append(value)
            self.api.params[param_key] = join_logic.join(housing)
        else:
            self.api.params[param_key] = value
        self.ui.current_page.content[3] = Menu('Result', self.api.params)

        #Change to the query mode which builds the user inputs into API requests
    def init_discover_mode(self, app_mode):
        self.app_mode = app_mode
        #Apply the top banner title
        self.ui.set_content('discover', 0, Title(app_mode, BLACK_7))
        #Convert the dictionary into a list menu - using only Keys
        if self.app_mode != 'Actor':
            #Build genres menu of content
            self.ui.set_content('discover', 1, Menu('Genres',self.genres[app_mode]['name_to_id'],display='key'))
            self.ui.set_content('discover', 2, Menu('Search Params', self.api._PARAMS[self.api.mode][self.api.format], display='key'))
            self.ui.set_content('discover', 3, 'Controls')
            self.ui.set_x_start('discover', 2, 1, 2, 3, 4)
        self.select_screen('discover')

    def select_genre(self, selection=0)->dict:
        self.refresh()
        self.ui.current_page.content[1].selected = selection
        
        input = chr(self.ui.get_keypress())
        if input not in genre_control:
            return self.select_genre(selection)
        else:
            data = genre_control[input]
            if len(data) == 1:
                return data[0]()
            elif len(data) > 1:
                return data[0](**data[1])
        self.function = self.cycle

    def attach_string_input(self, input):
        self.api.params['query'] = input

    def get_user_string(self):
        self.ui.current_page.sections[self.ui.current_page.input[0]].nodelay(False)
        curses.echo(True)
        input = self.getstr(*self.ui.current_page.input[1:]).decode('utf-8')
        self.attach_string_input(input)
    
    def cycle(self):
        self.ui.render()
        if len(self.ui.threads) == 0:
            self.ui.thread_task(self.ui.decorate_window)
        name = self.ui.current_page.name
        input = -1
        while input == -1:
            input = self.ui.get_keypress()
            if input not in self.controls[name]:
                input = -1
        data = self.controls[name][input]
        if len(data) > 1:
            data[0](**data[1])
        else:
            data[0]()
        return self.cycle()
    
