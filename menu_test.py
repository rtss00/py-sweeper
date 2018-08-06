from unicurses import *


choices = ['Start Game', 'Settings', 'About', 'Exit']

selected = 1
size = choices.__len__()


def render_menu(window, opt, select):
    x = y = 1
    box(window)
    for i in range(0, size):
        if i+1 == select:
            mvwaddstr(window, y, x, opt[i], A_REVERSE)
        else:
            mvwaddstr(window, y, x, opt[i])
        y += 1
    wrefresh(window)
    update_panels()


screen = initscr()
clear()
noecho()
cbreak()
curs_set(False)

menu = newwin(10, 20, 0, 0)
keypad(screen, True)
render_menu(menu, choices, selected)
wrefresh(menu)

while True:
    key = getch()

    if key == KEY_UP:
        selected = size if selected == 1 else selected-1
        mvwaddstr(screen, 15, 0, 'Selected: {}'.format(selected))
        clrtoeol()

    elif key == KEY_DOWN:
        selected = 1 if selected == size else selected+1
        mvwaddstr(screen, 15, 0, 'Selected: {}'.format(selected))
        clrtoeol()

    elif key == 10:
        mvwaddstr(screen, 15, 0, 'Option: {}'.format(choices[selected-1]))
        clrtoeol()
        if choices[selected-1] == 'Exit':
            break

    render_menu(menu, choices, selected)

echo()
nocbreak()
curs_set(True)
keypad(screen, False)
endwin()
