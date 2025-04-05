import os
import curses

def run_window():
    screen = curses.initscr()
    curses.start_color()  # Active les couleurs
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Dossier = bleu
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # Fichier = blanc
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)

    current_dir = os.getcwd()  # Dossier courant
    search_term = ""  # Termes de recherche
    files = get_file_list(current_dir, search_term)
    selected_index = 0
    scroll_offset = 0

    try:
        while True:
            draw_interface(screen, files, selected_index, scroll_offset, current_dir)

            key = screen.getch()

            if key == ord('q'):
                break

            selected_index, scroll_offset = navigate_files(key, selected_index, scroll_offset, files)

            if key == ord('/'):  # Recherche (touche /)
                search_term = get_search_term(screen)
                files = get_file_list(current_dir, search_term)  # Met à jour les fichiers avec la recherche
                selected_index = 0  # Réinitialiser la sélection
                scroll_offset = 0

            elif key == ord('u'):  # Touche pour remonter dans l'arborescence
                current_dir = os.path.dirname(current_dir)  # Remonte au répertoire parent
                files = get_file_list(current_dir, search_term)
                selected_index = 0  # Réinitialiser la sélection
                scroll_offset = 0

            elif key == 10:  # Touche Entrée
                selected_file = files[selected_index]
                selected_path = os.path.join(current_dir, selected_file)

                if os.path.isdir(selected_path):  # Si c'est un dossier, on l'ouvre
                    current_dir = open_directory(screen)
                    files = get_file_list(current_dir, search_term)
                    selected_index = 0  # Réinitialiser la sélection
                    scroll_offset = 0
                else:  # Si c'est un fichier, on affiche son nom (ou son contenu pour les fichiers texte)
                    screen.clear()
                    screen.addstr(0, 0, f"Ouvrir le fichier: {selected_file}")
                    screen.refresh()
                    screen.getch()

    finally:
        curses.nocbreak()
        screen.keypad(False)
        curses.echo()
        curses.endwin()

def get_file_list(directory, search_term=""):
    """ Récupère la liste des fichiers dans un répertoire donné. """
    try:
        files = [file for file in os.listdir(directory) if not file.startswith('.')]
        if search_term:
            files = [file for file in files if search_term.lower() in file.lower()]
    except PermissionError:
        files = []  # Si on n'a pas la permission, retourner une liste vide
    return files

def get_search_term(screen):
    """ Fonction pour gérer l'entrée du terme de recherche. """
    search_term = ""
    max_y, max_x = screen.getmaxyx()

    # Afficher un champ de saisie pour la recherche
    screen.clear()
    screen.addstr(max_y // 2, 0, "Recherche: ")
    screen.refresh()

    while True:
        key = screen.getch()

        if key == 27:  # Touche Esc pour annuler la recherche
            return ""
        elif key == 10:  # Touche Entrée pour valider
            return search_term
        elif key == 263:  # Touche Backspace
            search_term = search_term[:-1]
        elif 32 <= key <= 126:  # Autres caractères
            search_term += chr(key)

        screen.clear()
        screen.addstr(max_y // 2, 0, f"Recherche: {search_term}")
        screen.refresh()

def draw_interface(screen, files, selected_index, scroll_offset, current_dir):
    """ Gère l'affichage de l'interface principale. """
    screen.clear()
    max_y, max_x = screen.getmaxyx()

    visible_files = files[scroll_offset:scroll_offset + (max_y - 1)]

    for idx, filename in enumerate(visible_files):
        file_index = scroll_offset + idx
        file_path = os.path.join(current_dir, filename)
        if os.path.isdir(file_path):
            color = curses.color_pair(1)  # Dossier = bleu
        else:
            color = curses.color_pair(2)  # Fichier = blanc

        if file_index == selected_index:
            screen.addstr(idx, 0, filename[:max_x - 1], curses.A_REVERSE | color)
        else:
            screen.addstr(idx, 0, filename[:max_x - 1], color)

    help_text = f"↑/↓: Navigate   q: Quit   u: Up   /: Search   Enter: Open"
    screen.addstr(max_y - 1, 0, help_text[:max_x - 1], curses.A_DIM)

    screen.refresh()

def navigate_files(key, selected_index, scroll_offset, files):
    """ Gère la navigation dans les fichiers (haut/bas, sélection, ouverture). """
    if key == curses.KEY_UP and selected_index > 0:
        selected_index -= 1
        if selected_index < scroll_offset:
            scroll_offset -= 1  # Scroll si la sélection sort de l'écran
    elif key == curses.KEY_DOWN and selected_index < len(files) - 1:
        selected_index += 1
        if selected_index >= scroll_offset + curses.LINES - 2:  # Si on dépasse l'écran
            scroll_offset += 1

    return selected_index, scroll_offset

def open_directory(selected_path):
    """ Ouvre un répertoire sélectionné. """
    try:
        os.chdir(selected_path)
    except PermissionError:
        pass  # Si on n'a pas les droits, on ne fait rien
    return selected_path

if __name__ == '__main__':
    run_window()
