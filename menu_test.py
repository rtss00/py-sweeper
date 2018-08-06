from unicurses import *


choices = ['Start game', 'Settings', 'About', 'Exit']


def print_menu(window, selected):
    x = y = 2
    box(window)
    for position in range(0, choices.__len__()):
        if selected == position+1:  # We must add one to the position to get a 1-indexed choice list
            mvwaddstr(window, y, x, choices[position], A_REVERSE)
        else:
            mvwaddstr(window, y, x, choices[position])
        y += 1
    update_panels()  # Note that the window must be converted into a panel for this o work
    wrefresh(window)


screen = initscr()
clear()
noecho()
curs_set(False)
cbreak()

menu_window = newwin(10, 20, 0, 0)
keypad(screen, True)
new_panel(menu_window)
refresh()

cursor = 1
size = choices.__len__()

print_menu(menu_window, cursor)
doupdate()

while True:
    key = getch()

    if key == KEY_UP:
        cursor = size if cursor == 1 else cursor-1
    elif key == KEY_DOWN:
        cursor = 1 if cursor == size else cursor+1
    elif key == 10:
        if choices[cursor-1] == 'Exit':
            break
        mvwaddstr(screen, 20, 0, 'Selected: {}'.format(choices[cursor]))
        clrtoeol()
        wrefresh(menu_window)
    print_menu(menu_window, cursor)
    doupdate()

clear()
echo()
nocbreak()
curs_set(True)
keypad(screen, False)
endwin()
