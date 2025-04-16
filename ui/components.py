import curses

def draw_box(screen, y, x, height, width, text, attr=curses.A_NORMAL):
    # Draw box borders
    screen.addstr(y, x, "╔" + "═" * (width - 2) + "╗")
    for i in range(1, height - 1):
        screen.addstr(y + i, x, "║" + " " * (width - 2) + "║")
    screen.addstr(y + height - 1, x, "╚" + "═" * (width - 2) + "╝")
    
    # Center text inside the box
    text_y = y + (height - 1) // 2
    text_x = x + (width - len(text)) // 2
    screen.addstr(text_y, text_x, text[:width - 4], attr)