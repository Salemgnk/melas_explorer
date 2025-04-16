import curses
import os
from core.file_utils import get_file_list

def navigate_files(key, selected_index, scroll_offset, files):
    if key == curses.KEY_UP and selected_index > 0:
        selected_index -= 1
        if selected_index < scroll_offset:
            scroll_offset -= 1
    elif key == curses.KEY_DOWN and selected_index < len(files) - 1:
        selected_index += 1
        if selected_index >= scroll_offset + curses.LINES - 7:  # Adjusted for header, titles, help
            scroll_offset += 1
    return selected_index, scroll_offset

def navigate_right_panel(screen, key, scroll_offset, files, selected_index, current_dir):
    selected_file = files[selected_index] if files else ""
    selected_path = os.path.join(current_dir, selected_file)
    max_y, _ = screen.getmaxyx()
    max_visible = max_y - 10  # Adjusted for header, titles, metadata, help

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