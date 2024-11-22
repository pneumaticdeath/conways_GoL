* Conway's Game of Life

For the pygame version (pyg_life.py) there are the following command line options:
```
usage: ./pyg_life.py [-h] [--width WIDTH] [--height HEIGHT] [--fill FILL] [--load LOAD] [--window WINDOW] [--delay DELAY]
                     [--stagnation STAGNATION] [--stagnation-window STAGNATION_WINDOW]
                     [--similarity-threshold SIMILARITY_THRESHOLD] [--random-seed RANDOM_SEED]

options:
  -h, --help            show this help message and exit
  --width WIDTH         Initial width of game
  --height HEIGHT       Initial height of game
  --fill FILL           Percentage fill of initial field
  --load LOAD           Optional file for initial pattern
  --window WINDOW       Dimensions of window
  --delay DELAY         Delay in seconds between generation updates
  --stagnation STAGNATION
                        Exit if stagnating for this many generations
  --stagnation-window STAGNATION_WINDOW
  --similarity-threshold SIMILARITY_THRESHOLD
  --random-seed RANDOM_SEED
                        Seed the random number generator
```

And in the game you can use the following keys to control the display:

* P  Pause the game
* Z  Toggle auto-zoom
* C  Continue after auto-pause
* I  Zoom in
* O  Zoom out
* Q  Quit game
* Arrow Keys  Scroll around the playfield
