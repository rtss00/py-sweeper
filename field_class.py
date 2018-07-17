import func
from element_class import Element


class MinedField:
    def __init__(self, a, b, amount):
        self.side = a
        self.height = b
        self.amount = amount if amount <= a*b else a*b
        self.mines = func.random_in_range(0, a*b-1, amount)
        self.field = []
        for i in range(0, a*b):  # a*b is out of range in the list, but range() doesn't include it.
            if i in self.mines:
                elem = Element('BOMB')
            else:
                elem = Element('EMPTY')
            self.field.append(elem)

    def translate_position(self, x: int, y: int) -> int:
        if (x <= self.side) and (y <= self.height):
            return self.side*(y-1)+(x-1)
        else:
            return -1

    def print_field(self):
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                sym = 'X' if self.field[self.translate_position(x, y)].type == 'BOMB' else ' '
                print('[{}]'.format(sym), end='')
            print()
