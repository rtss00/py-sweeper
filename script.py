from field_class import MinedField
from sty import fg  # , bg, ef, rs
import os

# os.system('cls' if os.name == 'nt' else 'clear')
mf = MinedField(10, 10, 12)
# mf.print_solved_field()
mf.print_field()
print(fg(34) + "\nMines in positions:" + fg.rs, end=' ')
mf.mines.sort()
for i in mf.mines:
    print(i, end=' ')
print()

x = ''
while x != 'q':
    x = input('Enter position X')
    if x != 'q':
        x = int(x)
        y = int(input("Enter position Y"))
        mf.open_cell(x, y)
        os.system('cls' if os.name == 'nt' else 'clear')
        mf.print_field()
        mf.print_solved_field()
# print('Full field list:')
# count = 0
# for i in mf.field:
#    print("{}: {}, {} bombs nearby".format(count, i.type, mf.count_bombs()));
#    count += 1
