# Conway's Game of Life

This repository has 3 versions of John Conway's "Game of Life".  It is
sometimes described as a zero-player computer game.  The game starts with
a set of live cells within a large (infinite) rectalinear grid, and each
suceeding generation is calculated using a couple of simple rules.  If a
cell was alive during the previous generation, and had fewer than 2 live
neighbors it dies of loneliness, and if it had more than 3 live neighbors
it dies from overcrowding, but otherwise remains alive if it had 2 or 3 live
neighbors.  If a cell was "dead" in the previous generation, but had exactly
3 living neighbors, then a new cell is "born" at that location.  The rules
are simple, but yield surprisingly complex behaviors--in fact it has been
shown that the game of life is actually turing complete, that is, it can
be used to construct a traditional computer.

The three versions I have are:
* life.py     -- a strictly text based command line implemntation
* pyg_life.py -- an implenation using the _pygame_ SDL graphics library
* wxLife.py   -- a full GUI application build using _wxPython_

All three should run on Windows, MacOS and Linux, though I haven't tested 
them on Windows myself.

For the pygame version (pyg_life.py) there are the following command line options:
```
usage: ./pyg_life.py [-h] [--width WIDTH] [--height HEIGHT] [--fill FILL] [--load LOAD] [--window WINDOW] [--fullscreen]
                     [--paused] [--delay DELAY] [--stagnation STAGNATION] [--similarity-threshold SIMILARITY_THRESHOLD]
                     [--random-seed RANDOM_SEED]

options:
  -h, --help            show this help message and exit
  --width WIDTH         Initial width of game
  --height HEIGHT       Initial height of game
  --fill FILL           Percentage fill of initial field
  --load LOAD           Optional file for initial pattern
  --window WINDOW       Dimensions of window
  --fullscreen          Display in full screen
  --paused              Start the game paused
  --delay DELAY         Delay in seconds between generation updates
  --stagnation STAGNATION
                        Stop if stagnated for this many generations
  --similarity-threshold SIMILARITY_THRESHOLD
  --random-seed RANDOM_SEED
                        Seed the random number generator
```

And in the game you can use the following keys to control the display:

* P - Toggle whether the game is paused
* Z - Toggle auto-zoom
* C - Continue after stagnation pause
* I - Zoom in
* O - Zoom out
* B - Step backwards in time
* F - Run faster
* S - Run Slower
* D - Dump current pattern to save file
* Q - Quit game
* SPACE - Take a single step
* RETURN - toggle full screen display
* Arrow Keys - Scroll around the playfield
