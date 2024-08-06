from api.api import TMDB_API
from api.http import http_request
from ui.ascii.fonts import TINY
from ui.elements.title import Title

class ResultRender():
    BLOCKED = ('backdrop_path', )
    tv_keys = ["adult", "backdrop_path", "genre_ids", "id", "origin_country", "original_language", "original_name", "overview", "popularity", "poster_path", "first_air_date", "name", "vote_average"]
    movie_keys = ["adult", "backdrop_path", "genre_ids", "id", "original_language", "original_title", ""]
    def __init__(self, contents:list, mode:str, t_height, t_width, cols = 1) -> None:
        self.t_height = t_height
        self.t_width = t_width
        self.mode = mode
        self.cols = cols 

        self.ptr = 0
        self.contents = contents
        self.size = len(contents)

        self.selected = self.contents[self.ptr]

        self.update()
        super().__init__()

    def next_result(self):
        if self.ptr < len(self.contents)-1:
            self.ptr += 1
        self.selected = self.contents[self.ptr]
        self.update()

    def prev_result(self):
        if self.ptr > 0:
            self.ptr -= 1
        self.selected = self.contents[self.ptr]
        self.update()

    def set_title(self):
        if self.mode == 'TV':
            self.title = Title(self.selected['name'], TINY)
            self.title.width = self.t_width
        elif self.mode == 'Movie':
            self.title = Title(self.selected['title'], TINY)
            self.title.width = self.t_width

    def generate_image(self):
        for key, val in self.selected.items():
            if key == 'poster_path':
                url = TMDB_API._IMG_BASE + TMDB_API._IMG_SIZE + val
                image = http_request(url, direct=True)
                self.image_data = image

    def update(self):
        self.set_title()
        self.generate_image()
        self.render()

    def draw_overview(self, line):
        z, i = "", 1
        for char in line:
            if i == self.t_width-1:
                z += '\n'
                i == 1
            z+=char
            i+=1
        return z+'\n'
    
    def render(self):
        r = ""
        r += self.title.render()
        for key, val in self.selected.items():
            if key in self.BLOCKED:continue
            if key == 'poster_path': continue
            if key == 'genre_ids': continue
            if key == 'overview': r += self.draw_overview(val)
            else: r += key + ":" + zrepr(val) + '\n'
        return r

def zrepr(item):
    item = item.__repr__().replace("'",'')
    return item