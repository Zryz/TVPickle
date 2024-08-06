from typing import Dict, List, Any
from random import randint
from time import sleep
from PIL import Image
from ui.common.curses_tools import XTERMCOLOURS

from .elements.page import Page
from .elements.uiimage import UIImage

import curses, threading, math

#Pages house the indivual elements and contain a header, body and footer section.
#The order of render is determine by their order of appearance in the list from 0th to -1th.

#The window class purely handles rendering of a window.
#The content a window contains is housed at the Page level.
#User input is handled further down by the UIEngine that controls the pages.
####### Build curses windows as pages ##########
####### UI ELEMENTS ########


class UIEngine:
    page_data = {}

    def __init__(self) -> None:
        curses.wrapper(self.init_stdsrn)
        #self.pages: Dict [str, Page] = {}
        self.active_page: Page = None #The currently active Page instance

        self.stop_event = threading.Event()
        self.threads:List[threading.Thread] = []
        self.lock = threading.Lock()

        self.render_stack:List[curses.window] = []
        self.delay_time = 0 #We dynamically set a sleep timer of curses.napms threaded tasks to prevent constant 100% while loop cycle
        
    def init_stdsrn(self, stdsrn:curses.window):
        self.stdsrn = stdsrn
        self.t_height, self.t_width = self.stdsrn.getmaxyx()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    
    def resize_windows(self):
        curses.endwin()
        self.stdsrn.refresh()
        self.stdsrn.clear()
        self.t_height, self.t_width = self.stdsrn.getmaxyx()
        self.update_page_dimensions(self.t_width, self.t_width)

    """Ecludian distance away from each element of RGB"""
    def color_distance(self, c1, c2):
        return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)
    
        # Find the nearest color in the predefined collection
    def find_nearest_color(self, target_color):
        nearest_index = min(range(len(XTERMCOLOURS)), key=lambda i: self.color_distance(target_color,XTERMCOLOURS[i]))
        return nearest_index+1
            
    def set_content(self, window_idx, content):
        self.active_page.content[window_idx] = content
        
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
        self.active_page = instance

    def select_page(self, name:str):
        if name not in self.pages:
            print('page' + name + 'not found')
            return
        self.active_page = self.pages[name]
    
    def get_x_start(self, *windows_idx):
        return {x:self.x_start[x] for x in windows_idx}
        
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
            for window in self.decorative:
                y, x = window.getmaxyx()
                if y == 2 and x == 1:
                    return
                y_rand = [randint(0,y-2) for _ in range(10)]
                x_rand = [randint(0,x-1) for _ in range(10)]
                #For improved efficiency we apply 10 x and y co-ordinates at once per window call
                for _ in range(len(y_rand)):
                    window.addch(y_rand[_], x_rand[_], self.gen_random_char(), curses.color_pair(1))
                window.noutrefresh()
                curses.doupdate()
                sleep(0.001)
            curses.napms(self.delay_time)

    def set_input_window(self, name, window_idx, y_start, x_start):
        self.pages[name].input = [window_idx, y_start, x_start]

    def get_keypress(self, key=-1):
        curses.noecho()
        while key == -1:
            self.sections[0].keypad(True)
            key = self.sections[0].getch()
        return chr(key).__repr__().replace("'", '')
    
    def get_input(self):
        window = curses.newwin(5,10,40,40)
        window.nodelay(False)
        window.keypad(True)
        window.border()
        curses.echo()
        input = window.getstr(self.t_height//4, 0)
        return input.decode('utf-8')

    def remove_page(self, name):
        if name not in self.pages:
            print("Page not found!")
            return
        self.pages.pop(name)
        print("page removed")

    #Refresh all windows within a page - useful for changing pages
    def refresh(self):
        for window in self.sections + self.decorative:
            window.clear()
            window.noutrefresh()

    def render(self):
        self.delay_time = b_size = 0    
        self.refresh()
        for _ in range(len(self.sections)):
            window = self.sections[_]
            if self.b_size[_] > 0:
                b_size = self.attach_border(window, self.b_size[_])
            if isinstance(self.content[_], UIImage):
                self.image_to_pallet(window,self.content[_])
            elif self.content[_]:
                self.attach_content(window, self.content[_], b_size, self.x_start[_])
            window.noutrefresh()
        curses.doupdate()
        self.delay_time = 10
