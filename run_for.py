#!/usr/bin/env python

import argparse
import life

parser = argparse.ArgumentParser('run_for.py')
parser.add_argument('--generations', type=int, default=1000)
parser.add_argument('--output', default='output.rle')
parser.add_argument('--history', type=int, default=-1)
parser.add_argument('--updates', type=int, default=0)
parser.add_argument('seed')

args = parser.parse_args()

game = life.load(args.seed)
game.setHistoryLimit(args.history)

format = life.FMT_RLE
if args.output.endswith('.cells') or args.output.endswith('.cells.txt'):
    format = life.FMT_CELLS
elif args.output.endswith('.life') or args.output.endswith('.life.txt'):
    format = life.FMT_LIFE

try:
    while game.getGeneration() < args.generations:
        game.step()
        if args.updates > 0 and game.getGeneration() % args.updates == 0:
            print('Generation {} has {} cells'
                  .format(game.getGeneration(), len(game.getLiveCells())))
        if game.getLiveCells() in game.getHistory():
            print('Loop at generation {}'.format(game.getGeneration()))
            break
except KeyboardInterrupt:
    print('Interrupted at generation {}'.format(game.getGeneration()))

game.save(args.output, format)
