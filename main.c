#include <ncurses.h>
#include <dirent.h>
#include <string.h>
#include <stdlib.h>

#define MAX_FILES 1000
#define MAX_PATH 256

typedef struct {
    char *files[MAX_FILES];
    int count;
    int selected;
    char search_term[MAX_PATH];
} FileManager;

void init_file_manager(FileManager *fm) {
    fm->count = 0;
    fm->selected = 0;
    fm->search_term[0] = '\0';
}

void free_file_manager(FileManager *fm) {
    for (int i = 0; i < fm->count; i++) {
        free(fm->files[i]);
    }
}

void update_file_list(FileManager *fm) {
    DIR *dir = opendir(".");
    struct dirent *entry;
    int i = 0;

    // Vider la liste actuelle
    for (int j = 0; j < fm->count; j++) {
        free(fm->files[j]);
    }
    fm->count = 0;

    // Remplir avec les fichiers filtrés
    while ((entry = readdir(dir)) != NULL && i < MAX_FILES) {
        if (entry->d_name[0] == '.') continue; // Ignorer les fichiers cachés
        if (fm->search_term[0] != '\0' && strstr(entry->d_name, fm->search_term) == NULL) continue;
        fm->files[i] = strdup(entry->d_name);
        i++;
    }
    fm->count = i;
    closedir(dir);

    // Ajuster la sélection
    if (fm->selected >= fm->count) fm->selected = fm->count - 1;
    if (fm->selected < 0 && fm->count > 0) fm->selected = 0;
}

void draw_interface(FileManager *fm, WINDOW *search_win, WINDOW *list_win, WINDOW *footer_win) {
    // Barre de recherche
    werase(search_win);
    mvwprintw(search_win, 0, 0, "Rechercher : %s", fm->search_term);
    wrefresh(search_win);

    // Liste des fichiers
    werase(list_win);
    int max_y, max_x;
    getmaxyx(list_win, max_y, max_x); // Taille de la fenêtre
    for (int i = 0; i < fm->count && i < max_y; i++) {
        if (i == fm->selected) {
            wattron(list_win, A_REVERSE); // Surligner l’élément sélectionné
            mvwprintw(list_win, i, 0, "%-*s", max_x, fm->files[i]);
            wattroff(list_win, A_REVERSE);
        } else {
            mvwprintw(list_win, i, 0, "%-*s", max_x, fm->files[i]);
        }
    }
    wrefresh(list_win);

    // Footer
    werase(footer_win);
    if (fm->count > 0 && fm->selected >= 0) {
        mvwprintw(footer_win, 0, 0, "Sélection : %s", fm->files[fm->selected]);
    } else {
        mvwprintw(footer_win, 0, 0, "q: quitter | ↑↓: naviguer | Enter: sélectionner");
    }
    wrefresh(footer_win);
}

int main() {
    // Initialiser ncurses
    initscr();
    cbreak();
    noecho();
    keypad(stdscr, TRUE);

    // Créer les fenêtres
    int max_y, max_x;
    getmaxyx(stdscr, max_y, max_x);
    WINDOW *search_win = newwin(1, max_x, 0, 0);         // 1 ligne en haut
    WINDOW *list_win = newwin(max_y - 2, max_x, 1, 0);   // Milieu
    WINDOW *footer_win = newwin(1, max_x, max_y - 1, 0); // 1 ligne en bas

    // Initialiser le gestionnaire
    FileManager fm;
    init_file_manager(&fm);
    update_file_list(&fm);

    // Boucle principale
    int ch;
    int search_pos = 0;
    bool in_search = false;

    while (true) {
        draw_interface(&fm, search_win, list_win, footer_win);

        ch = getch();
        if (in_search) {
            if (ch == '\n') { // Enter pour valider la recherche
                in_search = false;
                update_file_list(&fm);
            } else if (ch == KEY_BACKSPACE || ch == 127) {
                if (search_pos > 0) fm.search_term[--search_pos] = '\0';
            } else if (ch >= 32 && ch <= 126 && search_pos < MAX_PATH - 1) {
                fm.search_term[search_pos++] = ch;
                fm.search_term[search_pos] = '\0';
            }
        } else {
            switch (ch) {
                case 'q':
                case 'Q':
                    goto end; // Sortir
                case KEY_UP:
                    if (fm.selected > 0) fm.selected--;
                    break;
                case KEY_DOWN:
                    if (fm.selected < fm.count - 1) fm.selected++;
                    break;
                case '\n': // Enter pour sélectionner
                    if (fm.count > 0 && fm.selected >= 0) {
                        draw_interface(&fm, search_win, list_win, footer_win);
                        refresh();
                    }
                    break;
                case '/': // Activer la recherche
                    in_search = true;
                    fm.search_term[0] = '\0';
                    search_pos = 0;
                    break;
            }
        }
    }

end:
    free_file_manager(&fm);
    delwin(search_win);
    delwin(list_win);
    delwin(footer_win);
    endwin();
    return 0;
}