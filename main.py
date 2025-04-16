import curses
from core.interface import run_window

if __name__ == "__main__":
    curses.wrapper(run_window)