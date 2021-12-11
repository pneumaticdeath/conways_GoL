#!/usr/bin/env python3

import argparse
import life
import pygame
import random
import sys
import time

bg_color = 255, 255, 255
cell_color = 0, 0, 127

parser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument('--width', type=int, default=80, help='Initial width of game')
parser.add_argument('--height', type=int, default=60, help='Initial height of game')
parser.add_argument('--fill', type=int, default=40, help='Percentage fill of initial field')
parser.add_argument('--window', default='800x600',  help='Dimensions of window')
parser.add_argument('--delay', type=float, default=0.1, help='Delay in seconds between generation updates')
parser.add_argument('--stagnation', type=int, default=10, help='Exit if no change in number of living cells for this many generations')
parser.add_argument('--stagnation-window', type=int, default=3)

args = parser.parse_args()

delim = None
for poss in (',', 'x'):
    if poss in args.window:
        delim = poss
        break

if delim is None:
    parser.usage()
    sys.exit(1)

try:
    window_size = tuple([int(x) for x in args.window.split(delim)])
except:
    sys.stderr.write('Invalid window size {}\n'.format(args.window))
    parser.usage()
    sys.exit(1)

initial_cells = set()
for y in range(args.height):
    for x in range(args.width):
        if random.uniform(0,100) < args.fill:
            initial_cells.add((x,y))

game = life.Life(initial_cells)

bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y = game.getBoundingBox()
print('{}, {}, {}, {}'.format(bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y))

pygame.init()

window = pygame.display.set_mode(window_size)

def display(game):
    global bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y
    window_width, window_height = window_size
    window.fill(bg_color)

    min_x, min_y, max_x, max_y = game.getBoundingBox()
    if min_x < bounding_min_x: bounding_min_x = min_x
    if min_y < bounding_min_y: bounding_min_y = min_y
    if max_x > bounding_max_x: bounding_max_x = max_x
    if max_y > bounding_max_y: bounding_max_y = max_y

    game_width = (bounding_max_x-bounding_min_x) + 1
    game_height = (bounding_max_y-bounding_min_y) + 1

    scale = min(window_width/game_width, window_height/game_height)
    print('Generation {}: scale: {} live cells: {}'.format(game.getGeneration(), scale, len(game.getLiveCells())))
    window_pixels = {}

    game_mid_x = int((bounding_max_x + bounding_min_x)/2)
    game_mid_y = int((bounding_max_y + bounding_min_y)/2)

    window_mid_x = int(window_width/2 + 0.5)
    window_mid_y = int(window_height/2 + 0.5)

    for game_x, game_y in game.getLiveCells():
        x = window_mid_x + int(scale*(game_x-game_mid_x-0.5))
        y = window_mid_y + int(scale*(game_y-game_mid_y-0.5))

        if scale <= 2:
            pix = x,y
            if pix in window_pixels:
                window_pixels[pix] += 1
            else:
                window_pixels[pix] = 1
        else:
            pygame.draw.circle(window, cell_color, (x, y), max(1, 0.45*scale))
            
    if scale <= 2:
        max_dens = max([d for d in window_pixels.values()])
        for coord, d in window_pixels.items():
            color = tuple([int((bg_color[c]*(max_dens-d)+cell_color[c]*d)/max_dens) for c in range(3)])
            pygame.draw.circle(window, color, coord, 1)

    
    pygame.display.flip()


stagnation = 0
live_cells_history = [len(game.getLiveCells())]

while game.getLiveCells() and (stagnation < args.stagnation or args.stagnation < 1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)

    display(game)
    game.step()
    if len(game.getLiveCells()) in live_cells_history:
        stagnation += 1
    else:
        stagnation = 0

    live_cells_history.append(len(game.getLiveCells()))
    if len(live_cells_history) > args.stagnation_window:
        live_cells_history = live_cells_history[-args.stagnation_window:]

    time.sleep(args.delay)

if game.getLiveCells():
    print("Stagnation")
    time.sleep(10)
