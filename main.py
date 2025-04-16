import os
import curses
import time

def run_window():
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)   # Folders
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Files
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Metadatas
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    current_dir = os.getcwd()
    search_term = ""
    files = get_file_list(current_dir, search_term)
    selected_index = 0
    scroll_offset = 0

    try:
        while True:
            draw_interface(screen, files, selected_index, scroll_offset, current_dir)

            key = screen.getch()

            if key == ord('q'):
                break
            elif key == ord('/'):
                search_term = get_search_term(screen)
                files = get_file_list(current_dir, search_term)
                selected_index = 0
                scroll_offset = 0
            elif key == ord('u'):
                current_dir = os.path.dirname(current_dir)
                files = get_file_list(current_dir, search_term)
                selected_index = 0
                scroll_offset = 0
            elif key == 10:
                selected_file = files[selected_index]
                selected_path = os.path.join(current_dir, selected_file)
                if os.path.isdir(selected_path):
                    current_dir = open_directory(selected_path)
                    files = get_file_list(current_dir, search_term)
                    selected_index = 0
                    scroll_offset = 0
            else:
                selected_index, scroll_offset = navigate_files(key, selected_index, scroll_offset, files)

    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()

def get_file_list(directory, search_term=""):
    try:
        files = [f for f in os.listdir(directory) if not f.startswith('.')]
        if search_term:
            files = [f for f in files if search_term.lower() in f.lower()]
    except PermissionError:
        files = []
    return files

def get_search_term(screen):
    search_term = ""
    max_y, max_x = screen.getmaxyx()
    screen.clear()
    screen.addstr(max_y // 2, 0, "Recherche: ")
    screen.refresh()

    while True:
        key = screen.getch()
        if key == 27:
            return ""
        elif key == 10:
            return search_term
        elif key in (8, 127, 263):
            search_term = search_term[:-1]
        elif 32 <= key <= 126:
            search_term += chr(key)
        screen.clear()
        screen.addstr(max_y // 2, 0, f"Recherche: {search_term}")
        screen.refresh()

def draw_interface(screen, files, selected_index, scroll_offset, current_dir):
    screen.clear()
    max_y, max_x = screen.getmaxyx()
    split_x = max_x // 2

    visible_files = files[scroll_offset:scroll_offset + (max_y - 2)]

    # Left Displaying
    for idx, filename in enumerate(visible_files):
        file_index = scroll_offset + idx
        file_path = os.path.join(current_dir, filename)
        color = curses.color_pair(1) if os.path.isdir(file_path) else curses.color_pair(2)
        if file_index == selected_index:
            screen.addstr(idx, 0, filename[:split_x - 1], curses.A_REVERSE | color)
        else:
            screen.addstr(idx, 0, filename[:split_x - 1], color)

    # Right Displaying
    selected_file = files[selected_index] if files else ""
    selected_path = os.path.join(current_dir, selected_file)
    if os.path.isdir(selected_path):
        content = get_file_list(selected_path)
        screen.addstr(0, split_x + 1, f"{selected_file}/", curses.A_BOLD | curses.color_pair(1))
        for i, f in enumerate(content[:max_y - 4]):
            screen.addstr(i + 1, split_x + 1, f[:split_x - 2], curses.color_pair(1 if os.path.isdir(os.path.join(selected_path, f)) else 2))
    elif os.path.isfile(selected_path):
        screen.addstr(0, split_x + 1, selected_file, curses.A_BOLD | curses.color_pair(2))
        try:
            with open(selected_path, 'r') as f:
                lines = f.readlines()
                for i, line in enumerate(lines[:max_y - 4]):
                    screen.addstr(i + 1, split_x + 1, line.strip()[:split_x - 2])
        except:
            screen.addstr(1, split_x + 1, "[Error while reading file]", curses.color_pair(3))

    # Metadatas
    if os.path.exists(selected_path):
        stats = os.stat(selected_path)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))
        size = stats.st_size
        screen.addstr(max_y - 2, split_x + 1, f"Modified: {mtime} | Size: {size} octets", curses.color_pair(3))

    help_text = f"↑/↓: Navigate   Enter: Ouvrir   /: Rechercher   u: Dossier parent   q: Quitter"
    screen.addstr(max_y - 1, 0, help_text[:max_x - 1], curses.A_DIM)
    screen.refresh()

def navigate_files(key, selected_index, scroll_offset, files):
    if key == curses.KEY_UP and selected_index > 0:
        selected_index -= 1
        if selected_index < scroll_offset:
            scroll_offset -= 1
    elif key == curses.KEY_DOWN and selected_index < len(files) - 1:
        selected_index += 1
        if selected_index >= scroll_offset + curses.LINES - 3:
            scroll_offset += 1
    return selected_index, scroll_offset

def open_directory(path):
    try:
        os.chdir(path)
    except PermissionError:
        pass
    return path

if __name__ == '__main__':
    run_window()
