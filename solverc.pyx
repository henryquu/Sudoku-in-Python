import logging
import itertools
from constants import *


class Solver:
    def __init__(self, board: Board):
        self.board = board
        self.allowed_load()

    # load list of allowed digts for every box, column and row
    # allowed digits are represented as a sum of powers of 2^i, i in <0, 8>
    # e.g. 1=1, 2=2, and 3=4, every added up combination is unique
    def allowed_load(self):
        self.allowed_box = [511, 511, 511, 511, 511, 511, 511, 511, 511]
        self.allowed_row = [511, 511, 511, 511, 511, 511, 511, 511, 511]
        self.allowed_col = [511, 511, 511, 511, 511, 511, 511, 511, 511]

        for y, x in CORDS:
            val = DIGITS_TO_BITS[self.board[y][x]]
            if val != 0:
                self.allowed_row[y] -= val
                self.allowed_col[x] -= val
                self.allowed_box[CORD_TO_BOX[(y, x)]] -= val

    # creates lists of digits used in groups the cell belongs to
    # then removes them from base range(1, 10)
    # doesn't use any preloading
    def allowed(board: list, y: int, x: int) -> set:
        box_y = y - y % 3
        box_x = x - x % 3

        column = [board[0][x], board[1][x], board[2][x],
                  board[3][x], board[4][x], board[5][x],
                  board[6][x], board[7][x], board[8][x]]
        row = board[y]
        box = (board[box_y][box_x:box_x + 3] +
               board[box_y + 1][box_x:box_x + 3] +
               board[box_y + 2][box_x:box_x + 3])

        return {1, 2, 3, 4, 5, 6, 7, 8, 9} - set(box + column + row)

    # checks assuming no rules are broken
    def is_solved(board: Board) -> bool:
        goal = sum(DIGITS)
        for row in board:
            if sum(row) != goal:
                return False
        return True

    def solve(self, wanted: int=-1) -> list:
        self.logical_solver()
        if Solver.is_solved(self.board):
            return [self.board]

        return Solver.brute_solver(self.board, wanted)

    @staticmethod
    def brute_solver(board, wanted: int=-1) -> list:
        def inner(board, empty, final, wanted):
            y, x = empty[0]
            for val in Solver.allowed(board, y, x):
                board[y][x] = val
                if len(empty) - 1 == 0:
                    final.append(tuple(tuple(row) for row in board))
                    board[y][x] = 0
                    return

                inner(board, empty[1:], final, wanted)
                board[y][x] = 0
                if len(final) == wanted:
                    return

        empty = tuple((y, x) for x in RANGE for y in RANGE if board[y][x] == 0)
        if len(empty) == 0:
            return

        final = []
        inner(board, empty, final, wanted)
        return final

    def logical_solver(self):
        while self._logic_boxes() or self._logic_cols() or self._logic_rows():
            pass

    # uses preloading, usable only after class initialisation
    def _allowed_in_cell(self, y: int, x: int, box: int) -> set:
        btd = BITS_TO_DIGITS
        col = {btd[b] for b in btd if self.allowed_col[x] & b}
        box = {btd[b] for b in btd if self.allowed_box[box] & b}
        row = {btd[b] for b in btd if self.allowed_row[y] & b}
        return col & box & row

    # logic funcs below check every cell in group and digit in group
    # if digit has 1 spot or cell has 1 digit allowed -> insert the digit
    # return False if function can't find anything anymore
    def _logic_cols(self) -> bool:
        changed = False

        for x in RANGE:
            placements = {digit: set() for digit in DIGITS}
            for y in RANGE:
                if self.board[y][x] != 0:
                    continue

                box = CORD_TO_BOX[(y, x)]
                allowed_in_cell = self._allowed_in_cell(y, x, box)
                if len(allowed_in_cell) == 1:
                        digit = allowed_in_cell.pop()
                        self.board[y][x] = digit
                        self._update_allowed(y, x, box, digit)
                        continue
                for digit in allowed_in_cell:
                    placements[digit].add(y)

            for digit in placements:
                if len(placements[digit]) == 1:
                    y = placements[digit].pop()
                    box = CORD_TO_BOX[(y, x)]
                    self._update_allowed(y, x, box, digit)
                    self.board[y][x] = digit
                    changed = True

        return changed

    def _logic_rows(self) -> bool:
        changed = False

        for y in RANGE:
            placements = {digit: set() for digit in DIGITS}
            for x in RANGE:
                if self.board[y][x] != 0:
                    continue

                box = CORD_TO_BOX[(y, x)]
                allowed_in_cell = self._allowed_in_cell(y, x, box)
                if len(allowed_in_cell) == 1:
                        digit = allowed_in_cell.pop()
                        self.board[y][x] = digit
                        self._update_allowed(y, x, box, digit)
                        continue
                for digit in allowed_in_cell:
                    placements[digit].add(x)

            for digit in placements:
                if len(placements[digit]) == 1:
                    x = placements[digit].pop()
                    box = CORD_TO_BOX[(y, x)]
                    self._update_allowed(y, x, box, digit)
                    self.board[y][x] = digit
                    changed = True

        return changed

    def _logic_boxes(self) -> bool:
        changed = False

        for i in RANGE:
            placements = {digit: set() for digit in DIGITS}
            y_plus = 3*(i // 3)
            x_plus = 3*(i % 3)
            for j, k in itertools.product((0, 1, 2), (0, 1, 2)):
                y, x = j + y_plus, k + x_plus
                if self.board[y][x] != 0:
                    continue

                allowed_in_cell = self._allowed_in_cell(y, x, i)
                if len(allowed_in_cell) == 1:
                    digit = allowed_in_cell.pop()
                    self.board[y][x] = digit
                    self._update_allowed(y, x, i, digit)
                    continue
                for digit in allowed_in_cell:
                    placements[digit].add((y, x))

            for digit in placements:
                if len(placements[digit]) == 1:
                    y, x = placements[digit].pop()
                    self._update_allowed(y, x, i, digit)
                    self.board[y][x] = digit
                    changed = True

        return changed

    # def hidden_pairs(self, placements): not implemented
    #     pass

    def _update_allowed(self, y: int, x: int, box: int, val: int):
        val = DIGITS_TO_BITS[val]
        self.allowed_row[y] -= val
        self.allowed_col[x] -= val
        self.allowed_box[box] -= val

    def _add_allowed(self, y: int, x: int, box: int, val: int):
        val = DIGITS_TO_BITS[val]
        self.allowed_row[y] += val
        self.allowed_col[x] += val
        self.allowed_box[box] += val

    # used for debugging purposes
    def _update_log(self, y: int, x: int, box: int, val: int):
        import inspect
        for i, row in enumerate(self.board):
            logging.info("%i: %s", i, row)
        logging.info("Row: %s", self.allowed_row)
        logging.info("Col: %s", self.allowed_col)
        logging.info("Box: %s", self.allowed_box)
        logging.info("Inserting %i into ((row %i, col %i) (box %i)) in %s",
                     val, y, x, box, inspect.stack()[1].function)


# checks number of inserted digits, sudoku needs at least 17 to be solvable
def clues_checker(board: Board) -> bool:
    digits = {i: 0 for i in DIGITS}
    sum = 0

    for row in board:
        for digit in row:
            if digit != 0:
                digits[digit] += 1
                sum += 1
    if sum < 17:
        return False

    zeros = 0
    for digit in digits:
        if digits[digit] == 0:
            zeros += 1
            if zeros == 2:
                return False
    return True


# list of all allowed digits in cells, dict by cords y, x
def all_allowed(board: Board) -> dict:
    allowed_in_cells = {}
    for y in RANGE:
        for x in RANGE:
            if board[y][x] != 0:
                continue
            allowed = Solver.allowed(board, y, x)
            if len(allowed) > 0:
                allowed_in_cells[(y, x)] = allowed
    return allowed_in_cells


# convert string int board object
def from_string(string: str) -> Board:
    string = string.strip()
    board = [[0 for _ in RANGE] for _ in RANGE]
    for i, val in enumerate(string):
        if '0' < val <= '9':
            board[i // 9][i % 9] = int(val)
        else:
            board[i // 9][i % 9] = 0
    return board


# converts board into string object
def to_string(board: list) -> str:
    s = ""
    for row in board:
        for val in row:
            s += str(val)
    return s


def main():
    from pprint import pprint
    # import logging
    # logging.basicConfig(filename='logging.txt', encoding='utf-8',
    #                     filemode='w', level=logging.DEBUG)

    for _ in range(10000):
        board = [
            [8, 0, 0, 0, 0, 9, 0, 0, 3],
            [0, 9, 0, 1, 0, 0, 8, 0, 0],
            [0, 1, 0, 0, 0, 7, 0, 0, 0],
            [0, 3, 0, 4, 0, 0, 0, 8, 0],
            [6, 0, 0, 0, 8, 0, 0, 0, 1],
            [0, 7, 0, 0, 0, 2, 0, 3, 0],
            [0, 0, 0, 5, 0, 0, 0, 1, 0],
            [0, 0, 4, 0, 0, 3, 0, 9, 0],
            [5, 0, 0, 7, 0, 0, 0, 0, 2]
        ]
        a = Solver(board)
    pprint(a.solve())

if __name__ == "__main__":
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        main()
    p = pstats.Stats(pr)
    p.sort_stats('tottime').print_stats(7)
