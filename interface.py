import webbrowser

from unicurses import *
from field_class import MinedField

'''
This constants control where the game and heading windows will be created, as well as the maximum
sizes allowed for the mined field. 
'''
HEAD_WIN_Y = 0
HEAD_WIN_X = 0
GAME_WIN_Y = HEAD_WIN_Y + 6
GAME_WIN_X = 0

MAX_LINE = 16
MAX_COLS = 16

MENU_WIN_Y = GAME_WIN_Y
MENU_WIN_X = MAX_COLS*3 + 5


class View:
    color_dic = {  # This converts the number of a cell to an 8-bit color code.
        1: 21,
        2: 2,
        3: 1,
        4: 19,
        5: 52,
        6: 14,
        7: 5,
        8: 11
    }

    def __init__(self, side: int, height: int, bombs: int):
        """
        Initialize settings, create two panels for the heading and game areas, and create a field in the game
        area. The creation of a field inside this function is a temporary feature.
        :param side: Side length of field
        :param height: Height length of field
        :param bombs: Amount of bombs in field
        """

        self.side = side
        self.height = height
        self.bombs = bombs

        self.standard_screen = initscr()
        noecho()
        cbreak()
        keypad(self.standard_screen, True)
        start_color()

        for i in range(1, 9):
            init_pair(i, self.color_dic[i], COLOR_BLACK)

        # Creation of heading and game windows and panels inside the standard screen
        self.head_win = newwin(7, 100, HEAD_WIN_Y, HEAD_WIN_X)
        self.game_win = newwin(MAX_LINE + 2, MAX_COLS*3 + 2, GAME_WIN_Y, GAME_WIN_X)
        self.menu_win = newwin(height + 2, 38, MENU_WIN_Y, MENU_WIN_X)
        # self.side_win = newwin()

        self.head_pan = new_panel(self.head_win)
        self.game_pan = new_panel(self.game_win)
        self.menu_pan = new_panel(self.game_win)

        self.main_menu = ['START GAME!', 'SETTINGS', 'ABOUT', 'EXIT']
        self.about = ['Py-Sweeper.',
                      'Minesweeper implemented in Python3',
                      'Check GitHub for more info:',
                      'github.com/rtss00/py-sweeper',
                      '2018',
                      '<< BACK <<'
                      ]
        self.settings = ['SIDE: [  ]', 'HEIGHT: [  ]', 'BOMBS: [  ]', 'APPLY', '<< BACK <<']

        self.menus = [None, self.main_menu, self.settings, self.about]

        self.select = 1
        self.in_menu = 0

        keypad(self.game_win, True)
        keypad(self.menu_win, True)

        wmove(self.game_win, 1, 2)

        self.mf = MinedField(side, height, bombs)

        self.render_heading()
        self.render_field(self.mf)
        self.render_menu(self.main_menu, self.select, True)

        wrefresh(self.menu_win)
        update_panels()
        doupdate()

    def render_heading(self) -> None:
        """
        Render the heading of the game in the heading area.
        Note that doupdate() will not be called at the end of this function.
        :return:
        """
        head = [" ___      ___                                \n"
                " | _ \_  _/ __|_ __ _____ ___ _ __  ___ _ _   | Use the arrow keys to move the cursor     \n"
                " |  _/ || \__ \ V  V / -_) -_) '_ \/ -_) '_|  | Press F to flag a cell or space to open it\n"
                " |_|  \_, |___/\_/\_/\___\___| .__/\___|_|    | Press M to return to the main menu        \n"
                "      |__/                   |_|              | Press Q to quit the game                  \n"
                ]

        for i in range(0, head.__len__()):
            mvwaddstr(self.head_win, i, 1, head[i])
        update_panels()

    def render_field(self, mf: MinedField) -> None:
        """
        Render the field here in the game area.
        Note that doupdate() will not be called at the end of this function.
        :param mf:
        :return:
        """
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
        update_panels()

    def render_menu(self, arr, option, no_reverse=False):
        wclear(self.menu_win)
        position = getyx(self.game_win)
        wattron(self.menu_win, A_BOLD)
        size = arr.__len__()
        y = 1
        # box(self.menu_win)
        for i in range(0, size):  # Because of this statement the EXIT option MUST be at the end.
            x = (getmaxyx(self.menu_win)[1] - arr[i].__len__() - 1) // 2
            if option == i+1 and not no_reverse:
                wattron(self.menu_win, A_REVERSE)
                mvwaddstr(self.menu_win, y, x, arr[i])
                wattroff(self.menu_win, A_REVERSE)

            else:
                mvwaddstr(self.menu_win, y, x, arr[i])
            y = MAX_LINE if i == arr.__len__()-2 else y+2

        wattroff(self.menu_win, A_BOLD)
        box(self.menu_win)
        wrefresh(self.menu_win)
        wmove(self.game_win, position[0], position[1])

    def finish_view(self) -> None:
        """
        Reverts the changes made to the terminal and exits the interface.
        :return:
        """
        echo()
        nocbreak()
        keypad(self.standard_screen, False)

        endwin()

    def process_key_input(self, key: int) -> int:
        """
        Key processor for the game area. Given the integer key code provided, will call appropriate functions.
        Note: You will need the keypad function set to True.
        :param key: Integer key code.
        :return: Integer with action information: 0-Exit, 1-Valid action, 2-Unrecognized key
        """
        pos = getyx(self.game_win)
        if (key == ord('q')) or (key == ord('Q')):
            return 0
        elif key == KEY_UP:
            if (pos[0] > 1) and self.in_menu == 0:
                wmove(self.game_win, pos[0]-1, pos[1])
                self.write('UP   ')
            elif self.in_menu != 0:
                self.select = self.menus[self.in_menu].__len__() if self.select == 1 else self.select - 1
                self.render_menu(self.menus[self.in_menu], self.select)
                self.write(self.select)
            return 1

        elif key == KEY_DOWN:

            if pos[0] < self.mf.height and self.in_menu == 0:
                wmove(self.game_win, pos[0]+1, pos[1])
                self.write('DOWN ')
            elif self.in_menu != 0:
                self.select = 1 if self.select == self.menus[self.in_menu].__len__() else self.select + 1
                self.render_menu(self.menus[self.in_menu], self.select)
                self.write(self.select)
            return 1

        elif key == KEY_LEFT:

            if pos[1] > 2 and self.in_menu == 0:
                wmove(self.game_win, pos[0], pos[1]-3)
                self.write('LEFT ')
            elif self.in_menu != 0:
                curs_set(True)
                # wmove(self.game_win, 1, self.mf.side*3-1)
                self.in_menu = 0
                self.render_menu(self.menus[1], self.select, True)
            return 1

        elif key == KEY_RIGHT:

            if pos[1] < self.mf.side*3-2 and self.in_menu == 0:
                wmove(self.game_win, pos[0], pos[1]+3)
                self.write('RIGHT')
            elif self.in_menu == 0:
                curs_set(False)
                self.in_menu = 1
                self.render_menu(self.menus[self.in_menu], self.select)
            return 1

        elif (key == ord(' ')) or (key == 10):

            if self.in_menu:
                self.write('MENU*')
                return self.key_action_menu(self.menus[self.in_menu][self.select - 1])

            else:
                self.write('OPEN ')
                return self.key_action_field('OPEN')

        elif (key == ord('f')) or (key == ord('F')):
            self.key_action_field('FLAG')
            self.write('FLAG ')
            return 1
        elif (key == ord('m')) or (key == ord('M')):
            # self.main_menu()
            self.in_menu = 1
            curs_set(False)
            self.render_menu(self.main_menu, 1)
            return 1
        else:
            return 2

    def write(self, string: str, y=0, x=0) -> None:
        pos = getyx(self.game_win)
        mvwaddstr(self.game_win, y, x, string, A_BOLD)

        clrtoeol()
        wmove(self.game_win, pos[0], pos[1])

    def key_action_field(self, action: str) -> int:
        """
        Open or flag cells in the current cursor position.
        :param action: String indicating the required action: OPEN or FLAG
        :return:
        """
        pos = getyx(self.game_win)
        y = pos[0]
        x = (pos[1] + 1) // 3

        if action == 'OPEN':
            self.mf.open_cell(x, y)
            self.render_field(self.mf)
        elif action == 'FLAG':
            self.mf.flag_cell(x, y)
            self.render_field(self.mf)
        doupdate()
        return 1

    def key_action_menu(self, action: str) -> int:

        if self.in_menu == 1:  # Main menu
            if action == 'START GAME!':
                self.mf = MinedField(self.mf.side, self.mf.height, self.mf.amount)
                self.render_field(self.mf)
                doupdate()

            elif action == 'SETTINGS':
                self.in_menu = 2
                self.select = 1

                self.render_menu(self.menus[self.in_menu], 1)

            elif action == 'ABOUT':
                self.in_menu = 3
                self.select = 1
                self.render_menu(self.menus[self.in_menu], 1)

            elif action == 'EXIT':
                return 0

        elif self.in_menu == 2:  # Settings menu
            if action == 'APPLY':
                pass

            elif action == self.menus[2][0]:
                # new_side = get_number_menu()
                x = self.get_number_menu(1)
                self.write(str(x))
                self.finish_view()
                print(str(x))
                input()
                return 0

            elif action == '<< BACK <<':
                self.in_menu = 1
                self.select = 1
                self.render_menu(self.menus[1], 1)

        elif self.in_menu == 3:  # About menu
            if action == 'github.com/rtss00/py-sweeper':
                webbrowser.open('https://github.com/rtss00/py-sweeper')

            elif action == '<< BACK <<':
                self.in_menu = 1
                self.select = 1
                self.render_menu(self.menus[1], 1)

    def get_number_menu(self, option):
        current_pos = getyx(self.game_win)

        base_position = (getmaxyx(self.menu_win)[1] - self.menus[2][option].__len__() - 1) // 2
        offset = self.menus[2][option].__len__() - 3
        x = base_position + offset

        wmove(self.menu_win, 1, x)

        echo()
        curs_set(True)
        first = getch()
        second = getch()
        noecho()
        curs_set(False)

        wmove(self.game_win, current_pos[0], current_pos[1])

        try:
            return int(chr(first) + chr(second))
        except ValueError:
            return 1
