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
        self.calculate_numbers()

    def translate_position(self, x: int, y: int) -> int:
        if (x <= self.side) and (y <= self.height):
            return self.side*(y-1)+(x-1)
        else:
            return -1

    def print_field(self):
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.translate_position(x,y)]
                if point.type == 'EMPTY':
                    sym = ' '
                elif point.type == 'NUMBER':
                    sym = 'n'
                else:
                    sym = 'X'
                print('[{}]'.format(sym), end='')
            print()

    def check_type(self, x: int, y: int) -> str:
        if (0 <= y <= self.height-1) and (0 <= x <= self.side):
            return self.field[self.translate_position(x, y)].type
        else:
            return 'EMPTY'

    def count_bombs(self, x: int, y: int) -> int:
        count = 0;
        for i in range(-1, 2):
            for j in range(-1, 2):
                if self.check_type(x+i, y+j) == 'BOMB':
                    count += 1;
        return count

    def calculate_numbers(self):
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.translate_position(x, y)]
                number = self.count_bombs(x, y)
                if (point.type != 'BOMB') and (number > 0):
                    point.type = 'NUMBER'
                    point.number = number
