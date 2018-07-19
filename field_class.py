import func
from element_class import Element
from sty import fg  # bg, ef, rs


class MinedField:
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
                point = self.field[self.translate_position(x, y)]
                if point.type == 'EMPTY':
                    sym = ' '
                elif point.type == 'NUMBER':
                    sym = str(point.number)
                else:
                    sym = 'X'
                text = '[' + fg(self.color_dic[int(sym)]) + sym + fg.rs + ']' if point.type == 'NUMBER' \
                    else '[{}]'.format(sym)
                print(text, end='')
            print()

    def check_type(self, x: int, y: int) -> str:
        if (1 <= y <= self.height-1) and (1 <= x <= self.side):
            return self.field[self.translate_position(x, y)].type
        else:
            return 'EMPTY'

    def count_bombs(self, x: int, y: int) -> int:
        count = 0
        for pos in self.get_neighbours(x, y):
            if self.field[pos].type == 'BOMB':
                count += 1
        return count

    def get_neighbours(self, x: int, y: int) -> list:
        ret = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (1 <= x+i <= self.side) and (1 <= y+j <= self.side):
                    new_pos = self.translate_position(x+i, y+j)
                    ret.append(new_pos)
        return ret

    def calculate_numbers(self):
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.translate_position(x, y)]
                number = self.count_bombs(x, y)
                if (point.type != 'BOMB') and (number > 0):
                    point.type = 'NUMBER'
                    point.number = number
