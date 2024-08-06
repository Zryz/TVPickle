from random import randint
from .defs import EXCLUDED_CHARS



def gen_random_char()->chr:
    val = randint(32, 115)
    while val > 126 and val < 160:
        val = randint(32, 300)
    if val % 5 == 0 or val % 2 == 0 or chr(val) in EXCLUDED_CHARS: 
        char = ' '
    else:
        char = chr(val)
    return char

