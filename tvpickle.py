import curses, signal

from ui.engine import UIEngine
from api.api import TMDB_API
from resultrenderer import ResultRender

ui = UIEngine()

#Engine that holds together moving between modes and selection
class TVPickle():
    def __init__(self) -> None:
        self.api = TMDB_API()

        self.refresh_screen = True
        self.app_mode = '#'
        self.refresh_mode = 'full' #Determine whether to run a full render

        """Build the API genre lookup tables since genres use ID's and not names"""
        self.build_pages()
        self.init_genres()

        """Results from the API are stored directly in list format from 'results'
           Each value represents a TV or Movie"""
        self.api_results:list = []

        signal.signal(signal.SIGWINCH, self.handle_resize)
        curses.curs_set(0)
        curses.cbreak()
        curses.noecho()

        """Set controls and begin app main cycle"""
        #Creates a self.controls
        self.change_controls(self.page_control_logic)
        self.cycle()

    ###################################
    """Curses window resize handler"""
    ###################################

    def handle_resize(self, signum, frame):
        self.ui.stop_thread()
        self.ui.resize_windows()
        self.ui.thread_task(self.ui.decorate_window)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        self.cycle()

    def build_pages(self):
        """Create the application pages and the layouts, numbers of windows and borders for app"""
        self.ui.create_page('intro', [.1,.8,.1], [None, None, None], [0,1,0])
        self.ui.create_page('mode', [0.25, .05, 0.65, 0.05], [None, None,[0.1, 0.27,0.27,0.26, 0.1], None],[2,0,0,2,2,2,0,0])
        self.ui.create_page('results', [1], [[.5,.5]],[1,1])
        self.ui.create_page('discover', [.25,.05,.45,.1,.15], [None, None,[.2,.15,.15,.15,.15,.2], [0.2,0.6,0.2], None], [2,0,0,-1,-1,-1,-1,0,0,1,0,0])

        """Assign fixed UI content such as titles and static window content"""

        self.ui.set_content('intro', 0, Title(INTRO_TITLE)+ 'Welcome to self Pickle - The ultimate self picking tool.' +'\nTo Begin Press Space!' )
        self.ui.set_content('mode', 0, Title('Choose A Mode', BLACK_7))
        self.ui.set_content('mode', 1, UIImage("img/appicon.png"))
        self.ui.set_content('mode', 2, Title(CINEMA) + ''+ Title('Movie', BLOCK_ALPHABET) + '\n' + Title('Press M',BLOCK_ALPHABET))
        self.ui.set_content('mode', 3, Title(ACTOR) + '' + Title('Actor', BLOCK_ALPHABET) + '\n' + Title('Press A', BLOCK_ALPHABET))

        """Set the starting page"""
        self.ui.select_page('intro')

    def clear(self):
        self.ui.active_page.clear()
    
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

    def select_screen(self, screen):
        if screen not in self.ui.pages: return
        if self.ui.active_page != None: 
            self.prev_page = self.ui.active_page
        #To prevent leaking of decorate into new screen we must stop and restart the decorate
        self.ui.stop_thread()
        self.ui.active_page = self.ui.pages[screen]
        self.ui.start_decorate()

    def previous_screen(self):
        if hasattr(self, 'prev_page'):
            self.ui.active_page = self.prev_page
            self.controls = self.prev_controls

    def parse_input(self, input):
        return self.page_control_logic[self.current_page][input]
        
    def next_result(self):
        if not hasattr(self, 'results'):
            raise ValueError('TVPickl has no results object')
        if not isinstance(self.results, ResultRender):
            raise TypeError("Content not a result render object")
        self.results.next_result()
        self.update_result_ui()

    def prev_result(self):
        if not hasattr(self, 'results'):
            raise ValueError('TVPickle has no results object')
        if not isinstance(self.results, ResultRender):
            raise TypeError("Content not a result render object")
        self.results.prev_result()
        self.update_result_ui()

    def update_result_ui(self):
        #self.ui.page.content[0] = Title(self.results.title, TINY)
        self.ui.active_page.content[0] = self.results.render()
        self.ui.active_page.content[1] = UIImage(self.results.image_data)

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
        if hasattr(self, 'controls'): self.prev_controls = self.controls
        value = controls()
        for page in value.keys():
            for key, val in UNIVERSAL_CONTROLS.items():
                value[page][key] = val
        self.controls = value

    """The app uses controls given as dicts that typically house functions
        The KEYS dictionary can be used to fetch keypad keys that are not printable
        The workaround used for this is taking the .__repr__ of the chr to identify keypad presses"""
    def page_control_logic(self)->dict:
        control_logic = {
        'intro':{' ':[self.select_screen, {'screen':'mode'}]},
        'mode':{'a':[self.init_discover_mode, {'app_mode':'Actor'}], 'A':[self.init_discover_mode, {'app_mode':'Actor'}], 'm':[self.init_discover_mode, {'app_mode':'Movie'}], 'M':[self.init_discover_mode, {'app_mode':'Movie'}], 't':[self.init_discover_mode, {'app_mode':'TV'}], 'T':[self.init_discover_mode, {'app_mode':'TV'}] },
        'results':{KEYS['bs']:[self.previous_screen], KEYS['left']:[self.prev_result], KEYS['right']:[self.next_result]},
        'discover':{KEYS['bs']:[self.select_screen,{'screen':'mode'}],KEYS['esc']:[self.select_screen,{'screen':'mode'}], 'g':[self.change_controls, {'controls':self.genre_control_logic}], KEYS['enter']:[self.build_result_page]}
        } 
        return control_logic
    
    def genre_control_logic(self)->dict:
        genre_control = {'discover':{']':[self.ui.increment_menu, {'menu_title':'Genres'}], '[':[self.ui.decrement_menu, {'menu_title':'Genres'}],KEYS['bs']:[self.change_controls, {'controls':self.page_control_logic}], ' ':[self.discover_add_to_api, {'menu_name':'Genres'}]}}
        return genre_control

    #Used to export Menu UIElement seletions into the API
    def discover_add_to_api(self, menu_name, join_logic='|'):
        housing = []
        menu = self.ui.get_uimenu_by_title(menu_name)
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
        self.ui.active_page.content[3] = Menu('Result', self.api.params)

        #Change to the query mode which builds the user inputs into API requests
    def init_discover_mode(self, app_mode):
        self.app_mode = app_mode
        self.api.mode = '/discover'
        match app_mode:
            case "TV":
                self.api.format = '/tv'
            case "Movie":
                self.api.format = '/movie'
            case "Actor":
                self.api.mode = '/search'
                self.api.format = '/person'
        #Apply the top banner title
        self.ui.set_content('discover', 0, Title(app_mode, BLACK_7))
        #Convert the dictionary into a list menu - using only Keys
        if self.app_mode != 'Actor':
            #Build genres menu of content
            self.ui.set_content('discover', 1, Menu('Genres',self.genres[app_mode]['name_to_id'],display='key'))
            self.ui.set_content('discover', 2, Menu('Search Params', self.api._PARAMS[self.api.mode][self.api.format], display='key'))
            self.ui.set_content('discover', 5, 'Controls')
            self.ui.set_x_start('discover', 2, 1, 2, 3, 4)
        self.select_screen('discover')

    def attach_string_input(self, input):
        self.api.params['query'] = input

    def get_user_string(self):
        self.ui.active_page.sections[self.ui.active_page.input[0]].nodelay(False)
        curses.echo(True)
        input = self.getstr(*self.ui.active_page.input[1:]).decode('utf-8')
        self.attach_string_input(input)

    def build_against_api(self):
        self.api_results = self.api.run_cycle()['results']
        if len(self.api_results) == 0:
            self.api_results = ['No Results Found']
        self.api.dump_data(CACHE_FILE, self.api_results)

    def build_result_page(self):
        self.change_controls(self.page_control_logic)
        self.build_against_api()
        if self.api_results == ['No Results Found']:
            self.ui.set_content('results', 0, Title('Oh Dear', TINY))
            self.ui.set_content('results', 1, Title('Nothing found - press \'r\' to retry configs'))
        else:

            result = ResultRender(self.api_results, self.app_mode, self.ui.t_height, self.ui.t_width//2)
            if not hasattr(self.ui, 'results'):
                self.results:ResultRender = result
            self.ui.set_content('results', 0, result.render())
            self.ui.set_content('results', 1, UIImage(result.image_data))
        self.select_screen('results')
        
    
    def cycle(self):
        self.ui.render()
        if len(self.ui.threads) == 0:
            self.ui.thread_task(self.ui.decorate_window)
        name = self.ui.active_page.name
        input = -1
        while input == -1:
            input = self.ui.get_keypress()
            if input not in self.controls[name]:
                self.ui.active_page.content[0] = input
                self.ui.render()
                input = -1
        data = self.controls[name][input]
        if len(data) > 1:
            data[0](**data[1])
        else:
            data[0]()
        self.ui.get_input()
        return self.cycle()


def run():
    tv = TVPickle()

run()