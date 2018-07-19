from field_class import MinedField
from sty import fg  # , bg, ef, rs


mf = MinedField(10, 10, 12)
mf.print_solved_field()

print(fg(34) + "\nMines in positions:" + fg.rs, end=' ')
mf.mines.sort()
for i in mf.mines:
    print(i, end=' ')
print()

inp = ''
while inp != 'q':
    inp = input('Enter position X')
    if inp != 'q':
        inp = int(inp)
        y = int(input("Enter position Y"))
        print("Position given: {}".format(mf.translate_position(inp, y)))
        for cell in mf.get_neighbours(inp, y):
            print('{},'.format(cell), end=' ')
        print()
# print('Full field list:')
# count = 0
# for i in mf.field:
#    print("{}: {}, {} bombs nearby".format(count, i.type, mf.count_bombs()));
#    count += 1
