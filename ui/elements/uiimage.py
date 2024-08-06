
import curses

from PIL import Image
from ..common.curses_tools import init_curses_colors

class UIImage:
    def __init__(self, image_file, scale='Fit', width=None, height=None) -> None:
        self.img = Image.open(image_file)
        self.aspect = self.img.width / self.img.height


def extract_palette(img):
        palette = img.getpalette()
        colors = []
        for i in range(0, len(palette), 3):
            r, g, b = palette[i], palette[i+1], palette[i+2]
            colors.append((r, g, b))
        return colors

def get_orientation(img:Image):
        if img.width > img.height:
            return 'landscape'
        elif img.width == img.height:
            return 'square'
        else:
            return 'portrait'
        
def image_to_pallet(window:curses.window, uiimage:Image):
        img:Image = uiimage.img
        max_height, max_width = window.getmaxyx()
        original_width, original_height = img.size
        aspect_ratio = original_width / original_height
        # Calculate new dimensions to fit within max_width and max_height
        if original_width > max_width or original_height > max_height-1:
            if aspect_ratio > 1:  # Wider than tall
                new_width = min(max_width, original_width)
                new_height = int(new_width / aspect_ratio)
                if new_height > max_height:
                    new_height = max_height
                    new_width = int(new_height * aspect_ratio)
            else:  # Taller than wide or square
                new_height = min(max_height, original_height)
                new_width = int(new_height * aspect_ratio)
                if new_width > max_width:
                    new_width = max_width
                    new_height = int(new_width / aspect_ratio)
        else:
            new_width, new_height = original_width, original_height

        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img = img.convert('P', palette=Image.ADAPTIVE, colors=256)
        
        colors = extract_palette(img)
        init_curses_colors(colors)

        for y in range(img.height):
            for x in range(img.width):
                pixel = img.getpixel((x, y))
                window.addstr(y, x, "%", curses.color_pair(pixel+2))
        window.addstr(0,0,str(aspect_ratio))
        window.noutrefresh()
