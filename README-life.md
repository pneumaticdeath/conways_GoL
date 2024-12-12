# Command line implementation

The *life.py* file contains not only the core game 
logic, but also a simple text-only display interface.

The argument structure is
```
usage: life [-h] [--size SIZE] [--fill FILL] [--delay DELAY] [--load LOAD]

options:
  -h, --help     show this help message and exit
  --size SIZE    Initial size of grid, default 30,30
  --fill FILL    percent of initial cells to be filled between 0 and 100
  --delay DELAY  Delay in seconds after every generation
  --load LOAD    Load initital state from a file
```
