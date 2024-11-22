#!/usr/bin/env python3

import sys


class Life(object):
    def __init__(self, live_cells=None):
        self._live = set()
        self._gen_counter = 0
        if live_cells is not None:
            self.addLiveCells(live_cells)

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
        self._live = next_gen
        self._gen_counter += 1

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


if __name__ == '__main__':
    import argparse
    import random
    import time

    parser = argparse.ArgumentParser('life')
    parser.add_argument('--size', default="30,30", help="Initial size of grid, default 30,30")
    parser.add_argument('--fill', type=int, default=50, help="percent of initial cells to be filled between 0 and 100")
    parser.add_argument('--delay', type=float, default=0.5, help="Delay in seconds after every generation")

    args = parser.parse_args()

    delim = None
    for poss_delimeter in [',', 'x']:
        if poss_delimeter in args.size:
            delim = poss_delimeter
            break

    if delim is None:
        parser.usage()
        sys.exit(1)

    size_x, size_y = [int(n) for n in args.size.split(delim)]

    initial_gen = set()
    for y in range(size_y):
        for x in range(size_x):
            if random.uniform(0, 100) <= args.fill:
                initial_gen.add((x, y))

    def display(game):
        min_x, min_y, max_x, max_y = game.getBoundingBox()

        print('({}, {}) -> ({}, {})'.format(min_x, min_y, max_x, max_y))
        print('+{}+'.format('-' * (2 * (max_x - min_x) + 1)))
        cells = game.getLiveCells()
        for y in range(min_y, max_y + 1):
            line = ' '.join(['*' if (x, y) in cells else ' ' for x in range(min_x, max_x + 1)])
            print('|{}|'.format(line))
        print('+{}+'.format('-' * (2 * (max_x - min_x) + 1)))

    life = Life(initial_gen)
    cells = life.getLiveCells()
    last_gen = set()
    while cells and cells != last_gen:
        print('Generation {}'.format(life.getGeneration()))
        display(life)
        life.step()
        last_gen = cells
        cells = life.getLiveCells()
        time.sleep(args.delay)
