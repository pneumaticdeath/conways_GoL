#!/usr/bin/env python3

import re
import sys


class Life(object):
    def __init__(self, live_cells=None):
        self.clear()
        if live_cells is not None:
            self.addLiveCells(live_cells)

    def clear(self):
        self._live = set()
        self._history = []
        self._meta = {}
        self._gen_counter = 0

    def addLiveCells(self, cells):
        for cell in cells:
            self._live.add(cell)

    def removeLiveCells(self, cells):
        for cell in cells:
            if cell in self._live:
                self._live.remove(cell)

    def neighbors(self, cell):
        x, y = cell
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if dx != 0 or dy != 0:
                    yield (x + dx, y + dy)

    def countNeighbors(self, cell):
        count = 0
        for neighbor in self.neighbors(cell):
            if neighbor in self._live:
                count += 1
        return count

    def getLiveCells(self):
        return self._live

    def getHistory(self):
        return self._history

    def getGeneration(self):
        return self._gen_counter

    def step(self):
        next_gen = set()
        cells_of_concern = set(self._live)  # make a copy of current live cells
        for cell in self._live:
            for neighbor in self.neighbors(cell):
                cells_of_concern.add(neighbor)
        for cell in cells_of_concern:
            n = self.countNeighbors(cell)
            if cell in self._live and n in [2, 3]:
                next_gen.add(cell)
            elif n == 3:
                next_gen.add(cell)
        self._history.append(self._live)
        self._live = next_gen
        self._gen_counter += 1

    def backwardsStep(self):
        """Move the simulation back one step.  Returns True if successful"""
        if self._history:
            self._live = self._history.pop()
            self._gen_counter -= 1
            return True
        return False

    def getBoundingBox(self):
        min_x, min_y, max_x, max_y = None, None, None, None
        for x, y in self._live:
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x > max_x:
                max_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_y is None or y > max_y:
                max_y = y
        return min_x, min_y, max_x, max_y

    def load(self, filename):
        self.clear()
        self._meta['filename'] = filename
        with open(filename, 'r') as f:
            if filename.lower().endswith('.life') or filename.lower().endswith('.life.txt'):
                self.loadLifeFile(f.readlines())
            elif filename.lower().endswith('.rle') or filename.lower().endswith('.rle.txt'):
                self.loadRLEFile(f.readlines())
            elif filename.lower().endswith('.cells') or filename.lower().endsiwth('.cells.txt'):
                self.loadCellsFile(f.readlines())
            else:
                raise TypeError('Unknown filetype')

    def loadLifeFile(self, lines):
        newCells = set()
        headers = []
        max_x = 0
        y = 0
        for line in lines:
            x = 0
            for c in line:
                if c == "#":
                    headers.append(line)
                    break
                elif not c.isspace():
                    newCells.add((x, y))
                x += 1
            if x > max_x:
                max_x = x
            y += 1
        self._meta['headers'] = headers
        self._meta['width'] = max_x
        self._meta['height'] = y
        self._live = newCells

    def loadCellsFile(self, lines):
        newCells = set()
        headers = []
        y = 0
        for line in lines:
            if line.startswith('!'):
                headers.append(line)
                continue
            x = 0
            for c in line:
                if c == '!':
                    break
                elif c == 'O':
                    newCells.add((x, y))
                elif c == '.':
                    pass
                elif c.isspace():
                    pass
                else:
                    print(f'Unknown character "{c}"')
                x += 1
            y += 1
        self._meta['headers'] = headers
        self._meta['width'] = x
        self._meta['height'] = y
        self._live = newCells

    def loadRLEFile(self, lines):
        newCells = set()
        headers = []
        y = 0
        x = 0
        size_y = 0
        size_x = 0
        max_x = 0
        count_str = ''
        done = False
        for line in lines:
            if line.startswith('#'):
                headers.append(line)
                continue
            elif line.lstrip().startswith('x'):
                match = re.search(r'x *= *([0-9]+), *y *= *([0-9]+)', line)
                if not match:
                    print(f'Unable to parse header line "{line.strip()}"')
                    continue
                groups = match.groups()
                size_x = int(groups[0])
                size_y = int(groups[1])
                continue
            else:
                for c in line:
                    if c.isdigit():
                        count_str += c
                    elif c.isspace():
                        pass
                    elif c in ['o', 'b', '$']:
                        if count_str != '':
                            count = int(count_str)
                            count_str = ''
                        else:
                            count = 1
                        if c == 'o':
                            for i in range(count):
                                newCells.add((x + i, y))
                            x += count
                        elif c == 'b':
                            x += count
                        elif c == '$':
                            if x > max_x:
                                max_x = x
                            x = 0
                            y += count
                    elif c == '!':
                        y += 1
                        done = True
                        break
                    else:
                        print(f'Unknown tag "{c}"')
            if done:
                break
        if not done:
            print('Did not find terminator')
        if max_x != size_x or y != size_y:
            print(f'Got pattern of {max_x}x{y} but expected {size_x}x{size_y}')
        self._meta['headers'] = headers
        self._meta['width'] = size_x
        self._meta['height'] = size_y
        self._live = newCells


if __name__ == '__main__':
    import argparse
    import random
    import time

    parser = argparse.ArgumentParser('life')
    parser.add_argument('--size', default="30,30",
                        help="Initial size of grid, default 30,30")
    parser.add_argument('--fill', type=int, default=50,
                        help="percent of initial cells to be filled between 0 and 100")
    parser.add_argument('--delay', type=float, default=0.5,
                        help="Delay in seconds after every generation")
    parser.add_argument('--load', help='Load initital state from a file')

    args = parser.parse_args()

    delim = None
    for poss_delimeter in [',', 'x']:
        if poss_delimeter in args.size:
            delim = poss_delimeter
            break

    if delim is None:
        parser.usage()
        sys.exit(1)

    life = Life()
    if args.load is None:
        initial_cells = set()
        size_x, size_y = [int(n) for n in args.size.split(delim)]
        for y in range(size_y):
            for x in range(size_x):
                if random.uniform(0, 100) <= args.fill:
                    initial_cells.add((x, y))
        life.addLiveCells(initial_cells)
    else:
        life.load(args.load)

    def display(game):
        min_x, min_y, max_x, max_y = game.getBoundingBox()

        print('({}, {}) -> ({}, {})'.format(min_x, min_y, max_x, max_y))
        print('+{}+'.format('-' * (2 * (max_x - min_x) + 1)))
        cells = game.getLiveCells()
        for y in range(min_y, max_y + 1):
            line = ' '.join(['*' if (x, y) in cells else ' ' for x in range(min_x, max_x + 1)])
            print('|{}|'.format(line))
        print('+{}+'.format('-' * (2 * (max_x - min_x) + 1)))

    cells = life.getLiveCells()
    last_gen = set()
    while cells and cells != last_gen:
        print('Generation {}'.format(life.getGeneration()))
        display(life)
        life.step()
        last_gen = cells
        cells = life.getLiveCells()
        time.sleep(args.delay)
