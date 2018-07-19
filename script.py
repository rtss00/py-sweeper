from field_class import MinedField
from sty import fg  # , bg, ef, rs
import os

os.system('cls' if os.name == 'nt' else 'clear')
mf = MinedField(10, 10, 12)
mf.print_field()
print('----------------------------------')
mf.print_solved_field()


x = ''
while x != 'q':
    x = input('Enter position X or \'q\' to leave')
    if x != 'q':
        x = int(x)
        y = int(input("Enter position Y"))
        act = input("Enter action: [o]pen or [f]lag")

        if act == 'f':
            mf.flag_cell(x,y)
            print('flag state for ({},{}): {}'.format(x, y, mf.field[mf.t_pos(x, y)].flagged))
        else:
            mf.open_cell(x, y)
        os.system('cls' if os.name == 'nt' else 'clear')
        mf.print_field()
        print('----------------------------------')
        mf.print_solved_field()
