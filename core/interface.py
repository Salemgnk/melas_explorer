import curses
import os
from core.navigation import navigate_files, navigate_right_panel
from core.file_utils import get_file_list, open_directory
from ui.draw import draw_interface

def run_window(screen):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)    # Folders
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Files
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Old Metadatas (unused)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Metadata Box
    curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Header Box
    curses.init_pair(6, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Left Title Box
    curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK) # Right Title Box
    curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Help Box
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    current_dir = os.getcwd()
    search_term = ""
    files = get_file_list(current_dir, search_term)
    selected_index = 0
    scroll_offset_left = 0
    scroll_offset_right = 0
    active_panel = 'left'

    try:
        while True:
            draw_interface(screen, files, selected_index, scroll_offset_left, scroll_offset_right, current_dir, active_panel)

            key = screen.getch()

            if key == ord('q'):
                break
            elif key == ord('/'):
                search_term = get_search_term(screen)
                files = get_file_list(current_dir, search_term)
                selected_index = 0
                scroll_offset_left = 0
                scroll_offset_right = 0
            elif key == ord('u'):
                current_dir = os.path.dirname(current_dir)
                files = get_file_list(current_dir, search_term)
                selected_index = 0
                scroll_offset_left = 0
                scroll_offset_right = 0
            elif key == 10:  # Enter key
                selected_file = files[selected_index]
                selected_path = os.path.join(current_dir, selected_file)
                if os.path.isdir(selected_path):
                    current_dir = open_directory(selected_path)
                    files = get_file_list(current_dir, search_term)
                    selected_index = 0
                    scroll_offset_left = 0
                    scroll_offset_right = 0
            elif key == ord('\t'):  # Tab key
                active_panel = 'right' if active_panel == 'left' else 'left'
            else:
                if active_panel == 'left':
                    selected_index, scroll_offset_left = navigate_files(key, selected_index, scroll_offset_left, files)
                else:
                    scroll_offset_right = navigate_right_panel(screen, key, scroll_offset_right, files, selected_index, current_dir)

    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()

def get_search_term(screen):
    search_term = ""
    max_y, max_x = screen.getmaxyx()
    screen.clear()
    screen.addstr(max_y // 2, 0, "Recherche: ")
    screen.refresh()

    while True:
        key = screen.getch()
        if key == 27:  # Escape
            return ""
        elif key == 10:  # Enter
            return search_term
        elif key in (8, 127, 263):  # Backspace
            search_term = search_term[:-1]
        elif 32 <= key <= 126:  # Printable characters
            search_term += chr(key)
        screen.clear()
        screen.addstr(max_y // 2, 0, f"Recherche: {search_term}")
        screen.refresh()