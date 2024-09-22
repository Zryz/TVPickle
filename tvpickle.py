import curses, pyui, logging

from logging.handlers import RotatingFileHandler
from api.api import TMDB_API
from common.defs import CINEMA, TELEVISION
from common.elements import result_text_render

from pyui.ascii.fonts import BLACK_7, BLOCK_ALPHABET, TINY, TOY_BLOCKS

#Api caller which defines what mode / state app is in
api = TMDB_API()

#Prevent balooning of log file
log_handler = RotatingFileHandler(
    'tvpickle.log',  # Log file name
    maxBytes=5*1024*1024,  # Max file size: 5 MB
    backupCount=3  # Keep 3 backup files
)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[log_handler]
)

class TVPickle():
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.app_mode: str

        """API Initialisation"""
        
        self.genres = api.init_genres()
        
        "Init App UI"
        self.ui = pyui.PYUI(self)
        self.build_ui()
        self.ui.controls.set_controls_db(tvpickle_controls(self))

        self.ui.controls.set_quit_keys('q', 'Q')
        self.ui.controls.select('intro')

        self.cycle()

    def build_ui(self):
        """Create the application pages and the layouts, numbers of windows and borders for app"""
        self.ui.define_page_struct('intro', ([.08,.19,.55,.1,.08], [None, [.15,.7,.15], [.15,.7,.15], [.15,.7,.15], None], [-1,-1,0,-1,-1,0,-1,-1,0,-1,-1]))
        self.ui.define_page_struct('format', ([0.25, .05, 0.65, 0.05], [None, None,[0.1, 0.4,0.4,0.1], None],[2,-1,-1,2,2,-1,-1]))
        self.ui.define_page_struct('mode', ([0.25, .05, 0.65, 0.05], [None, None,[0.1, 0.4,0.4,0.1], None],[2,-1,-1,2,2,-1,-1]))
        self.ui.define_page_struct('discover', ([.20,.1,.45,.1,.15], [None, None,[.2,.15,.15,.15,.15,.2], [0.2,0.6,0.2], None], [2,-1,-1,0,0,0,0,-1,-1,0,-1,-1]))
        self.ui.define_page_struct('results', ([.2,.15,.45,.2], [[.6, None],[.6], [.2,.2,.2], [.6]], [0,0,1,2,2,2,2,0,-1,0], 3))
        self.ui.define_page_struct('image', ([.1,.8,.1], [None, None, None], [-1, 0, -1]))

        self.ui.define_window_properties('format', 4, {'bg':(10,90,210), 'fg':(255,0,255)})

        """Set the starting page"""
        self.ui.select_page('intro')

        """Assign fixed UI content such as titles and static window content"""

        #self.ui.content.set('intro', 1, pyui.Title(INTRO_TITLE) + 'Welcome to self Pickle - The ultimate self picking tool.' + '\nTo Begin Press Space!' )
        self.ui.content.set('intro', 2, pyui.Title('TV Pickle', TOY_BLOCKS, (45,90,243), y_centre=True))
        self.ui.content.set('intro', 5, pyui.UIImage("img/appicon.jpg", True))
        self.ui.content.set('intro', 8, pyui.Title('Press Space To Begin', BLOCK_ALPHABET))

        self.ui.content.set('format', 0, pyui.Title('Choose A Mode', TOY_BLOCKS, rgb=(190, 20,1), y_centre=True))
        self.ui.content.set('format', 3, [pyui.UIImage('img/tv.jpg', center=True), pyui.Title('Press T', BLACK_7, rgb=(34,56,120), write_line=3)])
        self.ui.content.set('format', 4, [pyui.UIImage('img/movie.jpg', center=True), pyui.Title('Press M',BLACK_7, rgb=(120,38,55),write_line=3)])

    def set_format(self, app_mode):
        self.app_mode = app_mode
        self.api_by_format()

    def api_by_format(self):
        match self.app_mode:
            case "tv":
                api.format = '/tv'
                api.title_ref = 'name'
            case "movie":
                api.format = '/movie'
                api.title_ref = 'title'

    def select_api_item(self, menu:pyui.Menu):
        api.add_to_params('with_genres', menu.get_value())
        self.ui.content.set('discover', 4, api.params)

    def attach_string_input(self, input):
        api.params['query'] = input

    def get_user_string(self):
        self.ui.active_page.sections[self.ui.active_page.input[0]].nodelay(False)
        curses.echo(True)
        input = self.getstr(*self.ui.active_page.input[1:]).decode('utf-8')
        self.attach_string_input(input)

    def build_against_api(self):
        return api.run_cycle()['results']

    def current_result(self):
        if not hasattr(self, 'results'): return
        return self.results[self.result_idx]

    def next_result(self):
        if self.result_idx < len(self.results)-1:
            self.result_idx += 1
        self.update_result_ui()

    def prev_result(self):
        if self.result_idx > 0:
            self.result_idx -=1
        self.update_result_ui()

    def update_result_ui(self):
        p_name = 'results'
        self.ui.content.clear(p_name)
        self.ui.content.set(p_name, 0, pyui.Title('Results', TOY_BLOCKS, (230,20,10), y_centre=True))
        self.ui.content.set(p_name, 2, pyui.Title(self.current_result()[api.title_ref], BLACK_7, (120,23,233), y_centre=True))
        self.ui.content.set(p_name, 4, pyui.Title('Info', BLOCK_ALPHABET , (0,120,120),False))
        self.ui.content.set(p_name, 4, result_text_render(self.current_result()))
        self.ui.content.set(p_name, 1, pyui.UIImage(api.generate_image(self.current_result()), True))
        self.ui.content.set(p_name, 6, pyui.Title('Use left and right to switch between results', TINY))

    def build_discover_page(self):
        self.ui.content.set('discover', 0, pyui.Title(self.app_mode + ' Mode', BLACK_7, y_centre=True))
        self.build_genre_menu()
        self.build_api_menu()

        self.ui.select_page('discover')
        self.ui.controls.select('discover')

    def build_api_menu(self):
        api_menu = pyui.Menu('Search Params', api._PARAMS[api.mode][api.format], display='key')
        self.ui.content.set('discover', 4, api_menu)
        self.ui.content.set('discover', 5, api.params)

    def build_genre_menu(self):
        genre_menu = pyui.Menu('Genres',self.genres[self.app_mode]['name_to_id'],display='key', title_font=BLACK_7, text_font=BLOCK_ALPHABET)

        self.ui.controls.attach_binding('genre_menu', '[', genre_menu.prev)
        self.ui.controls.attach_binding('genre_menu', ']', genre_menu.next)
        self.ui.controls.attach_binding('genre_menu', ' ', [self.select_api_item, {'menu':genre_menu}])
        self.ui.controls.attach_binding('genre_menu', 'j', self.build_result_page)

        self.ui.content.set('discover', 3, genre_menu)

    def build_result_page(self):
        
        self.results = self.build_against_api()
        self.result_idx = 0

        if not self.results:
            self.ui.content.set('results', 0, pyui.Title('Oh Dear', TINY))
            self.ui.content.set('results', 1, pyui.Title('Nothing found - press \'r\' to retry configs'))
            return
        
        else:
            self.update_result_ui()

            self.ui.controls.attach_binding('results', curses.KEY_RIGHT, self.next_result)
            self.ui.controls.attach_binding('results', curses.KEY_LEFT, self.prev_result)
        
        self.ui.controls.select('results')
        self.ui.select_page('results')
        
    def cycle(self):
        while True:
            self.ui.render()
            stack = self.ui.controls()
            self.logger.info(stack)
            i = 0
            while i < len(stack):
                task = stack[i]
                if not callable(task[0]):
                    i+=1
                    continue
                if len(task) > 1:
                    task[0](**task[1])
                else:
                    task[0]()
                i+=1 

""" App Controls """

def tvpickle_controls(tvpickle:TVPickle)->dict:
    return {
        'universal':{
                    'a': [ [tvpickle.ui.pause_decoration]],
                    's': [[ tvpickle.ui.restart_decoration]]
                },
        'intro':{
                    ' ': [ [tvpickle.ui.select_page, {'name':'format'}], [tvpickle.ui.controls.select, {'control_name':'format'}]],
                },

        'discover':{
                    'g':[[tvpickle.ui.controls.select,{'control_name':'genre_menu'}]]
                },

        'format':{
                    'm':[[tvpickle.set_format, {'app_mode':'movie'}], [tvpickle.build_discover_page]], 
                    'M':[[tvpickle.set_format, {'app_mode':'movie'}]], 
                    't':[[tvpickle.set_format, {'app_mode':'tv'}]],
                    'T':[[tvpickle.set_format, {'app_mode':'tv'}]] 
                },

        'results':{ 
                    'left':[[tvpickle.prev_result]], 
                    'right':[[tvpickle.next_result]]
                }      
        }

def run():
    tv = TVPickle()


    
run()
