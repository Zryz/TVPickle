from .uielement import UIElement
from ..common.defs import TEXT_ALIGN

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

    def __add__(self, other):
        r = other
        if isinstance(other, str) and isinstance(self, Menu):
            r = ''
            for key, value in self.content.items():
                r+= key + ' : ' + value + ' '
            r + other
        elif isinstance(self.content, (Menu)) and isinstance(other, str):
            r = self.content.content + other
        return r

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

    def increment_menu(self, menu_title):
        for element in self.content:
            if isinstance(element, Menu):
                if element.title == menu_title:
                    element.increment_selected()

    def decrement_menu(self, menu_title):
        for element in self.content:
            if isinstance(element, Menu):
                if element.title == menu_title:
                    element.decrement_selected()

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
