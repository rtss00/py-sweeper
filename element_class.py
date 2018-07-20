from sty import fg


class Element:
    types = ('BOMB', 'EMPTY', 'NUMBER')
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

    def __init__(self, elem_type):
        if elem_type in self.types:
            self.type = elem_type
        else:
            self.type = 'EMPTY'
        self.flagged = False
        self.opened = False
        self.number = 0
        self.graphic = ' ' if self.type == 'EMPTY' else 'X'

    def flag(self):
        # only flag if it's un-flagged or not open.
        self.flagged = True if (not self.flagged) and (not self.opened) else False

    def open(self):
        # only open if it's not flagged
        self.opened = True if not self.flagged else False

    def change_type(self, _type, number=0):
        if _type == 'BOMB':
            self.type = 'BOMB'
            self.graphic = 'X'
        elif _type == 'NUMBER':
            self.type = 'NUMBER'
            self.graphic = fg(self.color_dic[number]) + str(number) + fg.rs
            self.number = number
        else:
            self.type = 'EMPTY'
            self.graphic = ' '

