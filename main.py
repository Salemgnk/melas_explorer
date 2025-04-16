import os
import curses
import time

def run_window():
    screen = curses.initscr()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)   # Folders
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Files
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Old Metadatas (unused)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Metadatas
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    current_dir = os.getcwd()
    search_term = ""
    files = get_file_list(current_dir, search_term)
    selected_index = 0
    scroll_offset_left = 0
    scroll_offset_right = 0
    active_panel = 'left'  # 'left' or 'right'

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
            elif key == ord('\t'):  # Tab key to switch panels
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
    screen.addstr(max_y // 2, 0, "Research: ")
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
        screen.addstr(max_y // 2, 0, f"Research: {search_term}")
        screen.refresh()

def draw_interface(screen, files, selected_index, scroll_offset_left, scroll_offset_right, current_dir, active_panel):
    screen.clear()
    max_y, max_x = screen.getmaxyx()
    split_x = max_x // 2

    # Header
    app_name = "Melas Explorer"
    screen.addstr(0, (max_x - len(app_name)) // 2, app_name, curses.A_BOLD | curses.color_pair(4))

    # Left Panel: File List
    visible_files = files[scroll_offset_left:scroll_offset_left + (max_y - 3)]  # Adjusted for header
    for idx, filename in enumerate(visible_files):
        file_index = scroll_offset_left + idx
        file_path = os.path.join(current_dir, filename)
        color = curses.color_pair(1) if os.path.isdir(file_path) else curses.color_pair(2)
        if file_index == selected_index and active_panel == 'left':
            screen.addstr(idx + 1, 0, filename[:split_x - 1], curses.A_REVERSE | color)  # Shift down by 1
        else:
            screen.addstr(idx + 1, 0, filename[:split_x - 1], color)

    # Right Panel: Content or Directory Listing
    selected_file = files[selected_index] if files else ""
    selected_path = os.path.join(current_dir, selected_file)
    right_content = []
    if os.path.isdir(selected_path):
        right_content = get_file_list(selected_path)
        screen.addstr(1, split_x + 1, f"{selected_file}/", curses.A_BOLD | curses.color_pair(1))  # Shift down by 1
    elif os.path.isfile(selected_path):
        screen.addstr(1, split_x + 1, selected_file, curses.A_BOLD | curses.color_pair(2))
        try:
            with open(selected_path, 'r') as f:
                right_content = [line.strip() for line in f.readlines()]
        except:
            right_content = ["[Error while reading file]"]

    # Display Right Panel Content with Scroll
    visible_right_content = right_content[scroll_offset_right:scroll_offset_right + (max_y - 5)]  # Adjusted for header and metadata
    for i, item in enumerate(visible_right_content):
        if os.path.isdir(selected_path):
            item_path = os.path.join(selected_path, item)
            color = curses.color_pair(1) if os.path.isdir(item_path) else curses.color_pair(2)
        else:
            color = curses.color_pair(2)
        screen.addstr(i + 2, split_x + 1, item[:split_x - 2], color)  # Shift down by 2

    # Metadata at Bottom of Right Panel
    if os.path.exists(selected_path):
        stats = os.stat(selected_path)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))
        size = stats.st_size
        screen.addstr(max_y - 2, split_x + 1, f"Modified: {mtime} | Size: {size} octets", curses.color_pair(3))

    # Help Text
    help_text = f"↑/↓: Navigate   /: Search   u: Go up   Enter: Open directory   Tab: Switch panel   q: Quit"
    screen.addstr(max_y - 1, 0, help_text[:max_x - 1], curses.A_DIM)
    screen.refresh()

def navigate_files(key, selected_index, scroll_offset, files):
    if key == curses.KEY_UP and selected_index > 0:
        selected_index -= 1
        if selected_index < scroll_offset:
            scroll_offset -= 1
    elif key == curses.KEY_DOWN and selected_index < len(files) - 1:
        selected_index += 1
        if selected_index >= scroll_offset + curses.LINES - 4:  # Adjusted for header
            scroll_offset += 1
    return selected_index, scroll_offset

def navigate_right_panel(screen, key, scroll_offset, files, selected_index, current_dir):
    selected_file = files[selected_index] if files else ""
    selected_path = os.path.join(current_dir, selected_file)
    max_y, _ = screen.getmaxyx()
    max_visible = max_y - 5  # Adjusted for header and metadata

    content_length = 0
    if os.path.isdir(selected_path):
        content_length = len(get_file_list(selected_path))
    elif os.path.isfile(selected_path):
        try:
            with open(selected_path, 'r') as f:
                content_length = len(f.readlines())
        except:
            content_length = 1

    if key == curses.KEY_UP and scroll_offset > 0:
        scroll_offset -= 1
    elif key == curses.KEY_DOWN and scroll_offset + max_visible < content_length:
        scroll_offset += 1
    return scroll_offset

def open_directory(path):
    try:
        os.chdir(path)
    except PermissionError:
        pass
    return path

if __name__ == '__main__':
    run_window()