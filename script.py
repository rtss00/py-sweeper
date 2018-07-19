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
    x = input('Enter position X')
    if x != 'q':
        x = int(x)
        y = int(input("Enter position Y"))
        mf.open_cell(x, y)
        os.system('cls' if os.name == 'nt' else 'clear')
        mf.print_field()
        print('----------------------------------')
        mf.print_solved_field()
