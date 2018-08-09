import func
from element_class import Cell
# from sty import fg  # bg, ef, rs


class MinedField:
    def __init__(self, a, b, amount):
        self.side = a
        self.height = b
        self.amount = amount if amount <= a*b else a*b
        self.mines = func.random_in_range(0, a*b-1, amount)
        self.field = []
        for i in range(0, a*b):  # a*b is out of range in the list, but range() doesn't include it.
            if i in self.mines:
                elem = Cell('BOMB')
            else:
                elem = Cell('EMPTY')
            self.field.append(elem)
        self.calculate_numbers()
        self.to_open = a * b - amount
        self.explode = False

    def t_pos(self, x: int, y: int) -> int:
        """
        Translates two-dimensional, 1-indexed position to 0-indexed one.

        :param x: Column in mined field between 1 and self.side
        :param y: Row in mined field between 1 and self.height
        :return: One-dimensional 0-indexed position to use in self.field
        """
        if (x <= self.side) and (y <= self.height):
            return self.side*(y-1)+(x-1)
        else:
            return -1

    def t_pos_rev(self, pos: int) -> list:
        """
        Translate 0-indexed one-dimensional position to 2 dimensional position in the mined field

        :param pos: One dimensional integer position in a 0-indexed list the represents the field matrix
        :return: List containing the x and y 1-indexed positions in the field matrix in the first 2 list elements
        """
        lst = list([pos % self.side + 1])
        lst.append(((pos - (lst[0] - 1)) // self.side) + 1)
        return lst

    def print_solved_field(self):
        """
        Prints the solved field. Useful for debugging purposes
        :return:
        """
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.t_pos(x, y)]
                sym = point.graphic

                text = '[{}]'.format(sym)
                print(text, end='')
            print()

    def print_field(self):
        """
        Prints the current state of the field, with flagged, open or closed cells, numbers and bombs.
        :return:
        """
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.t_pos(x, y)]
                if point.opened:
                    sym = point.graphic
                elif point.flagged:
                    # Color for previous versions
                    # sym = fg(8) + 'F' + fg.rs
                    sym = 'F'
                else:
                    sym = '?'
                print("[{}]".format(sym), end='')
            print()

    def flag_cell(self, x: int, y: int):
        """
        Flag the cell in the (x,y) position.
        :param x: Column in mined field between 1 and self.side
        :param y: Row in mined field between 1 and self.height
        :return:
        """
        point = self.field[self.t_pos(x, y)]
        point.flag()

    def open_cell(self, x: int, y: int):
        """
        Open the cell in the (x,y) position, with all the consequences.
        :param x: Column in mined field between 1 and self.side
        :param y: Row in mined field between 1 and self.height
        :return:
        """
        point = self.field[self.t_pos(x, y)]
        '''
        How this works:
        There are a few cases to take into consideration:
            -you select a non opened cell
                -it's a number, so you just open it and finish.
                -it's a bomb, so you just open and finish. You can control the game state from outside.
                -it's empty, so you open all its neighbour cells (recursive call).
            -you select an opened cell
                -it's a number and exactly [number] cells are flagged around it, so you open the un-flagged neighbours
        '''
        if not point.opened:

            if point.type == 'NUMBER':
                self.to_open -= 1
                point.open()
                self.explode = True

            elif (point.type == 'EMPTY') and (not point.flagged):
                self.to_open -= 1
                point.open()
                neighbours = self.get_neighbours(x, y)
                for cell in neighbours:
                    new_x = cell % self.side + 1
                    new_y = ((cell - (new_x - 1)) // self.side) + 1
                    self.open_cell(new_x, new_y)

            elif point.type == 'BOMB':
                point.open()

        elif point.type == 'NUMBER':
            # when we try to open a number with it's neighbour bombs flagged (and only this ones), the action
            # opens every neighbour cell except for the flagged ones. This is a common feature in
            # most minesweeper games
            neighbours = self.get_neighbours(x, y)
            flag_count = 0
            bomb_total = point.number
            for cell in neighbours:
                if self.field[cell].flagged:
                    flag_count += 1
            if flag_count == bomb_total:
                for cell in neighbours:
                    if not self.field[cell].opened:
                        new_pos = self.t_pos_rev(cell)
                        self.open_cell(new_pos[0], new_pos[1])

    def check_type(self, x: int, y: int) -> str:
        """
        Returns the type of the cell in the (x,y) position of the mined field.
        If x or y are not in the correct boundaries, the function returns 'EMPTY'

        :param x: Column in mined field between 1 and self.side
        :param y: Row in mined field between 1 and self.height
        :return:
        """
        if (1 <= y <= self.height-1) and (1 <= x <= self.side):
            return self.field[self.t_pos(x, y)].type
        else:
            return 'EMPTY'

    def count_bombs(self, x: int, y: int) -> int:
        """
        Bomb counter
        :param x: Column in mined field between 1 and self.side
        :param y: Row in mined field between 1 and self.height
        :return: Amount of bombs in the neighbouring cells of the (x,y) position, including itself.
        """
        count = 0
        for pos in self.get_neighbours(x, y):
            if (self.field[pos].type == 'BOMB') and (not self.field[pos].flagged):
                count += 1
        return count

    def get_neighbours(self, x: int, y: int) -> list:
        """
        Neighbour finder
        :param x: Column in mined field between 1 and self.side
        :param y: Row in mined field between 1 and self.height
        :return: List with the positions of all the neighbouring cells to (x,y), including itself.
        """
        ret = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if (1 <= x+i <= self.side) and (1 <= y+j <= self.height):
                    new_pos = self.t_pos(x+i, y+j)
                    ret.append(new_pos)
        return ret

    def calculate_numbers(self):
        """
        Calculates numbers for every position in the field, and changes all the relevant data for every Element object
        For use only with __init__
        :return:
        """
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                point = self.field[self.t_pos(x, y)]
                number = self.count_bombs(x, y)
                if (point.type != 'BOMB') and (number > 0):
                    point.change_type('NUMBER', number)

    def get_field(self):
        """
        Returns a multi-line field_str containing the current field (not colored).
        :return:
        """
        field_str = ''
        for y in range(1, self.height+1):
            for x in range(1, self.side+1):
                pos = self.t_pos(x, y)
                point = self.field[pos]
                if point.opened:
                    if point.type == 'NUMBER':
                        field_str += '[{}]'.format(point.number)
                    elif point.type == 'EMPTY':
                        field_str += '[ ]'
                    elif point.type == 'BOMB':
                        field_str += '[*]'
                else:
                    field_str += '[F]' if point.flagged else '[?]'
            field_str += "\n"
        return field_str
