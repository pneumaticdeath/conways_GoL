#!/usr/bin/env python

import argparse
import life

parser = argparse.ArgumentParser('run_for.py')
parser.add_argument('--generations', type=int, default=1000)
parser.add_argument('--output', default='output.rle')
parser.add_argument('--history', type=int, default=-1)
parser.add_argument('seed')

args = parser.parse_args()

game = life.load(args.seed)
game.setHistoryLimit(args.history)

try:
    while game.getGeneration() < args.generations:
        game.step()
        if game.getLiveCells() in game.getHistory():
            print('Loop at generation {}'.format(game.getGeneration()))
            break
except KeyboardInterrupt:
    print('Interrupted at generation {}'.format(game.getGeneration()))

game.save(args.output, life.FMT_RLE)
