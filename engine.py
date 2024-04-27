from utils import *
import curses
from ui import UIEngine

#The entire API is essentially string manipulation as requests are URLS.
#The concept will be to greate a class that captures these requests to intepreate the JSON responses efficiently
#By Caching results we can traverse without the need for excessive recalls.
#THere could be fun potential in trying to combine criteria - i.e movies with both A and B directed by C etc...
#There will at times be large amounts of pages and many results.

#Engine that holds together moving between modes and selection
class TVPickle:
    _startup = True
    _clear_screen = True
    _show_config = False
    _compileSearch = False

    def __init__(self) -> None:
        super().__init__()
        self.input = "" #Stores the last asked input
        self.page = 0 #Reference to the correct menu
        self.history = ["" for i in range(10)] #Create 10 blank strings to store history
        self.history_ptr = 0
        self.mode = "M" #Specify either TV or Movie search
        self.key = None
        self.run()

    def run(self):
        while True:
            self.input = input("")
            if self._startup: self.setMode(self.input)
            if self._compileSearch: self.compileSearch(self.input)
            print(self.criteria)

    def setMode(self, mode):
        if mode not in MENU_DATA['mode']:
            print("Invalid choice. Try again.")
            mode = input(": ")
            self.setMode(mode)
        else:
            self.mode = mode
            self._startup = False
            self.page += 1

    def saveSearch(self, input):
        if self.history_ptr < 10:
            self.history[self.history_ptr] = input
        else:
            self.history_ptr = 0

    def setKey(self, key):
        self.key = self.criteria.get(key)

    def _nextPage(self):
        self.page += 1
    
    def _prevPage(self):
        self.page -= 1
