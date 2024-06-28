from typing import Dict, List, Any
from random import randint
from math import ceil
from typing import Any
from time import sleep
from collections import namedtuple

import curses, threading, itertools, string, random

PageGenerator = namedtuple("PageGenerator", ['name', 'y_div', 'x_div', 'b_size'])

PROGRAM_WIDTH = 80
PROGRAM_HEIGHT = 80
PAGE_SECTIONS = ('header', 'body', 'footer')  # The breakdown of what a page is made up of
TEXT_ALIGN = {
    'center':str.center,
    'left':str.ljust,
    'right':str.rjust
            }
TEXT_FORMAT = {
    'cap':str.capitalize,
    'l':str.lower,
    'u':str.upper,
    't':str.title,
    'n':None
}

DEFAULT_TEXT = {'end':'\n', 'prefix':'', 'indent':0, 'align':'l'}
VALID_TEXT_PROPERTIES = ['end', 'prefix', 'indent', 'align']

CURSES_ATTRIBUTES = {
    'underline':curses.A_UNDERLINE,
    'bold':curses.A_BOLD
}

EXCLUDED_CHARS = set('\n\r\t\b\x1b/{}()[]')

"""  
  
o """

#Define the structure for custom fonts to be used as Title objects.
FONT_TEMPLATE = {'special_chars':"""""",'special':{' ':'   \n   ','.':"  \n▄ "},'numeric':{'default_width':0,'widths':{'0':0},'content':""},'upper':{'gap':0,'default_width':0, 'widths':{'Character Here':0},'content':""}}
BLOCK_ALPHABET = {'special_chars':""" .,'-()!?'""",'special':{' ':'   \n   ','.':"  \n▄ ",',':"  \n█ ",'-':"   \n▀▀ ",'(':'▄▀ \n▀▄ ',')':'▀▄ \n▄▀ ','!':'█ \n▄ ','?':'▄▀▄ \n ▄▀ '},'numeric':{'gap':1,'default_width':2,'widths':{'0':3, '3':3, '8':3},'content':"█▀█ ▄█ ▀█ ▀██ █▄ █▄ █▀ ▀█ █▄█ █\n█▄█  █ █▄ ▄▄█  █ ▄█ ██  █ █▄█ ▄█"},'upper':{'gap':1,'default_width':3, 'widths':{'I': 1,'F':2, 'N':4, 'M':5, 'W':5},'content':"▄▀▄ ██▄ ▄▀▀ █▀▄ ██▀ █▀ ▄▀  █▄█ █   █ █▄▀ █   █▄ ▄█ █▄ █ ▄▀▄ █▀▄ ▄▀▄ █▀▄ ▄▀▀ ▀█▀ █ █ █ █ █   █ ▀▄▀ ▀▄▀ ▀█\n█▀█ █▄█ ▀▄▄ █▄▀ █▄▄ █▀ ▀▄█ █ █ █ ▀▄█ █ █ █▄▄ █ ▀ █ █ ▀█ ▀▄▀ █▀  ▀▄█ █▀▄ ▄██  █  ▀▄█ ▀▄▀ ▀▄▀▄▀ █ █  █  █▄▄"}}

BLACK_7 = {'special_chars':""" .,?!()""",'special':{' ':'    \n    \n    \n    \n    \n    ', '.':'   \n   \n   \n   \n██╗\n╚═╝'},'upper':{'gap':0,'default_width':8, 'widths':{'I':3,'G':9,'M':11,'N':10,'O':9,'Q':9,'T':9,'U':9,'V':9,'W':10,'Y':9},'content':" █████╗ ██████╗  ██████╗██████╗ ███████╗███████╗ ██████╗ ██╗  ██╗██╗     ██╗██╗  ██╗██╗     ███╗   ███╗███╗   ██╗ ██████╗ ██████╗  ██████╗ ██████╗ ███████╗████████╗██╗   ██╗██╗   ██╗██╗    ██╗██╗  ██╗██╗   ██╗███████╗\n██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝ ██║  ██║██║     ██║██║ ██╔╝██║     ████╗ ████║████╗  ██║██╔═══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██║   ██║██║   ██║██║    ██║╚██╗██╔╝╚██╗ ██╔╝╚══███╔╝\n███████║██████╔╝██║     ██║  ██║█████╗  █████╗  ██║  ███╗███████║██║     ██║█████╔╝ ██║     ██╔████╔██║██╔██╗ ██║██║   ██║██████╔╝██║   ██║██████╔╝███████╗   ██║   ██║   ██║██║   ██║██║ █╗ ██║ ╚███╔╝  ╚████╔╝   ███╔╝ \n██╔══██║██╔══██╗██║     ██║  ██║██╔══╝  ██╔══╝  ██║   ██║██╔══██║██║██   ██║██╔═██╗ ██║     ██║╚██╔╝██║██║╚██╗██║██║   ██║██╔═══╝ ██║▄▄ ██║██╔══██╗╚════██║   ██║   ██║   ██║╚██╗ ██╔╝██║███╗██║ ██╔██╗   ╚██╔╝   ███╔╝  \n██║  ██║██████╔╝╚██████╗██████╔╝███████╗██║     ╚██████╔╝██║  ██║██║╚█████╔╝██║  ██╗███████╗██║ ╚═╝ ██║██║ ╚████║╚██████╔╝██║     ╚██████╔╝██║  ██║███████║   ██║   ╚██████╔╝ ╚████╔╝ ╚███╔███╔╝██╔╝ ██╗   ██║   ███████╗\n╚═╝  ╚═╝╚═════╝  ╚═════╝╚═════╝ ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝      ╚══▀▀═╝ ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝   ╚═══╝   ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝"},'numeric':""}

TINY = {'special_chars':""" .,'?""",'special':{' ':'  \n  \n  ','.':"  \n  \no ",',':'  \n  \n/ ',"'":'/ \n  \n  ','?':'_ \n )\no '},'numeric':{'gap':1,'default_width':4,'widths':{'1':2, '2':3, '3':3, '5':3, '7':3},'content':"  __     __  __        __  __  ___  __   __  \n /  \ /|  _)  _) |__| |_  /__    / (__) (__\ \n \__/  | /__ __)    | __) \__)  /  (__)  __/ "}, 'upper':{'gap':0,'default_width':4, 'widths':{'C':3,'E':3,'F':3,'I':1,'J':2,'L':3,'S':3,'T':3,'X':2,'Y':3,'Z':3}, 'content':"     __  __ __  __ __ __                        __  __  __  __  _____                 ___\n /\ |__)/  |  \|_ |_ / _ |__||  ||_/|  |\/||\ |/  \|__)/  \|__)(_  | /  \\\\  /|  |\/\_/ _/\n/--\|__)\__|__/|__|  \__)|  ||(_)| \|__|  || \|\__/|   \_\/| \ __) | \__/ \/ |/\|/\ | /__"},'lower':{'gap':0,'default_width':3, 'widths':{'f':2,'i':1,'j':1,'k':2,'l':1,'r':2,'s':2,'t':2,'v':2,'w':4,'x':2,'y':2,'z':2},'content':"                _                                               \n _ |_  _  _| _ (_ _ |_ oo| | _  _  _  _  _  _ _|_             _ \n(_||_)(_ (_|(-`| (_)| )|||<||||| )(_)|_)(_|| _)|_|_|\/\/\/><\//_\n                 _/     /            |    |                 /   "}}
#Pages house the indivual elements and contain a header, body and footer section.
#The order of render is determine by their order of appearance in the list from 0th to -1th.

#The window class purely handles rendering of a window.
#The content a window contains is housed at the Page level.
#User input is handled further down by the UIEngine that controls the pages.
####### Build curses windows as pages ##########
class Page:
    def __init__(self, t_height, t_width, name, y_div:List[float], x_div:List[float], b_size:List[int]=[], b_char='-', start_y=0, start_x=0) -> None:
        if sum(y_div) != 1.0:
            raise ValueError("Invalid y_div - confirm totals 1.0 and number of sections set")
        self.name = name
        self.sections: List[curses.window] = [] #Houses curses.window instances
        self.decorative: List[curses.window] = [] #None graphically changing windows (to make content changes more efficient)
        #Establish the number of y divisions
        y_divisions = self.distribute_windows(y_div, t_height)
        #Create page windows from top to bottom
        i = 0
        for _ in range(len(y_div)):
        #Determine if we are splitting the current y_division along its x axis
            if x_div[_] != None:
                windows = self.x_split_window(y_divisions[_], t_width, x_div[_], start_y)
                for q in range(len(windows)):
                    if b_size[q+i] == 0:
                        self.decorative.append(windows[q])
                    else:
                        self.sections.append(windows[q])
                i += len(windows)
        #Otherwise we make a fully extended window
            else:
                window = curses.newwin(y_divisions[_], t_width, start_y, start_x)
                self.fill_window(window)
                if b_size[i] == 0:
                    self.decorative.append(window)
                else:
                    self.sections.append(window)
                i+=1
            print(_)
            start_y += y_divisions[_]
            

        #Define content placeholders for windows
        self.content = [None for _ in range(len(self.sections))]
        #Allow an x-based pad on content to inset it into a window
        self.x_start = [0 for _ in range(len(self.sections))]
        self.input = [-1, 0, 0] #Define what window is to be used for text based input and y_start, x_start co-ordinates
        self.blocked = [] #Specify window index of bordless windows to not decorate i.e create blank windows.

        #Tuple house the original instantiation stats for later recalling if terminal resized and rendering
        self.page_stats = (name, y_div, x_div, b_size, b_char, start_y, start_x)
        
        self.b_size:List[int] = [x for x in b_size if x != 0]
        self.b_char = b_char
         
    def clear(self):
        for window in self.sections:
            window.clear()

    def refresh(self, window:curses.window=None):
        if window != None:
            window.noutrefresh()
        else:
            for element in self.sections:
                element.noutrefresh()
        curses.doupdate()

    #Pad out windows with initial " " post creation so that they always render fully
    def fill_window(self, window:curses.window, char=' '):
        height, width = window.getmaxyx()
        v = char == 'Magic'
        for line in range(height-1):
            for col in range(width):
                if v: char = self.gen_random_char()
                window.addch(line, col, char)

     #Divmod divide the sizes of the windows based on percentages set in y_div
    def distribute_windows(self, x_y_div, span)-> List[int]:
        z = []
        #Divmod and generate [size, remainder] pairs
        for scale in x_y_div:
            size, remainder = divmod(span*scale, 1.0)
            z.append([int(size),remainder])

        #Sum the total of the remainders (will always reach a whole number)
        z[len(x_y_div)//2][0] += int(sum([val[1] for val in z]))  
        
        #Return the line breakdown of window heights summing to y result of self.getmaxyx()
        return [val[0] for val in z]

    #If we are dividing pages into widths we create a list of windows.
    def x_split_window(self, height, width, x_div, y_start):
        window_widths = self.distribute_windows(x_div, width)
        housing, x_start = [], 0
        for l in range(len(x_div)):
            window = curses.newwin(height, window_widths[l], y_start, x_start)
            self.fill_window(window)
            x_start += window_widths[l]
            housing.append(window)
        return housing

    def set_input(self,index, y_start, x_start):
        self.input = [index, (y_start, x_start)]
    
    def attach_border(self, window:curses.window, b_size:int):
        height, width = window.getmaxyx()
        while height <= (b_size*2):
            b_size -= 1
        border = self.b_char * width
        for _ in range(b_size):
            window.addstr(_,0,border)
        for _ in range(height-b_size-1, height-1):
            window.addstr(_,0,border)
        return b_size

    """Attach content housed in self.content to the window
    Content can be given either as a string or as a list.
    When given as a list they will be joined by \ n to create new lines
    """
    def attach_content(self, window:curses.window, content:Any, b_size:int=None, x_start:int=0):
        height, width = window.getmaxyx()
        offset, content_height = 0, 0
        if isinstance(content, UI_ELEMENTS):
            content.width = width
            if isinstance(content, Title):
                for element in content.content:
                    if element.get('ascii'):
                        content_height += len(element['ascii'][0])
                    else:
                        content_height += len(element['string'])
                offset += (((height - (b_size*2))-content_height) // 2)
            if isinstance(content, Menu):
                offset = 0
            content = content.render()
        if isinstance(content, list):
            content = "\n".join(content)

        if (b_size + offset) < 0:   
                offset = -b_size

        i, x = 0 , 0 + x_start
        line = b_size + offset
        height = height - b_size
        while line < height and i < len(content):
            if content[i] == '\n':
                line+=1
                x = 0 + x_start
                i+=1
                continue
            elif x == width-2:
                while i < len(content) and content[i] != '\n':
                    i+=1
                continue
            try:
                window.addstr(line, x, content[i])
            except curses.error as e:
                print(line, x, height, width, offset)
            x += 1
            i += 1
            window.noutrefresh()

    #Return window instances that do not have a border and are not blocked from decoration
    def get_decorate_windows(self):
        return [self.sections[_] for _ in range(len(self.sections)) if self.b_size[_] > 0]
    

####### UI ELEMENTS ########

class UIElement():
    def __init_subclass__(cls, UIName, **kargs) -> None:
        cls.UIName = UIName
        super().__init_subclass__(**kargs)

    def __init__(self, content) -> None:
        self.content = content

    def __call__(self):
        return self.render()
    
    def __repr__(self) -> str:
        return self.render()

    def __add__(self, other):
        r = other
        if isinstance(other, str) and isinstance(self, Menu):
            r = ''
            for key, value in self.content.items():
                r+= key + ' : ' + value + ' '
            r + other
        elif isinstance(other, str) and isinstance(self, Text):
            r = self.content + other
        elif isinstance(other, str):
            if isinstance(self.content, (Text, Menu)) and isinstance(other, str):
                r = self.content.content + other
        return r

    @classmethod
    def create(cls, UIName, name, content):
        return UIELEMENT_LOOKUP[UIName](name, content)
    
    def update(self, contents):
        while  isinstance(self.content, UIElement):
            self = self.content
        self.content = contents

    def render(self):
        raise NotImplementedError('uielement: render() method required by uielements')

#UIElements
# Universal Elements
# Name: Instance Name, UIName: What form of UI, Section: Where does this show?, 

#Menu classes help to handle dictionarys / json key value pairings to make the interactable and render them
class Menu(UIElement, UIName='Menu'):
    selected = None
    def __init__(self, title, content:dict, align='left', end="\n", display='all'):
        self.values = [x for x in content.values()]
        self.title = title
        self.end = end
        self.display = display
        self.align = align
        self.selected = -1 #Used to choose a menu item
        super().__init__(content)

    def set_select(self, input=None):
        if input != None:
            if isinstance(input, int):
                if input > -1 and len(self.content) > 0 and input-1 < len(self.content):
                    self.selected = input

    def reset_selected(self):
        self.selected = None

    def increment_selected(self):
        if self.selected < len(self.values)-1:
            self.selected += 1

    def decrement_selected(self):
        if self.selected > 0:
            self.selected -= 1

    def get_selected_value(self):
        return self.values[self.selected]

    def render(self) -> str:
        #Like all UIElements classes they will receieve a self.width attribute at point of render by curses stdsrn to help apply string centre
        r, func = '', TEXT_ALIGN[self.align]
        r += self.title + '\n\n'
        for idx, val in enumerate(self.content.items()):
                if self.selected == idx:
                    r += '* '
                else: r += '  '
                if self.display == 'key': r += val[0]
                elif self.display == 'value': r += val[1]
                else: r += val[0] + ': ' + val[1]
                r += self.end
        return r

#Titles are always centered with the option to feed in a font format.
#Useful for banners and headings in pages
class Title(UIElement, UIName='Title'):
    def __init__(self, content:str, font_source=None) -> None:
        self.source = font_source
        if font_source != None:
            #if len(content) == 1:
            #    content = UIEngine.generate_ascii_letter(content, font_source)
            #else:
            #    self.build_word = True
            #content = [UIEngine.generate_ascii_letter(x, font_source) for x in content]
            content = [{'ascii':[UIEngine.generate_ascii_letter(x, font_source) for x in content]}] #'source':font_source}]
        else:
            content = [{'string':content.split('\n')}]
        super().__init__(content)

    def __repr__(self):
        return self.render()
    
    def __add__(self, other):
        if isinstance(other, Title):
            for x in other.content:
                self.content.append(x)
        elif isinstance(other, str):
            self.content.append({'string':other.split('\n')})
        return self

    def __radd__(self, other):
        if isinstance(other, Title):
            for _ in range(len(other.content)-1, -1, -1):
                self.content.insert(0, other.content[_])
            return self
        elif isinstance(other, str):
            self.content.insert(0, {'string':other.split('\n')})
            return self

    #Content is housed as lists of strings that represent new lines.
    def render(self)->str:
        result = []
        for content in self.content:
            if content.get('ascii'):
                #print(content['ascii'])
                #We have to generate ASCII art as part of the render process
                #Create a holder for each line of the block art
                maximum_height = max([len(i) for i in content['ascii']])
                build_lines = ["" for _ in range(maximum_height)]
                for letter in content['ascii']:
                    holder = ["" for _ in range(len(letter))]
                    for _ in range(len(letter)):
                        holder[_] += letter[_]
                    #Capital letters may have different heights to lower case,
                    #For this we need to ammend the difference - usually due to hanging letters g, y etc.
                    while len(holder) < maximum_height:
                        holder.append(" "*len(holder[0]))
                    for a in range(len(holder)):
                        build_lines[a] += holder[a]
                                
                #Center the content to fit the page
                centered = [x.center(self.width-1) for x in build_lines]
                result.append('\n'.join(centered))
            elif content.get('string'):
                result.append('\n'.join([x.center(self.width-1) for x in content['string']]))

        return result

class Text(UIElement, UIName='Text'):
    def __init__(self, content):
        raise RuntimeError("Use Text.new() to create a text object")
    
    #To enforce the creation of a correct Text (as it must be a string)
    @classmethod
    def _priv_init(cls, content, **kargs) -> None:
        instance = super().__new__(cls)
        instance.properties = {'end':kargs['end'], 'prefix':kargs['prefix'], 'indent':kargs['indent'], 'align':kargs['align']}
        super().__init__(instance, content)
        return instance

    @classmethod
    def new(cls, content, **kargs):
        if not isinstance(content, str):
            print('text: text type not str')
            return None
        test = cls.validate(**kargs)
        if not test:
            print('text: incomplete kargs - setting missing to defaults')
            for key in DEFAULT_TEXT.keys():
                if not kargs.get(key):
                    kargs[key] = DEFAULT_TEXT[key]
        return cls._priv_init(content, **kargs)

    @staticmethod
    def validate(**test:dict) -> bool:
        for key in DEFAULT_TEXT.keys():
            if key not in test:
                return False
        return True

    def render(self)-> str:
        return self.content.center(self.dimensions[0])

UI_ELEMENTS = (Menu, Text, Title)
#GUI CONFIG
UIELEMENT_LOOKUP = {
    'Menu': Menu,
    'Text': Text,
    'Title': Title
}

class UIEngine:
    FAST_UI = 1
    def __init__(self) -> None:
        curses.wrapper(self.init_stdsrn)
        self.pages: Dict [str, Page] = {}
        self.current_page: Page = None #Stores the currently active page instance
        #self.decorate = True #Animates borderless windows with a matrix like animation
        self.stop_event = threading.Event()
        self.threads:List[threading.Thread] = []
        self.lock = threading.Lock()
        self.render_stack:List[curses.window] = []
        self.delay_time = 0 #We dynamically set a sleep timer of curses.napms threaded tasks to prevent constant 100% while loop cycle
        
    def init_stdsrn(self, stdsrn:curses.window):
        self.stdsrn = stdsrn
        self.t_height, self.t_width = self.stdsrn.getmaxyx()
        self.init_colors()
    
    def resize_windows(self):
        curses.endwin()
        self.stdsrn.refresh()
        self.stdsrn.clear()
        self.t_height, self.t_width = self.stdsrn.getmaxyx()
        self.update_page_dimensions(self.t_width, self.t_width)

    def init_colors(self):
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_WHITE)
    
    def set_content(self, page_name, window_idx, content):
        self.pages[page_name].content[window_idx] = content

    def update_page_dimensions(self, t_height, t_width):
        for page in self.pages.values():
            vals = page.page_stats
            self.pages[page.name] = Page(t_height, t_width, *vals)

    def set_x_start(self, name, val, *window_idxs):
        page = self.pages[name]
        for number in window_idxs:
            page.x_start[number] = val

    def print_menu(self, value:dict, line=False, content:str=None):
        r = ""
        for key, val in value.items():
            if not content: r += key + " : " + val
            if content.lower() == "key": r += key
            if content.lower() == "value": r+= val
            if line: r+= '\n'
            else: r += ' || '
        return r
    
    def create_page(self, *args):
        instance = Page(self.t_height, self.t_width, *args)
        self.pages[instance.name] = instance
        if self.current_page is None:
            self.current_page = instance

    def select_page(self, name:str):
        if name not in self.pages:
            print('page' + name + 'not found')
            return
        self.current_page = self.pages[name]
    
    @staticmethod
    def gen_random_char()->chr:
        val = randint(32, 115)
        while val > 126 and val < 160:
            val = randint(32, 300)
        if val % 5 == 0 or val % 2 == 0 or chr(val) in EXCLUDED_CHARS: 
            char = ' '
        else:
            char = chr(val)
        return char
    
    #Font typically have a common width, defined as default_width - outliers can be defined within the 'widths' indivdually. 
    @staticmethod
    def get_ascii_width(char, source):
        if char not in source['widths']: width = source['default_width']
        else: width = source['widths'][char]
        return width

    #Special = Returned directly
    #Numeric = Generated (due to complexities of layers)
    #Alpha = Determine whether font supports given case and select correct library
    @staticmethod
    def generate_ascii_letter(char:str, source:str=None)->list:
        if not source: return char #Immediately return the text if no font source provided
        char_lower = char.islower()
        has_lower = source.get('lower')
        #Determine what type of character to generate - if not supported return the original char
        if char in source['special_chars']:
            return source['special'][char].split('\n') # Specials can be directly relayed as they are housed pre-built
        elif char.isdigit():
            library = 'numeric'
        elif char.isalpha():
            #If the character is a lowercase and the library doesn't support it - change both character and set library to upper
            if not has_lower and char_lower: 
                char = char.upper()
                library = 'upper'
            #If the character is uppercase all fonts have uppercase
            elif not char_lower:
                library = 'upper'
            #Else use the lowercase library since supported and character's format
            else:
                library = 'lower'
        else:
            #To get here content has been given that is unsupported - special character space will be used to plug a gap
            print('Unsupported character for given source - space character returned')
            return source['special'][' '].split('\n')
        #Setup which content library to use -
    
        ascii_height = source[library]['content'].count('\n')+1
        width = UIEngine.get_ascii_width(char, source[library])
        if library == 'upper':
            content_index = sum([UIEngine.get_ascii_width(chr(x), source[library])+source[library]['gap'] for x in range(65,ord(char))])
        elif library == 'lower':
            content_index = sum([UIEngine.get_ascii_width(chr(x), source[library])+source[library]['gap'] for x in range(97,ord(char))])
        else:
            content_index = sum([UIEngine.get_ascii_width(chr(x), source[library])+source[library]['gap'] for x in range(48,ord(char))])
        
        total_width = source[library]['content'].index('\n')+1
        
        r = []
        for i in range(content_index,(total_width)*ascii_height, total_width):
            r.append(source[library]['content'][i:i+width]+' '*source[library]['gap'])
        return r

    @staticmethod
    def generate_ascii_gap(source, size, height):
        r = []
        for _ in range(height):
            for _ in range(size):
                r.append(' '*size)
        return r
    
    def get_x_start(self, *windows_idx):
        return {x:self.current_page.x_start[x] for x in windows_idx}
        
    def block_decorate(self, page_name, *idxs):
        if page_name not in self.pages:
            return
        blocked = self.pages[page_name].blocked
        for index in idxs:
            if index not in blocked:
                blocked.append(index)

    def unblock_decorate(self, name, *idxs):
        if name not in self.pages:
            return
        blocked = self.pages[name].blocked
        for index in idxs:
            if index in blocked:
                blocked.remove(index)

    def pause_decorate(self):
        self.stop_event.set()

    def start_decorate(self):
        self.stop_event.clear()

    def init_decorate(self):
        self.thread_task(self.decorate_window)

    def get_menu_by_name(self, name)-> Menu:
        for element in self.current_page.content:
            if isinstance(element, Menu):
                if element.title == name:
                    return element

    def increment_menu(self, menu_name):
        for element in self.current_page.content:
            if isinstance(element, Menu):
                if element.title == menu_name:
                    element.increment_selected()

    def decrement_menu(self, menu_name):
        for element in self.current_page.content:
            if isinstance(element, Menu):
                if element.title == menu_name:
                    element.decrement_selected()

    def thread_task(self, task, *args):
        thread = threading.Thread(target=task, args=(args), daemon=True)
        thread.start()
        self.stop_event.clear()
        self.threads.append(thread)

    def pop_threads(self):
        if len(self.threads) > 0:
            return self.threads.pop()

    def stop_thread(self):
        thread = self.pop_threads()
        if thread:
            self.stop_event.set()
            thread.join()

    def decorate_window(self):  
        while not self.stop_event.is_set():
            for window in self.current_page.decorative:
                y, x = window.getmaxyx()
                if y == 2 and x == 1:
                    return
                y_rand = [randint(0,y-2) for _ in range(10)]
                x_rand = [randint(0,x-1) for _ in range(10)]
                #For improved efficiency we apply 10 x and y co-ordinates at once per window call
                for _ in range(len(y_rand)):
                    window.addch(y_rand[_], x_rand[_], self.gen_random_char(), curses.color_pair(2))
                window.noutrefresh()
                curses.doupdate()
                sleep(0.001)
            curses.napms(self.delay_time)

    def set_input_window(self, name, window_idx, y_start, x_start):
        self.pages[name].input = [window_idx, y_start, x_start]

    def get_keypress(self, key=-1):
        curses.noecho()
        while key == -1:
            key = self.current_page.sections[0].getch()
        return chr(key)
    
    def get_input(self, window:curses.window, y, x):
        curses.echo()
        input = window.getstr(y, x)
        return input.decode('utf-8')

    def remove_page(self, name):
        if name not in self.pages:
            print("Page not found!")
            return
        self.pages.pop(name)
        print("page removed")

    #Refresh all windows within a page - useful for changing pages
    def refresh(self):
        for window in self.current_page.sections + self.current_page.decorative:
            window.clear()
            window.noutrefresh()

    def partial_refresh(self):
        for window in self.render_stack:
            window.clear()
            window.noutrefresh()
        self.render_stack = []

    def render(self):
        self.delay_time = 0
        self.refresh()
        if len(self.render_stack) > 0:
            return self.partial_refresh()
        for _ in range(len(self.current_page.sections)):
            window = self.current_page.sections[_]
            window.nodelay(True)
            window.keypad(True)
            if self.current_page.b_size[_] > 0:
                b_size = self.current_page.attach_border(window, self.current_page.b_size[_])
            if self.current_page.content[_]:    
                self.current_page.attach_content(window, self.current_page.content[_], b_size, self.current_page.x_start[_])
            window.noutrefresh()
        curses.doupdate()
        self.delay_time = 10
