from field_class import MinedField;
from sty import fg, bg, ef, rs


mf = MinedField(10, 10, 12)
mf.print_field()

print(fg(34) + "\nMines in positions:" + fg.rs, end=' ')
mf.mines.sort()
for i in mf.mines:
    print(i, end=' ')
print()

# print('Full field list:')
# count = 0
# for i in mf.field:
#    print("{}: {}, {} bombs nearby".format(count, i.type, mf.count_bombs()));
#    count += 1
