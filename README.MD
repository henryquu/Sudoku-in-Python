# Sudoku

## Solver:
 - used depth first algorithm
 - solutions counter
 - solutions shower


## Options:
    - play random puzzle?
    - insert your own puzzle as string or manually into cells
    - show solved puzzle


## Gameplay:
- insert board manually / as string / load random board
- click on chosen cell to make it look for digit insertions
- keys 'F1' - 'F9' insert digits as small, key '1' - '9' as big
- if big digit inserted -> insert it into the board, check if solved
- delete last inserted digit with 'BackSpace' button
- can use 'Enter' / 'Return' key on cell with 1 small digit to transform it into big one


## GUI:
- Upper frame:
    - difficulty?
    - timer
    - solver
    - insert board
    - copy board

- Board:
    - 9x9 Cells divided into boxes graphically

- Cells:
    - 1 big digit or grid of small ones depending on input
    - focus on a single digit highlights the same digit in all cells

- list of avaible digits below the board

## TO-DO
- generator with choosing difficulty
- faster solver
- update time on button click doesn't reset timer