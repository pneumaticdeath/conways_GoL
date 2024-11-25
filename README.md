* Conway's Game of Life

For the pygame version (pyg_life.py) there are the following command line options:
```
usage: ./pyg_life.py [-h] [--width WIDTH] [--height HEIGHT] [--fill FILL] [--load LOAD] [--window WINDOW] [--fullscreen]
                     [--paused] [--delay DELAY] [--stagnation STAGNATION] [--stagnation-window STAGNATION_WINDOW]
                     [--similarity-threshold SIMILARITY_THRESHOLD] [--random-seed RANDOM_SEED]

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
  --stagnation-window STAGNATION_WINDOW
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
* F - Run faster
* S - Run Slower
* Q - Quit game
* SPACE - Take a single step
* RETURN - toggle full screen display
* Arrow Keys - Scroll around the playfield
