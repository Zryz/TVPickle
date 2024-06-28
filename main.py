from tv_pickle import *
from ui import BLOCK_ALPHABET, BLACK_7, TINY

uppz = "     __  __ __  __ __ __                        __  __  __  __  _____                 ___\n /\ |__)/  |  \|_ |_ / _ |__||  ||_/|  |\/||\ |/  \|__)/  \|__)(_  | /  \\  /|  |\/\_/ _/\n/--\|__)\__|__/|__|  \__)|  ||(_)| \|__|  || \|\__/|   \_\/| \ __) | \__/ \/ |/\|/\ | /__"

upper = "     __  __ __  __ __ __                        __  __  __  __  _____                 ___\n /\ |__)/  |  \|_ |_ / _ |__||  ||_/|  |\/||\ |/  \|__)/  \|__)(_  | /  \\  /|  |\/\_/ _/\n/--\|__)\__|__/|__|  \__)|  ||(_)| \|__|  || \|\__/|   \_\/| \ __) | \__/ \/ |/\|/\ | /__"
lower = "                _                                               \n _ |_  _  _| _ (_ _ |_ oo| | _  _  _  _  _  _ _|_             _ \n(_||_)(_ (_|(-`| (_)| )|||<||||| )(_)|_)(_|| _)|_|_|\/\/\/><\//_\n                 _/     /            |    |                 /   "

numeric = "  __     __  __        __  __  ___  __   __  \n /  \ /|  _)  _) |__| |_  /__    / (__) (__\ \n \__/  | /__ __)    | __) \__)  /  (__)  __/ "


#this = Title('Hello', BLOCK_ALPHABET)
#this.width = 150
#this.render()
#asdsa()
#Instiate the Application Engine


tv = TVPickle()
#print(tv.ui.generate_ascii_letter('a', BLOCK_ALPHABET))
#Title('m', BLOCK_ALPHABET)
#Building of the user interface pages
tv.ui.create_page('intro', [.1,.8,.1], [None, None, None], [0,1,0])
tv.ui.create_page('mode', [0.25, .05, 0.65, 0.05], [None, None,[0.1, 0.27,0.27,0.26, 0.1], None],[2,0,0,2,2,2,0,0])
tv.ui.create_page('results', [.1,.8,.1], [None, None, None],[0,1,0])

tv.ui.create_page('discover', [.25,.05,.45,.1,.15], [None, None,[.2,.15,.15,.15,.15,.2], [0.2,0.6,0.2], None], [2,0,0,-1,-1,-1,-1,0,0,1,0,0])
#tv.ui.block_decorate('query', 3, 4, 5, 6    )

#tv.ui.set_input_window('query', 5, 2, 4)

#Attach content to the pages

tv.ui.set_content('intro', 0, Title(INTRO_TITLE)+ 'Welcome to TV Pickle - The ultimate TV picking tool.' +'\nTo Begin Press Space!' )

tv.ui.set_content('mode', 0, Title('Choose A Mode', BLACK_7))
tv.ui.set_content('mode', 1, Title(TELEVISION) + '' + Title('Television', BLOCK_ALPHABET) + '\n' + Title('Press T',BLOCK_ALPHABET))
tv.ui.set_content('mode', 2, Title(CINEMA) + ''+ Title('Movie', BLOCK_ALPHABET) + '\n' + Title('Press M',BLOCK_ALPHABET))
tv.ui.set_content('mode', 3, Title(ACTOR) + '' + Title('Actor', BLOCK_ALPHABET) + '\n' + Title('Press A', BLOCK_ALPHABET))

#tv.ui.set_content('query', 0, Title(tv.get_app_mode(), BLACK_7))

tv.ui.select_page('intro')
tv.cycle()