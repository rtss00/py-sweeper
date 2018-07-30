from unicurses import *


HEAD_WIN_Y = 0
HEAD_WIN_X = 0
GAME_WIN_Y = HEAD_WIN_Y + 9
GAME_WIN_X = 0

MAX_LINE = 16
MAX_COLS = 16


class View:
    def __init__(self):
        self.standard_screen = initscr()
        noecho()
        nocbreak()
        keypad(self.standard_screen, True)

        # Creation of heading and game windows and panels inside the standard screen
        self.head_win = newwin(9, 100, 0, 0)
        self.game_win = newwin(MAX_LINE + 2, MAX_COLS*3 + 2, GAME_WIN_Y, GAME_WIN_X)
        self.head_pan = new_panel(self.head_win)
        self.game_pan = new_panel(self.game_win)

        self.render_heading()
        self.render_field()

        box(self.head_win)
        box(self.game_win)

        update_panels()
        doupdate()

        getch()

    def render_heading(self):
        head = [" ___      ___                                +-------------------------------------------+\n"
                " | _ \_  _/ __|_ __ _____ ___ _ __  ___ _ _   | Use the arrow keys to move the cursor     |\n"
                " |  _/ || \__ \ V  V / -_) -_) '_ \/ -_) '_|  | Press F to flag a cell or space to open it|\n"
                " |_|  \_, |___/\_/\_/\___\___| .__/\___|_|    | Press M to return to the main menu        |\n"
                "      |__/                   |_|              | Press Q to quit the game                  |\n"
                "                                              +-------------------------------------------+\n"
                ]

        for i in range(0, head.__len__()):
            mvwaddstr(self.head_win, i+1, 1, head[i])

    def render_field(self):
        for i in range(1, 17):
            mvwaddstr(self.game_win, i, 1, '[ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ][ ]')

    def finish_view(self):
        echo()
        cbreak()
        keypad(self.standard_screen, False)

        endwin()
