# py-sweeper
**Minesweeper** implemented in _Python3_. Just for fun. Open to suggestions!  
I wanted to implement Minesweeper at some point in  my life and here it is.
All the logic is implemented in Python, and I used UniCurses for the GUI in the terminal. UniCurses feels quite a bit like a mess, but I had to make a choice if I wanted this to be cross-platform. I'm sure it'd be more "elegant" if implemented solely in curses or ncurses.
This was quite a nice little challenge. Hope you have fun with it.

## Requirements
The game requires the UniCurses library to work with the terminal. You can download it from the [Python Package Index](https://pypi.org/project/UniCurses/). No need to install it, just make sure the unicurses.py file is in the same directory from where you're running everything.  
Also, you should include feluxe's [sty](https://github.com/feluxe/sty) package in the same directory **ONLY** if you're curious and are working with previous versions of the game for some reason. It was used for a previous version of the game, and removed since then.

## How to play?
Up to now, the size of the field and the amount of mines is fixed, but this should be updated soon.

### Moving the cursor, opening cells
Use the arrow keys to move the cursor over the field, and press space to open a cell. If there's a mine underneath, it's game over. If you manage to open every cell that doesn't contain a mine, you win.
If you see a number, e.g. 3 in an opened cell, it means that theres that amount of bombs in the neighbouring cells, including the corners.  

### Flags
Press F to flag or unflag an unopened cell. Flagged cells cannot be opened, and remind you where bombs are, or might be. _Flags are important!_ They can make the field faster to clean: let's say a cell has the number 2 in it, and it's surrounded by two flags (exactly). If you try to reopen the cell with the number 2, every single neighbour cell will open.
This makes things very fast to solve once you can determine where bombs are, but remember that if the flags are not on top bombs, all the other cells will open, including the ones with bombs!
