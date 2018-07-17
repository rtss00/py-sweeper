class Element:
    types = ('BOMB', 'EMPTY', 'NUMBER')

    def __init__(self, elem_type):
        if elem_type in self.types:
            self.type = elem_type
        else:
            self.type = 'EMPTY'
        self.flagged = False

