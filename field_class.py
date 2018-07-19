import func
from element_class import Element
from sty import fg  # bg, ef, rs


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
        self.to_open = a * b - amount

    def t_pos(self, x: int, y: int) -> int:  # translate_position
        if (x <= self.side) and (y <= self.height):
            return self.side*(y-1)+(x-1)
        else:
            return -1

    def print_solved_field(self):
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.t_pos(x, y)]
                sym = point.graphic

                text = '[{}]'.format(sym)
                print(text, end='')
            print()

    def print_field(self):
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.t_pos(x, y)]
                if point.opened:
                    sym = point.graphic
                elif point.flagged:
                    sym = fg(8) + 'F' + fg.rs
                else:
                    sym = '?'
                print("[{}]".format(sym), end='')
            print()

    def flag_cell(self, x: int, y: int):
        point = self.field[self.t_pos(x, y)]
        point.flag()

    def open_cell(self, x: int, y: int):
        point = self.field[self.t_pos(x, y)]
        if (point.type == 'NUMBER') or (point.type == 'BOMB'):
            if not point.opened:
                self.to_open -= 1
            point.open()
            print('opened ({},{}), left {}'.format(x, y, str(self.to_open)))
        elif (point.type == 'EMPTY') and (not point.opened) and (not point.flagged):
            if not point.opened:
                self.to_open -= 1
            point.open()
            print('opened ({},{}), left {}'.format(x, y, str(self.to_open)))
            neighbours = self.get_neighbours(x, y)
            for cell in neighbours:
                new_x = cell % self.side + 1
                new_y = ((cell - (new_x - 1)) // self.side) + 1
                self.open_cell(new_x, new_y)

    def check_type(self, x: int, y: int) -> str:
        if (1 <= y <= self.height-1) and (1 <= x <= self.side):
            return self.field[self.t_pos(x, y)].type
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
                    new_pos = self.t_pos(x+i, y+j)
                    ret.append(new_pos)
        return ret

    def calculate_numbers(self):
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.t_pos(x, y)]
                number = self.count_bombs(x, y)
                if (point.type != 'BOMB') and (number > 0):
                    point.change_type('NUMBER', number)
