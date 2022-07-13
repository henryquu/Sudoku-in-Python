from copy import deepcopy
from pprint import pprint
import solver
from random import choice
from rules import DIFFICULTY
import solvercython

def validate(board: list) -> list:
    solutions = 0

    def inner(board):
        nonlocal solutions
        if solutions > 1:
            return

        cords = solver.find_zero(board)
        if cords is None:
            return
        y, x = cords

        for i in range(1, 10):
            if solvercython.allowed(board, i, y, x):
                board[y][x] = i
                if solver.is_solved(board):
                    solutions += 1
                    if solutions > 1:
                        return

                inner(board)
                board[y][x] = 0
    
    inner(board)
    if solutions == 1:
        return 1
    elif solutions > 1:
        return 0
    return -1

def generate_dfs(difficulty):
    diff = DIFFICULTY[difficulty]

def fill_board():
    def recursive(board, not_filled):
        n = len(not_filled)
        if n > 64:
            y, x = choice(not_filled)
        else:
            y, x = not_filled[0]

        not_filled.remove((y, x))
        for val in range(1, 10):
            if solvercython.allowed(board, val, y, x):
                board[y][x] = val
                if n < 64 and solvercython.is_solved(board):
                    return deepcopy(board)
                if rec := recursive(board, not_filled):
                    return deepcopy(rec)

        board[y][x] = 0
        not_filled.append((y, x))

    board = [[0 for _ in range(9)] for _ in range(9)]
    cords = [(y, x) for x in range(9) for y in range(9)]

    return recursive(board, cords)
        



def generate():
    pass

def main():
    # board = [
    #     [1, 2, 3, 4, 5, 6, 7, 8, 9],
    #     [4, 5, 6, 7, 8, 9, 1, 2, 3],
    #     [7, 8, 9, 1, 2, 3, 4, 5, 6],
    #     [2, 3, 1, 5, 6, 4, 8, 9, 7],
    #     [5, 6, 4, 8, 9, 7, 2, 3, 1],
    #     [8, 9, 7, 2, 3, 1, 5, 6, 4],
    #     [3, 1, 2, 6, 4, 5, 9, 7, 8],
    #     [6, 4, 5, 9, 7, 8, 3, 1, 2],
    #     [9, 7, 8, 3, 1, 2, 6, 4, 5]
    # ]
    # print(solver.is_solved(board))
    pprint(fill_board())

if __name__ == '__main__':
    main()