
#Define the structure for custom fonts to be used as Title objects.
FONT_TEMPLATE = {'special_chars':"""""",'special':{' ':'   \n   ','.':"  \n▄ "},'numeric':{'default_width':0,'widths':{'0':0},'content':""},'upper':{'gap':0,'default_width':0, 'widths':{'Character Here':0},'content':""}}
BLOCK_ALPHABET = {'special_chars':""" .,'-()!?'""",'special':{' ':'   \n   ','.':"  \n▄ ",',':"  \n█ ",'-':"   \n▀▀ ",'(':'▄▀ \n▀▄ ',')':'▀▄ \n▄▀ ','!':'█ \n▄ ','?':'▄▀▄ \n ▄▀ '},'numeric':{'gap':1,'default_width':2,'widths':{'0':3, '3':3, '8':3},'content':"█▀█ ▄█ ▀█ ▀██ █▄ █▄ █▀ ▀█ █▄█ █\n█▄█  █ █▄ ▄▄█  █ ▄█ ██  █ █▄█ ▄█"},'upper':{'gap':1,'default_width':3, 'widths':{'I': 1,'F':2, 'N':4, 'M':5, 'W':5},'content':"▄▀▄ ██▄ ▄▀▀ █▀▄ ██▀ █▀ ▄▀  █▄█ █   █ █▄▀ █   █▄ ▄█ █▄ █ ▄▀▄ █▀▄ ▄▀▄ █▀▄ ▄▀▀ ▀█▀ █ █ █ █ █   █ ▀▄▀ ▀▄▀ ▀█\n█▀█ █▄█ ▀▄▄ █▄▀ █▄▄ █▀ ▀▄█ █ █ █ ▀▄█ █ █ █▄▄ █ ▀ █ █ ▀█ ▀▄▀ █▀  ▀▄█ █▀▄ ▄██  █  ▀▄█ ▀▄▀ ▀▄▀▄▀ █ █  █  █▄▄"}}

BLACK_7 = {'special_chars':""" .,?!()""",'special':{' ':'    \n    \n    \n    \n    \n    ', '.':'   \n   \n   \n   \n██╗\n╚═╝'},'upper':{'gap':0,'default_width':8, 'widths':{'I':3,'G':9,'M':11,'N':10,'O':9,'Q':9,'T':9,'U':9,'V':9,'W':10,'Y':9},'content':" █████╗ ██████╗  ██████╗██████╗ ███████╗███████╗ ██████╗ ██╗  ██╗██╗     ██╗██╗  ██╗██╗     ███╗   ███╗███╗   ██╗ ██████╗ ██████╗  ██████╗ ██████╗ ███████╗████████╗██╗   ██╗██╗   ██╗██╗    ██╗██╗  ██╗██╗   ██╗███████╗\n██╔══██╗██╔══██╗██╔════╝██╔══██╗██╔════╝██╔════╝██╔════╝ ██║  ██║██║     ██║██║ ██╔╝██║     ████╗ ████║████╗  ██║██╔═══██╗██╔══██╗██╔═══██╗██╔══██╗██╔════╝╚══██╔══╝██║   ██║██║   ██║██║    ██║╚██╗██╔╝╚██╗ ██╔╝╚══███╔╝\n███████║██████╔╝██║     ██║  ██║█████╗  █████╗  ██║  ███╗███████║██║     ██║█████╔╝ ██║     ██╔████╔██║██╔██╗ ██║██║   ██║██████╔╝██║   ██║██████╔╝███████╗   ██║   ██║   ██║██║   ██║██║ █╗ ██║ ╚███╔╝  ╚████╔╝   ███╔╝ \n██╔══██║██╔══██╗██║     ██║  ██║██╔══╝  ██╔══╝  ██║   ██║██╔══██║██║██   ██║██╔═██╗ ██║     ██║╚██╔╝██║██║╚██╗██║██║   ██║██╔═══╝ ██║▄▄ ██║██╔══██╗╚════██║   ██║   ██║   ██║╚██╗ ██╔╝██║███╗██║ ██╔██╗   ╚██╔╝   ███╔╝  \n██║  ██║██████╔╝╚██████╗██████╔╝███████╗██║     ╚██████╔╝██║  ██║██║╚█████╔╝██║  ██╗███████╗██║ ╚═╝ ██║██║ ╚████║╚██████╔╝██║     ╚██████╔╝██║  ██║███████║   ██║   ╚██████╔╝ ╚████╔╝ ╚███╔███╔╝██╔╝ ██╗   ██║   ███████╗\n╚═╝  ╚═╝╚═════╝  ╚═════╝╚═════╝ ╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚═╝ ╚════╝ ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝      ╚══▀▀═╝ ╚═╝  ╚═╝╚══════╝   ╚═╝    ╚═════╝   ╚═══╝   ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝"},'numeric':{'gap':0,'default_width':8,'widths':{'0':9,'1':4,'6':9},'content':" ██████╗  ██╗██████╗ ██████╗ ██╗  ██╗███████╗ ██████╗ ███████╗ █████╗  █████╗ \n██╔═████╗███║╚════██╗╚════██╗██║  ██║██╔════╝██╔════╝ ╚════██║██╔══██╗██╔══██╗\n██║██╔██║╚██║ █████╔╝ █████╔╝███████║███████╗███████╗    ██╔╝ ╚█████╔╝╚██████║\n████╔╝██║ ██║██╔═══╝  ╚═══██╗╚════██║╚════██║██╔═══██╗  ██╔╝  ██╔══██╗ ╚═══██║\n╚██████╔╝ ██║███████╗██████╔╝     ██║███████║╚██████╔╝  ██║   ╚█████╔╝ █████╔╝\n ╚═════╝  ╚═╝╚══════╝╚═════╝      ╚═╝╚══════╝ ╚═════╝   ╚═╝    ╚════╝  ╚════╝ "}}

TINY = {'special_chars':""" .,'?""",'special':{' ':'  \n  \n  ','.':"  \n  \no ",',':'  \n  \n/ ',"'":'/ \n  \n  ','?':'_ \n )\no '},'numeric':{'gap':1,'default_width':4,'widths':{'1':2, '2':3, '3':3, '5':3, '7':3},'content':"  __     __  __        __  __  ___  __   __  \n /  \ /|  _)  _) |__| |_  /__    / (__) (__\ \n \__/  | /__ __)    | __) \__)  /  (__)  __/ "}, 'upper':{'gap':0,'default_width':4, 'widths':{'C':3,'E':3,'F':3,'I':1,'J':2,'L':3,'S':3,'T':3,'X':2,'Y':3,'Z':3}, 'content':"     __  __ __  __ __ __                        __  __  __  __  _____                 ___\n /\ |__)/  |  \|_ |_ / _ |__||  ||_/|  |\/||\ |/  \|__)/  \|__)(_  | /  \\\\  /|  |\/\_/ _/\n/--\|__)\__|__/|__|  \__)|  ||(_)| \|__|  || \|\__/|   \_\/| \ __) | \__/ \/ |/\|/\ | /__"},'lower':{'gap':0,'default_width':3, 'widths':{'f':2,'i':1,'j':1,'k':2,'l':1,'r':2,'s':2,'t':2,'v':2,'w':4,'x':2,'y':2,'z':2},'content':"                _                                               \n _ |_  _  _| _ (_ _ |_ oo| | _  _  _  _  _  _ _|_             _ \n(_||_)(_ (_|(-`| (_)| )|||<||||| )(_)|_)(_|| _)|_|_|\/\/\/><\//_\n                 _/     /            |    |                 /   "}}


 #Font typically have a common width, defined as default_width - outliers can be defined within the 'widths' indivdually. 

def get_ascii_width(char, source):
    if char not in source['widths']: width = source['default_width']
    else: width = source['widths'][char]
    return width

#Special = Returned directly
#Numeric = Generated (due to complexities of layers)
#Alpha = Determine whether font supports given case and select correct library

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
    width = get_ascii_width(char, source[library])
    if library == 'upper':
        content_index = sum([get_ascii_width(chr(x), source[library])+source[library]['gap'] for x in range(65,ord(char))])
    elif library == 'lower':
        content_index = sum([get_ascii_width(chr(x), source[library])+source[library]['gap'] for x in range(97,ord(char))])
    else:
        content_index = sum([get_ascii_width(chr(x), source[library])+source[library]['gap'] for x in range(48,ord(char))])
    
    total_width = source[library]['content'].index('\n')+1
    
    r = []
    for i in range(content_index,(total_width)*ascii_height, total_width):
        r.append(source[library]['content'][i:i+width]+' '*source[library]['gap'])
    return r

def generate_ascii_gap(source, size, height):
    r = []
    for _ in range(height):
        for _ in range(size):
            r.append(' '*size)
    return r