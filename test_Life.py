import life
import os
import sys

for filename in sys.argv[1:]:
    test = life.load(filename)
    test.save('Foo.life', life.FMT_LIFE)
    foo = life.load('Foo.life')
    min_x, min_y, max_x, max_y = test.getBoundingBox()
    test_cells = set([(x - min_x, y - min_y) for x, y in test.getLiveCells()])
    min_x, min_y, max_x, max_y = foo.getBoundingBox()
    foo_cells = set([(x - min_x, y - min_y) for x, y in foo.getLiveCells()])
    if test_cells != foo_cells:
        print(f'{filename} FAILED')
        sys.exit(1)
    else:
        print(f'{filename} passed')

os.unlink('Foo.life')
sys.exit(0)

