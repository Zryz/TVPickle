from pathlib import Path
from ui import Menu, Banner, Title

API_KEY = 'ba11c5aff22acaf0909a2e054360c25c'
BASE_URL = 'https://api.themoviedb.org/3/'
CORE_DATA = ['title', 'release_date', 'vote_average', 'genre_ids']
STACK_LIMIT = 30

#API CACHE LOCATIONS
api_cache = Path('./cache/search_history.json')
api_genres = Path('./cache/genres.json')

#HELPER FUNCTIONS

def isiter(l)-> bool:
    try:
        iter(l)
        return True
    except TypeError:
        return False
    

#GUI TEXT ELEMENTS
#UI Elements are provided as a 2D dictionary.
#pageName acts as the primary key.
#section acts as the secondary key.
#From here you specify the content to be rendered
#For elements that need 'Bannerising' you add them into the BANNER_MAP

#Defines all the pages and modes within the app
PROGRAM_PAGES = ('modePage', 'searchPage', 'resultsPage', 'configPage')

#UIElement arguments
UI_KARGS = {
    'coreElements':{
        'footer':{'menuData':{'end':''}},
    }
}

#Specify the Menu options for the pages of the app.
MENU_DATA = {
    'dictName':'menuData',
    'coreElements':{
    'footer':{'Q!':'Quit', 'R!':'Reset'}
        },
    'modePage':{
        'body':{'M':'Movie','T':'TV'}
        },
    'searchPage':{
        'body':{'A:':'Actor', 'G:':'Genre','Y:':'Year','D:':'Description','R:':'Rating'}
        },
    'resultsPage':{
        'header':{'+':'Next Page','-':'Previous Page'}}       
}

#Define the text used within any UITitle elements
TITLE_DATA = {
    'dictName':'titleData',
    'coreElements':{
        'header':'TV Pickle'
    },          
    'modePage':{
        'header':'TV Mode Selection',
        'page':'Please choose a mode to search for content.\n. Use M: for Movies or T: for TV.'
    },
    'searchPage':{
        'header':'Search Mode Page',
        'page':'Please enter criteria to use for searching against.'
    },
    'resultsPage':{
        'header':'Search Results'
    }
}

#Define what UI Elements need to be represented as a Banner
BANNER_MAP = {
    'dictName':'bannerMap',
    'coreElements':{
        'header':'UITitle',
        'footer':'UIMenu'
        },
    'modePage':{
        'header':'UITitle',
        },
    'searchPage':{
        'header':{'UIBanner':'UITitle'},
        'body':['UITitle', 'UIMenu']
        }
}

