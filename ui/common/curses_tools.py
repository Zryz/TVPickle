import curses


#Anything that handles curses or helps to initialise the curses windows and it's global namespaces are referenced and defined from here

def generate_xterm_colors():
    colors = []

    # 16 basic colors
    basic_colors = [
        (0, 0, 0), (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128), (0, 128, 128), (192, 192, 192),
        (128, 128, 128), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 0, 255), (0, 255, 255), (255, 255, 255)
    ]
    
    colors.extend(basic_colors)

    # 216 colors (6x6x6 color cube)
    levels = [0, 95, 135, 175, 215, 255]
    for r in levels:
        for g in levels:
            for b in levels:
                colors.append((r, g, b))

    # 24 grayscale colors
    grayscale_levels = [8 + 10 * i for i in range(24)]
    for gray in grayscale_levels:
        colors.append((gray, gray, gray))

    return colors


def init_curses_colors(colors):
    #curses.start_color()
    #curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    for i, (r, g, b) in enumerate(colors):
        if i >= 255:
            break
        curses.init_color(i+1, int(r * 1000 / 255), int(g * 1000 / 255), int(b * 1000 / 255))
        curses.init_pair(i + 2, i+1, curses.COLOR_BLACK)

XTERMCOLOURS = generate_xterm_colors()