import curses
import os
import time
from core.file_utils import get_file_list
from ui.components import draw_box

def draw_interface(screen, files, selected_index, scroll_offset_left, scroll_offset_right, current_dir, active_panel):
    screen.clear()
    max_y, max_x = screen.getmaxyx()
    split_x = max_x // 2

    # Header: Full-width App Name Box
    app_name = "Nexlify Explorer"
    draw_box(screen, 0, 0, 3, max_x, app_name, curses.color_pair(5) | curses.A_BOLD)

    # Left Panel Title: Current Directory
    left_title = os.path.basename(current_dir) or current_dir
    draw_box(screen, 3, 0, 3, split_x, left_title[:split_x - 4], curses.color_pair(6) | curses.A_BOLD)

    # Right Panel Title: Content of Selected File/Folder
    selected_file = files[selected_index] if files else ""
    right_title = f"Content of {selected_file}" if selected_file else "No Selection"
    draw_box(screen, 3, split_x + 1, 3, max_x - split_x - 1, right_title[:(max_x - split_x - 5)], curses.color_pair(7) | curses.A_BOLD)

    # Vertical Separator
    for y in range(6, max_y - 3):
        screen.addstr(y, split_x, "│")

    # Left Panel: File List
    visible_files = files[scroll_offset_left:scroll_offset_left + (max_y - 9)]  # Adjusted for header, titles, help
    for idx, filename in enumerate(visible_files):
        file_index = scroll_offset_left + idx
        file_path = os.path.join(current_dir, filename)
        color = curses.color_pair(1) if os.path.isdir(file_path) else curses.color_pair(2)
        if file_index == selected_index and active_panel == 'left':
            screen.addstr(idx + 6, 0, filename[:split_x - 1], curses.A_REVERSE | color)
        else:
            screen.addstr(idx + 6, 0, filename[:split_x - 1], color)

    # Right Panel: Content or Directory Listing
    selected_path = os.path.join(current_dir, selected_file)
    right_content = []
    if os.path.isdir(selected_path):
        right_content = get_file_list(selected_path)
        screen.addstr(6, split_x + 1, f"{selected_file}/", curses.A_BOLD | curses.color_pair(1))
    elif os.path.isfile(selected_path):
        screen.addstr(6, split_x + 1, selected_file, curses.A_BOLD | curses.color_pair(2))
        try:
            with open(selected_path, 'r') as f:
                right_content = [line.strip() for line in f.readlines()]
        except:
            right_content = ["[Error while reading file]"]

    # Display Right Panel Content with Scroll
    visible_right_content = right_content[scroll_offset_right:scroll_offset_right + (max_y - 13)]  # Adjusted for header, titles, metadata, help
    for i, item in enumerate(visible_right_content):
        if os.path.isdir(selected_path):
            item_path = os.path.join(selected_path, item)
            color = curses.color_pair(1) if os.path.isdir(item_path) else curses.color_pair(2)
        else:
            color = curses.color_pair(2)
        screen.addstr(i + 7, split_x + 1, item[:split_x - 2], color)

    # Metadata Box
    if os.path.exists(selected_path):
        stats = os.stat(selected_path)
        mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))
        size = stats.st_size
        metadata_text = f"Modified: {mtime} | Size: {size} octets"
        draw_box(screen, max_y - 5, split_x + 1, 3, min(len(metadata_text) + 4, max_x - split_x - 1), metadata_text, curses.color_pair(4))

    # Help Box
    help_text = "↑/↓: Navigate   /: Search   u: Go up   Enter: Open directory   Tab: Switch panel   q: Quit"
    draw_box(screen, max_y - 3, 0, 3, min(max_x, len(help_text) + 4), help_text, curses.color_pair(8))

    screen.refresh()