class Element:
    types = ('BOMB', 'EMPTY', 'NUMBER')

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
        self.flagged = True if (not self.flagged) and (not self.open) else False

    def open(self):
        # only open if it's not flagged
        self.opened = True if not self.flagged else False

    def change_type(self, _type, number=0):
        if _type == 'BOMB':
            self.type = 'BOMB'
            self.graphic = 'X'
        elif _type == 'NUMBER':
            self.type = 'NUMBER'
            self.graphic = str(number)
        else:
            self.type = 'EMPTY'
            self.graphic = ' '
