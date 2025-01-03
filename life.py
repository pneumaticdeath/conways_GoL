#!/usr/bin/env python3

import os
import re
import sys

FMT_LIFE = 1
FMT_CELLS = 2
FMT_RLE = 3


class Life(object):
    def __init__(self, live_cells=None, history_limit=-1):
        self.clear()
        self._history_limit = history_limit
        if live_cells is not None:
            self.addLiveCells(live_cells)

    def clear(self):
        self._live = set()
        self._history = []
        self._meta = {}
        self._gen_counter = 0

    def setHistoryLimit(self, limit):
        self._history_limit = limit

    def getHistoryLimit(self):
        return self._history_limit

    def setMetaData(self, key, value):
        self._meta[key] = value

    def clearMetaData(self, key=None):
        if key is None:
            self._meta = {}
        else:
            if key in self._meta:
                del self._meta[key]

    def addHeader(self, header):
        if 'headers' not in self._meta:
            self._meta['headers'] = []
        self._meta['headers'].append(header)

    def getHeaders(self):
        return self._meta.get('headers', [])

    def getMetaData(self, key=None, default=None):
        if key is not None:
            return self._meta.get(key, default)
        else:
            return self._meta

    def addComment(self, comment):
        if 'comments' not in self._meta:
            self._meta['comments'] = []
        self._meta['comments'].append(comment)

    def clearComments(self):
        self._meta['comments'] = []

    def getComments(self):
        return self._meta.get('comments', [])

    def addLiveCells(self, cells):
        for cell in cells:
            self._live.add(cell)

    def removeLiveCells(self, cells):
        for cell in cells:
            if cell in self._live:
                self._live.remove(cell)

    def orderedCells(self):
        min_x, min_y, max_x, max_y = self.getBoundingBox()
        width = max_x - min_x + 1
        cells = list(self._live)

        def keyfunc(cell):
            return (cell[1] - min_y) * width + cell[0] - min_x

        cells.sort(key=keyfunc)
        return cells

    def neighbors(self, cell):
        x, y = cell
        for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
            yield (x + dx, y + dy)

    def getLiveCells(self):
        return self._live

    def getHistory(self):
        return self._history

    def getGeneration(self):
        return self._gen_counter

    def step(self):
        next_gen = set()
        neighbor_count = {}
        for cell in self._live:
            for neighbor in self.neighbors(cell):
                if neighbor in neighbor_count:
                    neighbor_count[neighbor] += 1
                else:
                    neighbor_count[neighbor] = 1
        for cell, count in neighbor_count.items():
            if count == 3 or count == 2 and cell in self._live:
                next_gen.add(cell)

        if self._history_limit != 0:
            self._history.append(self._live)
        if self._history_limit > 0 and len(self._history) > self._history_limit:
            self._history = self._history[-self._history_limit:]
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
            elif filename.lower().endswith('.cells') or filename.lower().endswith('.cells.txt'):
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
                    self.addComment(line[x + 1:])
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
        line_number = 0
        for line in lines:
            line_number += 1
            if line.startswith('!'):
                if line_number == 1:
                    self._meta['description'] = line[1:]
                elif line_number == 2:
                    self._meta['author'] = line[1:]
                else:
                    self.addComment(line[1:])
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
            if line.startswith('#N'):
                self._meta['description'] = line[2:]
                continue
            elif line.startswith('#O'):
                self._meta['author'] = line[2:]
                continue
            elif line.startswith('#C'):
                self.addComment(line[2:])
                continue
            elif line.startswith('#'):
                headers.append(line[1:])
                continue
            elif line.lstrip().startswith('x'):
                match = re.search(r'x *= *([0-9]+), *y *= *([0-9]+)', line)
                if not match:
                    print(f'Unable to parse header line "{line.strip()}"')
                else:
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
        if x > max_x:
            max_x = x
        if max_x != size_x or y != size_y:
            print(f'Got pattern of {max_x}x{y} but expected {size_x}x{size_y}')
        self._meta['headers'] = headers
        self._meta['width'] = size_x
        self._meta['height'] = size_y
        self._live = newCells

    def save(self, filename, format=FMT_LIFE):
        if format == FMT_LIFE:
            return self.saveLifeFile(filename)
        elif format == FMT_CELLS:
            return self.saveCellsFile(filename)
        elif format == FMT_RLE:
            return self.saveRLEFile(filename)
        else:
            return False

    def saveLifeFile(self, filename):
        min_x, min_y, max_x, max_y = self.getBoundingBox()
        if not filename.endswith('.life') and not filename.endswith('.life.txt'):
            filename += '.life.txt'
        with open(filename, 'w') as f:
            if 'description' in self._meta:
                description = self._meta['description']
                f.write(f'# {description}')
                if not description.endswith('\n'):
                    f.write('\n')
            if 'author' in self._meta:
                author = self._meta['author']
                f.write(f'# Author: {author}')
                if not author.endswith('\n'):
                    f.write('\n')
            if 'filename' in self._meta:
                orig_filename = self._meta['filename']
                f.write(f'# Loaded from "{os.path.basename(orig_filename)}"\n')
            elif 'height' in self._meta and 'width' in self._meta:
                orig_height = self._meta['height']
                orig_width = self._meta['width']
                f.write(f'# Height: {orig_height}   Width: {orig_width}')
                if 'fill' in self._meta:
                    fill = self._meta['fill']
                    f.write(f'   Fill: {fill}')
                f.write('\n')
            f.write(f'# Generation {self.getGeneration()}\n')
            f.write(f'# Bounding Box ({min_x}, {min_y}) -> ({max_x}, {max_y})\n')
            for comment in self.getComments():
                if comment.startswith('#'):
                    f.write(comment)
                else:
                    f.write('# ')
                    if comment.startswith('!'):
                        f.write(comment[1:])
                    else:
                        f.write(comment)
                if not comment.endswith('\n'):
                    f.write('\n')

            cells = self.getLiveCells()
            if min_y is not None:
                for y in range(min_y, max_y + 1):
                    for x in range(min_x, max_x + 1):
                        f.write('*' if (x, y) in cells else ' ')
                    f.write('\n')
        return True

    def saveCellsFile(self, filename):
        min_x, min_y, max_x, max_y = self.getBoundingBox()
        if not filename.endswith('.cells') and not filename.endswith('.cells.txt'):
            filename += '.cells.txt'
        with open(filename, 'w') as f:
            if 'description' in self._meta:
                description = self._meta['description']
                f.write(f'!{description}')
                if not description.endswith('\n'):
                    f.write('\n')
            if 'author' in self._meta:
                author = self._meta['author']
                f.write(f'!{author}')
                if not author.endswith('\n'):
                    f.write('\n')
            if 'filename' in self._meta:
                orig_filename = self._meta['filename']
                f.write(f'! {os.path.basename(orig_filename)}\n')
            for comment in self.getComments():
                if comment.startswith('!'):
                    f.write(comment)
                else:
                    f.write('!')
                    if comment.startswith('#'):
                        f.write(comment[1:])
                    else:
                        f.write(comment)
                if not comment.endswith('\n'):
                    f.write('\n')
            cells = self.getLiveCells()
            if min_y is not None:
                for y in range(min_y, max_y + 1):
                    for x in range(min_x, max_x + 1):
                        f.write('O' if (x, y) in cells else '.')
                    f.write('\n')
        return True

    def saveRLEFile(self, filename, max_line_length=79):
        min_x, min_y, max_x, max_y = self.getBoundingBox()
        if not filename.endswith('.rle') and not filename.endswith('.rle.txt'):
            filename += '.rle.txt'
        with open(filename, 'w') as f:
            if 'description' in self._meta:
                if self._meta['description'].startswith('#N'):
                    f.write(self._meta['description'])
                else:
                    description = self._meta['description']
                    f.write(f'#N{description}')
                if not description.endswith('\n'):
                    f.write('\n')
            if 'author' in self._meta:
                author = self._meta['author']
                if author.startswith('#O'):
                    f.write(author)
                else:
                    f.write(f'#O{author}')
                if not author.endswith('\n'):
                    f.write('\n')
            for comment in self.getComments():
                if comment.startswith('#C'):
                    f.write(comment)
                else:
                    f.write('#C')
                    if comment.startswith('!'):
                        f.write(comment[1:])
                    else:
                        f.write(comment)
                if not comment.endswith('\n'):
                    f.write('\n')
            if 'filename' in self._meta:
                orig_filename = self._meta['filename']
                f.write(f'#C originally loaded from {os.path.basename(orig_filename)}\n')
            if self.getGeneration() > 0:
                gen = self.getGeneration()
                f.write(f'#C at generation {gen}  Bounded by ({min_x}, {min_y}) -> ({max_x}, {max_y})\n')
            f.write('x = {}, y = {}, rule = b3/s23\n'.format(max_x - min_x + 1, max_y - min_y + 1))
            syms_rle = self.findRLE()
            line = ''
            for sym, sym_count in syms_rle:
                if sym_count > 1:
                    new_blob = f'{sym_count}{sym}'
                else:
                    new_blob = sym
                if len(line) + len(new_blob) > max_line_length:
                    f.write(line)
                    f.write('\n')
                    line = new_blob
                else:
                    line += new_blob
            if line:
                f.write(line)
                f.write('\n')
        return True

    def findRLE(self):
        min_x, min_y, max_x, max_y = self.getBoundingBox()
        sym_rle = []
        last_y = 0
        last_x = -1
        for cell in self.orderedCells():
            rel_x = cell[0] - min_x
            rel_y = cell[1] - min_y
            if rel_y > last_y:
                sym_rle.append(('$', rel_y - last_y))
                if rel_x > 0:
                    sym_rle.append(('b', rel_x))
                sym_rle.append(('o', 1))
                last_y = rel_y
            elif rel_x == last_x + 1:
                # It's non-obvious, but if sym_rle has anything
                # the last symbol will always be 'o'
                if sym_rle:
                    sym_rle[-1] = ('o', sym_rle[-1][1] + 1)
                else:
                    sym_rle.append(('o', 1))
            else:
                sym_rle.append(('b', (rel_x - last_x) - 1))
                sym_rle.append(('o', 1))
            last_x = rel_x
        sym_rle.append(('!', 1))
        return sym_rle


def load(filename):
    game = Life()
    game.load(filename)
    return game


def display(game):
    min_x, min_y, max_x, max_y = game.getBoundingBox()

    print('({}, {}) -> ({}, {})'.format(min_x, min_y, max_x, max_y))
    print('+{}+'.format('-' * (2 * (max_x - min_x) + 1)))
    cells = game.getLiveCells()
    for y in range(min_y, max_y + 1):
        line = ' '.join(['*' if (x, y) in cells else ' ' for x in range(min_x, max_x + 1)])
        print('|{}|'.format(line))
    print('+{}+'.format('-' * (2 * (max_x - min_x) + 1)))


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

    try:
        while life.getLiveCells() and life.getLiveCells() not in life.getHistory():
            print('Generation {}'.format(life.getGeneration()))
            display(life)
            life.step()
            time.sleep(args.delay)
        if life.getLiveCells():
            print('Stagnated at generation {}'.format(life.getGeneration()))
            display(life)
        else:
            print('Extinct at generation {}'.format(life.getGeneration()))
    except KeyboardInterrupt:
        print('Interrupted at gneeration {}'.format(life.getGeneration()))
        if life.getLiveCells():
            display(life)
