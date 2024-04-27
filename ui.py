import utils
import os

class UIEngine(object):
    def __init__(self) -> None:
        self.pagePtr = 0
        self.currentPage = utils.PROGRAM_PAGES[self.pagePtr]
        self.UIElements = [] #Initialised UIElements are housed in a complete list.
        self.menuData = utils.MENU_DATA
        self.titleData = utils.TITLE_DATA
        self.bannerMap = utils.BANNER_MAP
        self.kargs = utils.UI_KARGS
        print(self.parseUIData(self.menuData, self.titleData))
        print(self.UIElements)

    def parseUIData(self, *args):
        kargs = {}
        for dataMap in args:
            for pageName, pageElements in dataMap.items():
                if pageName == 'dictName':continue #We don't need this here.
                for section, content in pageElements.items():
                    if self.kargs.get(pageName):
                        if self.kargs[pageName].get(section):
                            print(dataMap['dictName'], self.kargs[pageName][section].keys())
                            if dataMap['dictName'] in self.kargs[pageName][section].keys():
                                print('hit')
                                kargs = self.kargs[pageName][section][dataMap['dictName']]
                    else:
                        kargs = {}
                    self.UIElements.append(UIELEMENT_LOOKUP[dataMap['dictName']](content,section,pageName,**kargs))

    def createUIElement(self, UIName, content, section, pageName, **kargs):
        element = UIELEMENT_LOOKUP[UIName](content, section, pageName)
        return element
    
    def parseBannerData(self):
        for pageName, pageElements in self.bannerMap.items():
            for section, UIElement in pageElements.items():
                pass

    def filterUIElements(self, pageName, section, UIName):
        pass
    
    def render(self):
        pass
    """ 
    def reduceKargsDict(self, dictionary:dict, tmp=None)-> list:
        if not tmp: tmp = {}
        if not isinstance(dictionary, dict): return print("Input not DICT!")
        for key, value in dictionary.items():
            tmp[key] = []
            if isinstance(value, dict):
                self.reduceDictLookup(value, tmp)
            elif isinstance(value, list):
                for item in value:
                    tmp.append(item)
            else:
                tmp.append(value)
        return tmp 
    """
    def add(self, page):
        if isinstance(page, Page):
            self.Pages
        
    def setConsoleHeight(self):
        print('\x1b[8;'+ str(self.height) + ';' + str(self.width)+ 't')

    def changeName(self, element:object, name):
        if hasattr(element, 'name'):
            element.name = name
        else:
            print('Cant change name for', element, 'It has no name attribute')
        
    def build(self):
        pass

#Pages are the meat of the UI - 
#Pages can house any variety of UIelements to render and defines the order they appear.
        
class Page():
    UIElements = {}
    def __init__(self, pageName, UIElement, indent=4) -> None:
        self.width = PROGRAM_WIDTH
        self.height = PROGRAM_WIDTH
        self.pageName = pageName
        self.render_order = PAGE_SECTIONS
        self.renderCoreElements = True
        self.element_id = 0
        self.isRendered = {x:True for x in PAGE_SECTIONS}
        self.clearScreen = True
        self.indent = ' ' * indent
        self.registerElement(UIElement)

    @classmethod
    def registerElement(cls, UIElement):
        if cls.UIElements.get(UIElement.pageName):
            #We need to remove nested UIElements from the page list to avoid them being double rendered
            if isinstance(UIElement.content, UI_ELEMENTS):
                cls.UIElements[UIElement.pageName].remove(UIElement.content)
            cls.UIElements[UIElement.pageName].append(UIElement)
        else:
            cls.UIElements[UIElement.pageName] = [UIElement]

    def add(self, section, element:object, **kargs):
        if utils.isiter(element):
            for l in element:
                self.add(section, l)
        if isinstance(element, UI_ELEMENTS):
            self.element_id +=1
            setattr(element, 'id', self.element_id)
        self.UIElements[element.name] = element
        for k,v in kargs.items():
            setattr(self.UIElements[element.name], k, v)

    def render(self):
        if self.clearScreen: os.system('cls' if os.name == 'nt' else 'clear')
        for section in self.render_order:
            if self.UIElements.get(section):
                self.UIElements[section].render()

class UIElement(Page):
    #elements = {} #When a UIElement is created we specify what page it belongs to
    def __init_subclass__(cls, UIName, **kargs) -> None:
        cls.UIName = UIName
        super().__init_subclass__(**kargs)

    def __init__(self, content, section, UIElement, pageName, end='\n') -> None:
        if not content:
            self.content = UIElement
        else:
            self.content = content
        self.end = end
        self.section = section
        self.pageName = pageName
        #self.registerElement(UIElement)
        super().__init__(pageName, UIElement)

    def __repr__(self) -> str:
        return self.render()

    @classmethod
    def create(cls, UIName, name, content):
        return UIELEMENT_LOOKUP[UIName](name, content)
    
    def update(self, contents):
        self.contents = contents

    def render(self):
        raise NotImplementedError('render() method requied in UIElement')

#UIElements
# Universal Elements
# Name: Instance Name, UIName: What form of UI, Section: Where does this show?, 

class Menu(UIElement, UIName='UIMenu'):
    def __init__(self, content, section, pageName, end="\n", **kargs):
        super().__init__(content, section, self, pageName, end)

    def render(self):
        r = ''
        for option, label in self.content.items():
            r += self.indent + option + ': ' + label + '.' + self.end
        return r

#Banners act like  header and footers that support generated dividers.
class Banner(UIElement, UIName='UIBanner'):
    def __init__(self, content, section, pageName, divCount=1, char='-', **kargs) -> None:
        super().__init__(content, section, self, pageName)
        self.dividerChar = char
        self.dividerCount = divCount
        self.dividerPadding = 0

    def changeDivider(self, char):
        if isinstance(char, str): self.dividerChar = char
        else:
            print('Banner: Invalid character type for divider')

    def genDivider(self)-> str:
        r = ''
        for i in range(self.dividerCount):
            r += self.dividerChar*self.width + '\n'
            if i < self.dividerPadding:
                r+= '\n'
        return r

    def render(self)-> str:
        r = ''
        r += self.genDivider()
        if isinstance(self.content, UI_ELEMENTS): r += self.content.render()
        elif isinstance(self.content, list): r += ''.join(self.content).center(self.width)
        else:
            r += self.content.center(self.width)
        r += self.genDivider()
        return r


class Title(UIElement, UIName='UITitle'):
    def __init__(self, content, section, pageName, prefix='', end='\n', alignment='Center', format='Title', **kargs) -> None:
        super().__init__(content, section, self, pageName)
        self.prefix = prefix
        self.alignment = ALIGNMENTS[alignment]
        self.format = TEXT_FORMAT[format]

    def __call__(self, *args, **kwds) -> str:
        self.render()

    def render(self)-> str:
        r = self.indent + self.content + self.end
        return self.format(self.alignment(r, self.width))

PROGRAM_WIDTH = 120
PROGRAM_WIDTH = 80

PAGE_SECTIONS = ('header', 'body', 'footer') #The breakdown of what a page is made up of


UI_ELEMENTS = (Menu, Banner, Title)

ALIGNMENTS = {'Center':str.center,
              'LJust':str.ljust,
              'RJust':str.rjust
            }

TEXT_FORMAT = {
                'Capitalize':str.capitalize,
                'Lower':str.lower,
                'Upper':str.upper,
                'Title':str.title
}

#GUI CONFIG

UIELEMENT_LOOKUP = {
    'menuData':Menu,
    'titleData':Title,
    'bannerMap':Banner
}
