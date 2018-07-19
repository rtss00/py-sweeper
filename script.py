from field_class import MinedField
from element_class import Element
# from sty import fg, bg, ef, rs
import os

os.system('cls' if os.name == 'nt' else 'clear')
mf = MinedField(5, 5, 5)
mf.print_field()
print('TO OPEN: {}   ---------------------'.format(mf.to_open))
mf.print_solved_field()


x = ''
point = Element
while x != 'q' and mf.to_open != 0:
    x = input('Enter position X or \'q\' to leave ')
    if x != 'q':
        x = int(x)
        y = int(input("Enter position Y "))
        act = input("Enter action: [o]pen or [f]lag ")

        if act == 'f':
            mf.flag_cell(x, y)
        else:
            mf.open_cell(x, y)
            point = mf.field[mf.t_pos(x, y)]
            if point.type == 'BOMB':
                break
        os.system('cls' if os.name == 'nt' else 'clear')
        mf.print_field()
        print('TO OPEN: {}   ---------------------'.format(mf.to_open))
        mf.print_solved_field()

if (mf.to_open == 0) and (x != 'q') and (point.type != 'BOMB'):
    print('WINNER!')
else:
    print('LOSER!')
