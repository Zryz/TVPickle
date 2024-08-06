import curses, os

from ..elements.uielement import Menu, Title, Text
from ..elements.uiimage import UIImage


UI_ELEMENTS = (Menu, Text, Title, UIImage)
#GUI CONFIG

UIELEMENT_LOOKUP = {
    'Menu': Menu,
    'Text': Text,
    'Title': Title
}

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

KEYS = {'bs':'ć', 'up':'ă', 'left':'Ą', 'right':'ą', 'down':'Ă', 'enter':'\\n', 'esc':'\x1b'}

DEFAULT_TEXT = {'end':'\n', 'prefix':'', 'indent':0, 'align':'l'}

VALID_TEXT_PROPERTIES = ['end', 'prefix', 'indent', 'align']

CURSES_ATTRIBUTES = {
    'underline':curses.A_UNDERLINE,
    'bold':curses.A_BOLD
}

EXCLUDED_CHARS = set('\n\r\t\b\x1b/{}()[]')