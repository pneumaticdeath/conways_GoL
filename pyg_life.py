#!/usr/bin/env python3

import argparse
import life
import pygame
import random
import sys
import time

bg_color = 0, 0, 0
cell_color = 0, 255, 0

parser = argparse.ArgumentParser(sys.argv[0])
parser.add_argument('--width', type=int, default=80, help='Initial width of game')
parser.add_argument('--height', type=int, default=60, help='Initial height of game')
parser.add_argument('--fill', type=int, default=40, help='Percentage fill of initial field')
parser.add_argument('--load', default=None, help='Optional file for initial pattern')
parser.add_argument('--window', default='800x600', help='Dimensions of window')
parser.add_argument('--delay', type=float, default=0.1, help='Delay in seconds between generation updates')
parser.add_argument('--stagnation', type=int, default=10, help='Exit if stagnating for this many generations')
parser.add_argument('--stagnation-window', type=int, default=3)
parser.add_argument('--similarity-threshold', type=float, default=0.95)
parser.add_argument('--random-seed', type=int, default=None, help="Seed the random number generator")

args = parser.parse_args()

if args.random_seed is not None:
    random.seed(args.random_seed)

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
except Exception:
    sys.stderr.write('Invalid window size {}\n'.format(args.window))
    parser.usage()
    sys.exit(1)

initial_cells = set()
if args.load is None:
    for y in range(args.height):
        for x in range(args.width):
            if random.uniform(0, 100) < args.fill:
                initial_cells.add((x, y))
else:
    with open(args.load, "r") as f:
        y = 0
        for line in f.readlines():
            x = 0
            for c in line:
                if c == '#':  # we've hit a comment
                    break
                elif not c.isspace():
                    initial_cells.add((x, y))
                x += 1
            y += 1

game = life.Life(initial_cells)

bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y = game.getBoundingBox()
print('{}, {}, {}, {}'.format(bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y))

pygame.init()

window = pygame.display.set_mode(window_size)


def display(game, disp_min_x, disp_min_y, disp_max_x, disp_max_y, print_status=True):
    window_width, window_height = window_size
    window.fill(bg_color)

    disp_width = (disp_max_x - disp_min_x) + 1
    disp_height = (disp_max_y - disp_min_y) + 1

    scale = min(window_width / (disp_width + 1), window_height / (disp_height + 1))
    if print_status:
        print('Generation {}: scale: {} live cells: {}'.format(game.getGeneration(), scale, len(game.getLiveCells())))
    window_pixels = {}

    disp_mid_x = int((disp_max_x + disp_min_x) / 2)
    disp_mid_y = int((disp_max_y + disp_min_y) / 2)

    window_mid_x = int(window_width / 2 + 0.5)
    window_mid_y = int(window_height / 2 + 0.5)

    for cell_x, cell_y in game.getLiveCells():
        x = window_mid_x + int(scale * (cell_x - disp_mid_x - 0.5))
        y = window_mid_y + int(scale * (cell_y - disp_mid_y - 0.5))

        if scale <= 2:
            pix = x, y
            if pix in window_pixels:
                window_pixels[pix] += 1
            else:
                window_pixels[pix] = 1
        else:
            pygame.draw.circle(window, cell_color, (x, y), max(1, 0.45 * scale))

    if scale <= 2:
        max_dens = max([d for d in window_pixels.values()])
        for coord, d in window_pixels.items():
            color = tuple([int((bg_color[c] * (max_dens - d) + cell_color[c] * d) / max_dens) for c in range(3)])
            pygame.draw.circle(window, color, coord, 1)

    pygame.display.flip()


stagnation = 0
live_cells_history = [game.getLiveCells()]
num_cells_history = [len(game.getLiveCells())]

zoom_pause = False
pause = False

zoom_factor = 1.1
shift_factor = 0.1
speed_factor = 1.5

delay_time = args.delay


def shift(min_v, max_v, factor):
    spread = max_v - min_v
    shiftamt = max(1, int(spread * abs(factor)))
    if factor > 0:
        return min_v + shiftamt, max_v + shiftamt
    else:
        return min_v - shiftamt, max_v - shiftamt


def scale(min_v, max_v, factor):
    mid = (max_v + min_v) / 2
    new_min = int(mid - (mid - min_v) * factor + 0.5)
    new_max = int(mid + (max_v - mid) * factor + 0.5)

    if new_min == min_v:
        new_min -= 1 if factor > 1 else -1

    if new_max == max_v:
        new_max += 1 if factor > 1 else -1

    if new_min < new_max:
        return new_min, new_max
    else:
        return min_v, max_v


def zoom(factor):
    global bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y
    bounding_min_x, bounding_max_x = scale(bounding_min_x, bounding_max_x, factor)
    bounding_min_y, bounding_max_y = scale(bounding_min_y, bounding_max_y, factor)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                zoom_pause = not zoom_pause
            elif event.key == pygame.K_i:
                zoom_pause = True
                zoom(1 / zoom_factor)
            elif event.key == pygame.K_o:
                zoom_pause = True
                zoom(zoom_factor)
            elif event.key == pygame.K_p:
                pause = not pause
            elif event.key == pygame.K_c:
                cell_color = 0, 255, 0
                stagnation = 0
            elif event.key == pygame.K_f:
                delay_time /= speed_factor
            elif event.key == pygame.K_s:
                delay_time *= speed_factor
            elif event.key == pygame.K_UP:
                bounding_min_y, bounding_max_y = shift(bounding_min_y, bounding_max_y, -shift_factor)
            elif event.key == pygame.K_DOWN:
                bounding_min_y, bounding_max_y = shift(bounding_min_y, bounding_max_y, shift_factor)
            elif event.key == pygame.K_LEFT:
                bounding_min_x, bounding_max_x = shift(bounding_min_x, bounding_max_x, -shift_factor)
            elif event.key == pygame.K_RIGHT:
                bounding_min_x, bounding_max_x = shift(bounding_min_x, bounding_max_x, shift_factor)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                sys.exit(0)

    min_x, min_y, max_x, max_y = game.getBoundingBox()

    if not zoom_pause and min_x is not None:
        if min_x < bounding_min_x:
            bounding_min_x = min_x
        if min_y < bounding_min_y:
            bounding_min_y = min_y
        if max_x > bounding_max_x:
            bounding_max_x = max_x
        if max_y > bounding_max_y:
            bounding_max_y = max_y

    if game.getLiveCells() and (stagnation < args.stagnation or args.stagnation < 1):
        display(game, bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y, not pause)
        if not pause:
            game.step()

            stagnating = 0
            curr_cells = game.getLiveCells()
            for historical_cells in live_cells_history:
                if len(curr_cells.intersection(historical_cells)) \
                        >= args.similarity_threshold * len(curr_cells):
                    stagnating += 1
                    print("Stagnating on similarity")

            if len(curr_cells) in num_cells_history:
                print("Stagnating on population")
                stagnating += 1

            if stagnating > 0:
                stagnation += 1
                if args.stagnation > 0 and stagnation >= args.stagnation:
                    print("Stagnated at {}".format(game.getGeneration() - args.stagnation))

            else:
                stagnation = 0

            live_cells_history.append(curr_cells)
            if len(live_cells_history) > args.stagnation_window:
                live_cells_history = live_cells_history[-args.stagnation_window:]

            num_cells_history.append(len(curr_cells))
            if len(num_cells_history) > args.stagnation_window:
                num_cells_history = num_cells_history[-args.stagnation_window:]
    else:
        cell_color = 255, 0, 0
        display(game, bounding_min_x, bounding_min_y, bounding_max_x, bounding_max_y, False)

    time.sleep(delay_time)
