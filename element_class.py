# from sty import fg


class Cell:
    # Only valid cell types
    types = ('BOMB', 'EMPTY', 'NUMBER')
    # Color dictionary for previous versions
    # color_dic = {1: 21, 2: 2, 3: 1, 4: 19, 5: 52, 6: 14, 7: 5, 8: 11}

    def __init__(self, elem_type=None):
        """
        Initialize a Cell object, un-flagged, un-opened, with number 0 by default, with the given type.
        If no argument is passed, or the argument is not in Cell.types, The type will be set as 'EMPTY'.
        :param elem_type: Type of cell. Possible values: 'BOMB', 'NUMBER', 'EMPTY'
        """
        if elem_type in self.types:
            self.type = elem_type
        else:
            self.type = 'EMPTY'
        self.flagged = False
        self.opened = False
        self.number = 0
        self.graphic = ' ' if self.type == 'EMPTY' else 'X'

    def flag(self):
        """
        Flag cell.
        :return:
        """
        # only flag if it's un-flagged or not open.
        self.flagged = True if (not self.flagged) and (not self.opened) else False

    def open(self):
        """
        Open cell. Propagation not available at cell level, only at field level.
        :return: None
        """
        # only open if it's not flagged
        self.opened = True if not self.flagged else False

    def change_type(self, _type, number=0):
        """
        Changes the type of the cell to [_type]. If type wrong type is provided, the function has no effect.
        If [_type]=='NUMBER' the number on the cell will be changed to the passed argument. Otherwise it'll be set to 0
        :param _type: Type to change. Must be in Cell.types
        :param number: Value to set if [_type]=='NUMBER' (1 <= number <= 8 to maintain consistency). Default to 0.
        :return: None
        """
        if _type in self.types:
            self.type = _type
            self.graphic = ' '
            self.graphic = str(number) if _type == 'NUMBER' else 'X'
            self.number = number if _type == 'NUMBER' else 0



