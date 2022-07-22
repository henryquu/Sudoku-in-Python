from copy import deepcopy
from pprint import pprint
import cProfile


def is_allowed(board: list, val: int, y: int, x: int) -> bool:
    box_y = (y // 3) * 3
    box_x = (x // 3) * 3
    digits = (0, 1, 2, 3, 4, 5, 6, 7, 8)

    if val in set(board[y]): 
        return False
    if val in (board[i][x] for i in digits): 
        return False
    if val in (board[box_y + i // 3][box_x + i % 3] for i in digits): 
        return False

    return True


def allowed(board: list, y: int, x: int) -> set:
    digits = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    box_y = (y // 3) * 3
    box_x = (x // 3) * 3

    allowed_digits = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    box = set(
        board[box_y + 0][box_x:box_x + 3] + board[box_y + 1][box_x:box_x + 3] + 
        board[box_y + 2][box_x:box_x + 3] + [board[i][x] for i in digits] + 
        board[y]
    )

    
    allowed_digits -= box

    return allowed_digits


def is_solved(board: list) -> bool:
    goal = sum(range(1, 10))
    for row in board:
        if sum(row) != goal:
            return False
    return True


def find_zero(board: list) -> tuple[int]:
    for y, row in enumerate(board):
        if 0 in row:
            return (y, row.index(0))


def solve(board: list) -> list:
    final = []
    empty = tuple((y, x) for y in range(9) for x in range(9) if board[y][x] == 0)

    def dfs(board, empty):
        y, x = empty[0]

        for i in allowed(board, y, x):
            board[y][x] = i
            if len(empty) - 1 == 0:
                final.append(deepcopy(board))
                board[y][x] = 0
                return

            dfs(board, empty[1:])
            board[y][x] = 0
    
    dfs(board, empty)
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
        if '0' < val <= '9':  
            board[i // 9][i % 9] = int(val)
        else:
            board[i // 9][i % 9] = 0
    return board

def to_string(board: list) -> str:
    s = ""
    for row in board:
        for val in row:
            s += str(val)
    return s


def main():
    board = [
        [0, 0, 8, 0, 0, 0, 7, 0, 0],
        [0, 1, 0, 0, 4, 9, 0, 3, 5],
        [9, 0, 7, 3, 0, 0, 0, 0, 2],
        [5, 0, 0, 0, 8, 3, 0, 0, 0],
        [0, 0, 0, 4, 0, 2, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 9, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 8, 9, 7, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 3, 5, 8]
    ]

    print("sudoku: ", to_string(board))
    outcomes = solve(board)
    print('Number of solutions:',  len(outcomes))


if __name__ == "__main__":
    cProfile.run('main()', sort='tottime')

