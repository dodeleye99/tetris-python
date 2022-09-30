# Tetris Python

A Tetris implementation coded in Python, using the [Pygame](https://www.pygame.org/news) library.

![Demo](_demos/demo1.gif)

## Controls

* `Left Arrow`: Move left. Hold for quick movement.

* `Right Arrow`: Move right. Hold for quick movement.

* `Down Arrow`: Fast drop.

* `X key`: Rotate clockwise.

* `Z key`: Rotate anticlockwise.

* `Escape key`: Toggle pause. Alternatively, click the pause button.

## Score System
The points for clearing lines depends on the current level and the number of lines cleared:

`points = level * base`.

The `base` values for each line are as follows:
* `1 line  = 40 points`
* `2 lines = 100 points` 
* `3 lines = 300 points`
* `4 lines = 1200 points`

Also one point is given for every space fallen while fast dropping. 
