from copy import deepcopy
from pprint import pprint
from random import sample, choice
from rules import DIFFICULTY
from solver import is_solved, allowed
import cProfile

def validate(board: list) -> list:
    solutions = 0
    empty = tuple((y, x) for y in range(9) for x in range(9) if board[y][x] == 0)

    def inner(board, empty):
        nonlocal solutions
        if solutions > 1:
            return

        cords = empty[0]
        if cords is None:
            return
        y, x = cords

        for i in allowed(board, y, x):
            board[y][x] = i
            if is_solved(board):
                solutions += 1
                if solutions > 1:
                    return

            inner(board, empty[1:])
            board[y][x] = 0
    
    inner(board, empty)
    if solutions == 1:
        return True
    return False


def fill_board() -> list[list[int]]:
    def index(row, column): 
        return (3 * (row % 3) + column) % 9

    shuffled_digits = sample(range(1, 10), 9)

    board = tuple([shuffled_digits[index(r, c)] for c in range(9)] for r in range(9))

    if is_solved(board):
        return board
    return fill_board()


def make_puzzle(clues: tuple[int]):
    digits = range(9)
    board_base = fill_board()
    filled_saved = set((y, x) for x in digits for y in digits)

    while True:
        board = deepcopy(board_base)
        filled = deepcopy(filled_saved)
        while len(filled) >= clues[0]:
            y, x = choice(digits), choice(digits)
            board[y][x] = 0
            filled.discard((y, x))
            
            if len(filled) <= clues[1] and validate(board):
                return board

def main():
    print(make_puzzle(DIFFICULTY['Easy']))


if __name__ == '__main__':
    cProfile.run('main()', sort='tottime')