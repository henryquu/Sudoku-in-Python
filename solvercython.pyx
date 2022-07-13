from copy import deepcopy
from typing import Tuple
import cython

def allowed(board: list, val: int, y: int, x: int) -> bool:
    box_y = (y // 3) * 3
    box_x = (x // 3) * 3

    if val in board[y]:
        return False
    for i in range(9):
        if (board[i][x] == val or
            board[box_y + i // 3][box_x + i % 3] == val
        ):
            return False

    return True


def is_solved(board: list) -> bool:
    goal = sum(range(1, 10))
    for row in board:
        if sum(row) != goal:
            return False
    return True


def find_zero(board: list) -> Tuple[int, int]:
    for y, row in enumerate(board):
        if 0 in row:
            return (y, row.index(0))


def solve(board: list) -> list:
    final = []

    def inner(board):
        y, x = find_zero(board)
        if y is None:
            return board

        for i in range(1, 10):
            if allowed(board, i, y, x):
                board[y][x] = i
                if is_solved(board):
                    return final.append(deepcopy(board))

                inner(board)
                board[y][x] = 0
    
    inner(board)
    return final


def check_for_duplicates(lst: list) -> None:
    i = 0
    for k, x in enumerate(lst):
        for y in lst[k + 1:]:
            if x == y:
                i += 1
    print(i)

def from_string(string: str) -> list:
    string = string.strip()
    board = [[0 for _ in range(9)] for _ in range(9)]
    for i, val in enumerate(string):
        board[i // 9][i % 9] = int(val)
    return board

def main():
    game = [
        [0, 4, 6, 0, 0, 0, 0, 0, 2],
        [0, 0, 0, 0, 0, 0, 0, 0, 5],
        [5, 0, 0, 0, 0, 0, 0, 0, 6],
        [3, 0, 0, 6, 0, 0, 8, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, 0, 5, 4, 0, 0, 0, 0],
        [0, 0, 2, 0, 1, 5, 0, 0, 0],
        [0, 0, 0, 0, 6, 0, 0, 4, 0],
        [0, 0, 4, 0, 0, 0, 6, 0, 0]
    ]

    outcomes = solve(game)
    print('Number of solutions:',  len(outcomes))


if __name__ == "__main__":
    main()

