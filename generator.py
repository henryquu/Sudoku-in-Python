from pprint import pprint
from random import sample, choice
from constants import DIFFICULTY, RANGE, DIGITS, Board
from solverc import Solver, clues_checker


# makes a random full board that fulfills sudoku rules
def fill_board() -> list[list[int]]:
    def pattern(row, column) -> int:
        return (3 * (row % 3) + row // 3 + column) % 9

    def shuffle(s) -> list[int]:
        return sample(s, len(s))

    rBase = range(3)
    rows = [g*3 + r for g in shuffle(rBase) for r in shuffle(rBase)]
    cols = [g*3 + c for g in shuffle(rBase) for c in shuffle(rBase)]

    nums = shuffle(DIGITS)
    board = [[nums[pattern(r, c)] for c in cols] for r in rows]

    if Solver.is_solved(board):
        return board
    return fill_board()


# takes full board, starts removing randomly and checks if has unique solution
def generate(clues: tuple[int]) -> Board:
    while True:
        board = fill_board()
        filled = set((y, x) for x in RANGE for y in RANGE)
        while len(filled) >= clues[0]:
            y, x = choice(tuple(filled))
            board[y][x] = 0
            filled -= {(y, x)}

            copy = [row.copy() for row in board]
            if len(filled) <= clues[1] and clues_checker(board):
                check = Solver(copy).solve(wanted=2)
                if check and len(check) == 1:
                    return board


def main():
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        x = generate(DIFFICULTY['Easy'])
        pprint(x)
    p = pstats.Stats(pr)
    p.sort_stats('tottime').print_stats(5)


if __name__ == '__main__':
    main()
