from field_class import MinedField;


mf = MinedField(10, 10, 12)
mf.print_field()

print("\nMines in positions:",end=' ')
mf.mines.sort()
for i in mf.mines:
    print(i, end=' ')
print()

