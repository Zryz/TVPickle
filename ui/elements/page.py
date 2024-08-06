from typing import List, Any
from typing import Any


import curses

class Page:
    def __init__(self, t_height, t_width, name, y_div:List[float], x_div:List[float], b_size:List[int]=[], b_char='-', start_y=0, start_x=0) -> None:
        #We handle floating precision issues by rounding (for e.g sum [.2,.7,.1] == .9999)
        if round(sum(y_div),1) != 1.0:
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
            start_y += y_divisions[_]
            
        #Define string content placeholders for windows
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
                window.addch(line, col, char, curses.color_pair(1))

     #Divmod divide the sizes of the windows based on percentages set in y_div
    def distribute_windows(self, divisions, span)-> List[int]:
        z = []
        #Divmod and generate [size, remainder] pairs
        for scale in divisions:
            size, remainder = divmod(span*scale, 1.0)
            z.append([int(size),remainder])

        #Sum the total of the remainders (will always reach a whole number) and apply to the centre sector len // 2
        z[len(divisions)//2][0] += int(sum([val[1] for val in z]))  
        
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
    
        
    def attach_border(self, window:curses.window, b_size:int):
        height, width = window.getmaxyx()
        while height <= (b_size*2):
            b_size -= 1
        border = self.b_char * width
        for _ in range(b_size):
            window.addstr(_,0,border, curses.color_pair(1))
        for _ in range(height-b_size-1, height-1):
            window.addstr(_,0,border, curses.color_pair(1))
        return b_size



    """Attach content housed in self.content to the window
    Content can be given either as a string or as a list.
    When given as a list they will be joined by \ n to create new lines
    """
    def attach_content(self, window:curses.window, content:Any, b_size:int, x_start:int=0, offset=0):
        height, width = window.getmaxyx()

        content, offset = self.format_content(content, width, height, b_size)

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
                window.addstr(line, x, content[i], curses.color_pair(1))
            except curses.error as e:
                print(line, x, height, width, offset)
            x += 1
            i += 1
            window.noutrefresh()

    #Return window instances that do not have a border and are not blocked from decoration
    def get_decorate_windows(self):
        return [self.sections[_] for _ in range(len(self.sections)) if self.b_size[_] > 0]
    