from unicurses import *
from field_class import MinedField


HEAD_WIN_Y = 0
HEAD_WIN_X = 0
GAME_WIN_Y = HEAD_WIN_Y + 9
GAME_WIN_X = 0

MAX_LINE = 16
MAX_COLS = 16


class View:
    color_dic = {
        1: 21,
        2: 2,
        3: 1,
        4: 19,
        5: 52,
        6: 14,
        7: 5,
        8: 11
    }

    def __init__(self, side, height, bombs):
        self.standard_screen = initscr()
        noecho()
        cbreak()
        keypad(self.standard_screen, True)
        start_color()

        for i in range(1, 9):
            init_pair(i, self.color_dic[i], COLOR_BLACK)

        # Creation of heading and game windows and panels inside the standard screen
        self.head_win = newwin(9, 100, HEAD_WIN_Y, HEAD_WIN_X)
        self.game_win = newwin(MAX_LINE + 2, MAX_COLS*3 + 2, GAME_WIN_Y, GAME_WIN_X)
        self.head_pan = new_panel(self.head_win)
        self.game_pan = new_panel(self.game_win)
        keypad(self.game_win, True)

        wmove(self.game_win, 1, 2)

        self.mf = MinedField(side, height, bombs)

        self.render_heading()
        self.render_field(self.mf)

        update_panels()
        doupdate()

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

    def render_field(self, mf):
        position = getyx(self.game_win)
        field_str = ''
        for y in range(1, mf.height + 1):
            for x in range(1, mf.side + 1):
                pos = mf.t_pos(x, y)
                point = mf.field[pos]
                if point.opened:
                    if point.type == 'NUMBER':
                        field_str = '{}'.format(point.number)
                    elif point.type == 'EMPTY':
                        field_str = ' '
                    elif point.type == 'BOMB':
                        field_str = '*'
                else:
                    field_str = 'F' if point.flagged else '?'
                mvwaddstr(self.game_win, y, x*3-2, '[')
                mvwaddstr(self.game_win, y, x*3-1, field_str, color_pair(point.number) if point.opened else 'NO_USE')
                mvwaddstr(self.game_win, y, x*3, ']')
        wmove(self.game_win, position[0], position[1])

    def finish_view(self):
        echo()
        nocbreak()
        keypad(self.standard_screen, False)

        endwin()

    def process_key_input(self, key):
        pos = getyx(self.game_win)
        if (key == ord('q')) or (key == ord('Q')):
            return 0
        elif key == KEY_UP and (pos[0] > 1):
            wmove(self.game_win, pos[0]-1, pos[1])
            self.write('UP   ')
            return 1
        elif key == KEY_DOWN and (pos[0] < self.mf.height):
            wmove(self.game_win, pos[0]+1, pos[1])
            self.write('DOWN ')
            return 1
        elif key == KEY_LEFT and (pos[1] > 2):
            wmove(self.game_win, pos[0], pos[1]-3)
            self.write('LEFT ')
            return 1
        elif key == KEY_RIGHT and (pos[1] < self.mf.side*3-2):
            wmove(self.game_win, pos[0], pos[1]+3)
            self.write('RIGHT')
            return 1
        elif key == ord(' '):
            self.key_action('OPEN')
            self.write('OPEN ')
            return 1
        elif (key == ord('f')) or (key == ord('F')):
            self.key_action('FLAG')
            self.write('FLAG ')
            return 1
        elif (key == ord('m')) or (key == ord('M')):
            # self.main_menu()
            self.write('MENU ')
            return 1
        else:
            return 2

    def write(self, string):
        pos = getyx(self.game_win)
        mvwaddstr(self.game_win, 0, 0, string, A_BOLD)
        wmove(self.game_win, pos[0], pos[1])

    def key_action(self, action):
        pos = getyx(self.game_win)
        y = pos[0]
        x = (pos[1] + 1) // 3
        if action == 'OPEN':
            self.mf.open_cell(x, y)
            self.render_field(self.mf)
        elif action == 'FLAG':
            self.mf.flag_cell(x, y)
            self.render_field(self.mf)
        update_panels()
        doupdate()

