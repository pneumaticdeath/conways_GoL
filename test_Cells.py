import life
import os
import sys

for filename in sys.argv[1:]:
    test = life.load(filename)
    test.save('Foo.cells', life.FMT_CELLS)
    foo = life.load('Foo.cells')
    min_x, min_y, max_x, max_y = test.getBoundingBox()
    test_cells = set([(x - min_x, y - min_y) for x,y in test.getLiveCells()])
    if test_cells != foo.getLiveCells():
        print(f'{filename} FAILED')
        sys.exit(1)
    else:
        print(f'{filename} passed')

os.unlink('Foo.cells')
sys.exit(0)

