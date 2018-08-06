from unicurses import *
from interface import View


def main():
    view = View(16, 16, 12)
    while True:
        if view.process_key_input(wgetch(view.game_win)) == 0:
            break
    view.finish_view()


if __name__ == "__main__":
    main()
