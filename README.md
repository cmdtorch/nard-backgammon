# Nard Game (Backgammon)

Classic board game of Nard (Backgammon) for two players.

![pypi](https://img.shields.io/pypi/v/nard-backgammon.svg)
![versions](https://img.shields.io/pypi/pyversions/nard-backgammon.svg)



#### Common rules
- Players: the game is played by two players
- Tables board of 24 points or spaces; 2 dice; 30 pieces (15 per player)
- Both players throw a die to decide who plays first; the one with the higher die leads off
- Bearing off:
  - Begins once all 15 pieces are in the home quadrant
  - One piece is removed from the point corresponding to the roll of each die
  - If there are no piece on the point corresponding to a die roll, the player must make a legal move with a piece further away
  - If that is not possible, a piece is borne off from the furthest point that is occupied.

## Installation

```bash
$ pip install nard-backgammon
```

## Usage


#### Playing
```python
from nard_backgammon import (
    Nard, 
    NardState, 
    Player, 
    get_random_move, 
    board_to_str)


# If the first_player is None, then the starting
# player is found on the first roll `first_roll()`
game = Nard.new(first_roll_player=Player.WHITE)

while True:

    match game.state:
        # If first_roll_player is None then 
        # NardState is will be FIRST_ROLL at the init
        case NardState.FIRST_ROLL:
            game.first_roll()

        case NardState.PLAYING:
            # get valid moves for active player
            moves = game.get_valid_moves()
            if not moves:
                game.skip()
                continue
            move = get_random_move(moves)
            game.play_move(move)
            print(board_to_str(game))

        case NardState.ENDED:
            print(f'Winner: {game.outcome.winner}')
            break # End game, exit the loop
```

#### Output
```text
...
            ||12-11-10-9--8--7-||6--5--4--3--2--1-||
            ||o  o  x  x     x ||                 ||
            ||2     2  7     2 ||                 ||
            ||                 ||                 || White off: 0
            ||                 ||                 || Black off: 4
            ||                 ||                 || Dices: (4, 3)
            ||               2 ||      4  3       ||
            ||            o  o ||   o  o  o  o    ||
            ||13-14-15-16-17-18||19-20-21-22-23-24||
...
Winner: Player.WHITE
```
