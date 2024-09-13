import curses, pyui, logging

from time import sleep

from api.api import TMDB_API
from common.defs import INTRO_TITLE, CINEMA, SEARCH, PAGE_STRUCTS, TELEVISION
from common.controls import tvpickle_controls
from common.elements import result_text_render

from pyui.ascii.fonts import BLACK_7, BLOCK_ALPHABET, TINY, TOY_BLOCKS
from pyui.test.paths import dump_object

api = TMDB_API()

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        #logging.StreamHandler(),  # Outputs logs to the console
        logging.FileHandler('app.log'),  # Logs to a file
    ]
)

#Engine that holds together moving between modes and selection
class TVPickle():
    def __init__(self) -> None:
        #It's best to instantiate the UI within the app for easier class resolution 
        self.logger = logging.getLogger(self.__class__.__name__)
        self.ui = pyui.PYUI(self)

        self.refresh_screen = True
        self.app_mode = '#'

        """API Initialisation"""
        self.genres = api.init_genres()

        """CONTROLS"""
        #Main application controls
        self.ui.controls.set_controls_db(tvpickle_controls(self))
        #Quit keys to exit app from anywhere
        self.ui.controls.set_quit_keys('q', 'Q')

        "Init App UI"
        self.build_ui()

        self.ui.controls.select('intro')

        self.cycle()

    def build_ui(self):
        """Create the application pages and the layouts, numbers of windows and borders for app"""
        self.ui.define_page_struct('intro', ([.08,.19,.55,.1,.08], [None, [.15,.7,.15], [.15,.7,.15], [.15,.7,.15], None], [-1,-1,0,-1,-1,0,-1,-1,0,-1,-1]))
        self.ui.define_page_struct('mode', ([0.25, .05, 0.65, 0.05], [None, None,[0.1, 0.4,0.4,0.1], None],[2,-1,-1,2,2,-1,-1]))
        self.ui.define_page_struct('discover', ([.20,.1,.45,.1,.15], [None, None,[.2,.15,.15,.15,.15,.2], [0.2,0.6,0.2], None], [2,-1,-1,0,0,0,0,-1,-1,0,-1,-1]))
        self.ui.define_page_struct('results', ([.2,.15,.45,.2], [[.6, None],[.6], [.2,.2,.2], [.6]], [0,0,1,2,2,2,2,0,-1,0], 2))
        self.ui.define_page_struct('image', ([.1,.8,.1], [None, None, None], [-1, 0, -1]))

        """Set the starting page"""
        self.ui.select_page('intro')

        """Assign fixed UI content such as titles and static window content"""

        #self.ui.content.set('intro', 1, pyui.Title(INTRO_TITLE) + 'Welcome to self Pickle - The ultimate self picking tool.' + '\nTo Begin Press Space!' )
        self.ui.content.set('intro', 2, pyui.Title('TV Pickle', TOY_BLOCKS, (45,90,243), y_centre=True))
        self.ui.content.set('intro', 5, pyui.UIImage("img/appicon.jpg", True))
        self.ui.content.set('intro', 8, pyui.Title('Press Space To Begin', BLOCK_ALPHABET))

        self.ui.content.set('mode', 0, pyui.Title('Choose A Mode', TOY_BLOCKS, rgb=(190, 20,1), y_centre=True))
        self.ui.content.set('mode', 3, pyui.Title(TELEVISION) + '' + pyui.Title('TV', BLACK_7) + '\n' + pyui.Title('Press T', BLOCK_ALPHABET))
        #self.ui.content.set('mode', 3, pyui.UIImage("img/appicon.png"))
        #self.ui.content.set('mode', 4, pyui.UIImage("img/danny.jpg"))
        self.ui.content.set('mode', 4, pyui.Title(CINEMA) + '' + pyui.Title('Movie', BLACK_7, rgb=(160,50,200)) + '\n' + pyui.Title('Press M',BLOCK_ALPHABET))
       # self.ui.content.set('mode', 5, pyui.Title(SEARCH) + '' + pyui.Title('Search', BLACK_7) + '\n' + pyui.Title('Press S', BLOCK_ALPHABET, (25,66,200)))
    
       #Based on current state relay what query parameters can be set
    def get_query_options(self)->str:
        render_text = ""  
        menu = api._PARAMS
        val = [[key, val] for key, val in menu[api.mode][api.format].items()]
        return '\n'.join([item[0] +": " + item[1] for item in val])
    
    def build_query_options(self):
        form = self.ui.format_text
        panel_content = [form()]

    def init_actor_mode(self):
        self.app_mode = 'Actor'
        self.select_screen('query')

    def parse_input(self, input):
        return self.page_control_logic[self.current_page][input]

    #Change to the query mode which builds the user inputs into API requests
    def init_discover_mode(self, app_mode):
        self.app_mode = app_mode
        api.mode = '/discover'
        match app_mode:
            case "TV":
                api.format = '/tv'
                api.title_ref = 'name'
            case "Movie":
                api.format = '/movie'
                api.title_ref = 'title'
            case "Actor":
                api.mode = '/search'
                api.format = '/person'
        #Apply the top banner title
        self.ui.content.set('discover', 0, pyui.Title(app_mode + ' Mode', BLACK_7, y_centre=True))
        #Convert the dictionary into a list menu - using only Keys
        genre_menu = pyui.Menu('Genres',self.genres[app_mode]['name_to_id'],display='key')
        api_menu = pyui.Menu('Search Params', api._PARAMS[api.mode][api.format], display='key')

        self.ui.controls.attach_binding('genre_menu', '[', genre_menu.prev)
        self.ui.controls.attach_binding('genre_menu', ']', genre_menu.next)
        self.ui.controls.attach_binding('genre_menu', ' ', [self.select_api_item, {'menu':genre_menu}])
        self.ui.controls.attach_binding('genre_menu', 'j', self.build_result_page)

        if self.app_mode != 'Actor':
            #Build genres menu of content
            self.ui.content.set('discover', 3, genre_menu)
            self.ui.content.set('discover', 4, api_menu)
            self.ui.content.set('discover', 5, api.params)

        self.ui.select_page('discover')

        self.ui.controls.select('discover')

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

    def build_result_page(self):
        
        self.results = self.build_against_api()
        self.result_idx = 0

        if not self.results:
            self.ui.content.set('results', 0, pyui.Title('Oh Dear', TINY))
            self.ui.content.set('results', 1, pyui.Title('Nothing found - press \'r\' to retry configs'))
            return
        
        else:
            self.update_result_ui()

            self.ui.controls.attach_binding('results', 'd', self.next_result)
            self.ui.controls.attach_binding('results', 'f', self.prev_result)
        
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


def run():
    tv = TVPickle()


    
run()
