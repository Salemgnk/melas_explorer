import os

def get_file_list(directory, search_term=""):
    try:
        files = [f for f in os.listdir(directory) if not f.startswith('.')]
        if search_term:
            files = [f for f in files if search_term.lower() in f.lower()]
    except PermissionError:
        files = []
    return files

def open_directory(path):
    try:
        os.chdir(path)
    except PermissionError:
        pass
    return path