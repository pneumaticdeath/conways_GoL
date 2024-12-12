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
- [life.py](README-life.md)     -- a strictly text based command line implemntation
- [pyg_life.py](README-pyg_life.md) -- an implenation using the **pygame** SDL graphics library
- wxLife.py   -- a full GUI application built using **wxPython**

All three should run on Windows, MacOS and Linux, though I haven't tested 
them on Windows myself.
