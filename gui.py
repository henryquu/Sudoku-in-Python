from time import gmtime, strftime
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo, askokcancel
from typing import Counter, Tuple
import solver

CLOCK = u"\U0001F551"


class Cell(tk.Canvas):
    def __init__(self, master, y: int, x: int, val: int):
        tk.Canvas.__init__(
            self, master, bg='white', selectbackground='green',
            highlightthickness=1, highlightbackground='black',
            highlightcolor='red')

        self.digits = {}
        self.singled = False
        self.default_bg = 'white'

        self.row = y
        self.column = x
        y = y * 50 + (y // 3) * 4
        x = x * 50 + (x // 3) * 4
        self.place(y=y, x=x, height=50, width=50)

        self.bind('<Button-1>', lambda *_: self.focus_set())
        self.inputs = self.bind('<KeyRelease>', lambda a: self.input(a.keysym))

        if val != 0:
            self.create_text(25, 25, text=val, font='Arial, 18')
            self.config(bg='#D3D3D3', state='disabled')
            self.default_bg = '#D3D3D3'
            self.unbind('<KeyRelease>', self.inputs)

        self.high = self.bind(
            '<FocusIn>',
            lambda _: self.master.highlight(self.row, self.column, 'yellow'))
        self.bind(
            '<FocusOut>',
            lambda _: self.master.highlight(self.row, self.column))

    def input(self, key: str) -> None:
        n = len(self.digits)
        if n > 0:
            current_last = list(self.digits.keys())[-1]

        if key == 'Return' and n == 1:
            nr = current_last
            self.remove_digit(nr)
            self.single(nr)

        elif key == 'BackSpace' and n > 0:
            self.remove_digit(current_last)

        elif (
            len(key) == 2 and key[0] == 'F' and
            key[1].isdecimal and key[1] != '0'
        ):
            key = key[1]
            if self.singled:
                self.remove_digit(current_last)
                self.singled = False
                self.multiple(current_last, key)
            else:
                if key not in self.digits:
                    self.multiple(key)
                else:
                    self.remove_digit(key)

        elif len(key) == 1 and key.isdecimal() and key != '0':
            if key in self.digits and self.singled:
                self.remove_digit(key)
            else:
                for digit in list(self.digits):
                    self.remove_digit(digit)
                self.single(key)

    def single(self, digit: str) -> None:
        id = self.create_text(25, 25, text=digit, font='Arial, 18')
        self.digits[digit] = id
        self.master.board[self.row][self.column] = int(digit)
        self.singled = True
        self.master.highlight(self.row, self.column, 'yellow')
        self.master.master.update_free()
        if solver.solved(self.master.board):
            self.master.master.finished()

    def multiple(self, *digits: Tuple[str]) -> None:
        for digit in set(digits):
            nr = int(digit) - 1
            y = 10 + 15 * (nr // 3)
            x = 10 + 15 * (nr % 3)
            id = self.create_text(x, y, text=digit, font='Arial, 10')
            self.digits[digit] = id

    def remove_digit(self, digit: str) -> None:
        if self.singled:
            self.master.highlight(self.row, self.column)
        self.delete(self.digits[digit])
        self.digits.pop(digit)
        self.master.board[self.row][self.column] = 0
        self.singled = False
        self.master.master.update_free()


class Board(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg='black')
        self.pack(fill='both', expand=True)
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[0 for _ in range(9)] for _ in range(9)]
        self.create_cells()

    def create_cells(self) -> None:
        if self.cells:
            self.destroy_cells()

        for y in range(9):
            for x in range(9):
                self.cells[y][x] = Cell(self, y, x, self.board[y][x])

    def load_string(self, string: str) -> None:
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        for i, val in enumerate(string.replace(' ', '')):
            if val.isdecimal() and val != '0':
                self.board[i // 9][i % 9] = int(val)
        self.create_cells()

    def board_to_string(self) -> str:
        string = ''
        for row in self.board:
            for val in row:
                string = string + str(val) if val > 0 else string + '.'
        return string

    def destroy_cells(self, *_) -> None:
        for child in self.winfo_children():
            child.destroy()

    def highlight(self, y: int, x: int, color: str = None) -> None:
        val = self.board[y][x]
        if val == 0:
            return

        for y, row in enumerate(self.board):
            for x, k in enumerate(row):
                if k == val:
                    if color is None:
                        self.cells[y][x].config(bg=self.cells[y][x].default_bg)
                    else:
                        self.cells[y][x].config(bg=color)


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Sudoku")
        self.geometry(
            f"458x553+{self.winfo_screenwidth() // 2}"
            f"+{self.winfo_screenheight() // 4}"
            )
        self.resizable(False, False)

        self.frame = tk.Frame(
            self, background='green', height=70,
            highlightbackground='black', highlightthickness=1)
        self.frame.pack(fill='x')
        self.frame.option_add('*Background', 'green')
        self.frame.grid_propagate(False)

        self.random = tk.Button(
            self.frame, text='Load random', command=self.load_random)
        self.random.grid(row=0, column=0, padx=5, pady=5)

        self.insert = tk.Button(
            self.frame, text='Insert puzzle', command=self.insert_window)
        self.insert.grid(row=1, column=0, padx=5, sticky='ew')

        self.time = 0
        self.timer = tk.Label(
            self.frame,
            text=CLOCK + strftime("%M:%S", gmtime(self.time)),
            font='Arial, 14'
            )
        self.timer.grid(row=0, column=3, rowspan=2, sticky='ns')
        self.timer_id = None
        self.frame.columnconfigure(3, weight=5)

        self.bottom_frame = tk.Frame(
            self, background='green', height=25,
            highlightbackground='black', highlightthickness=1)
        self.bottom_frame.propagate(False)
        self.bottom_frame.pack(fill='both', side='bottom')

        self.counter = {x: 0 for x in range(1, 10)}
        self.free_digits = tk.Label(self.bottom_frame, font='Arial, 13')
        self.free_digits.pack(pady=3, padx=5, anchor='w')

        self.board = Board(self)
        self.update_free()

        self.copy = tk.Button(
            self.frame, text='Copy board', command=self.get_board)
        self.copy.grid(row=1, column=2, padx=5, sticky='ew')

        self.solve = tk.Button(
            self.frame, text='Solve', command=self.ask_solve)
        self.solve.grid(row=0, column=4, padx=5, sticky='ew')

        self.mainloop()

    def update_time(self) -> None:
        self.time += 1
        if self.time / 60 < 60:
            text = CLOCK + strftime("%M:%S", gmtime(self.time))
        else:
            text = CLOCK + strftime("%H:%M:%S", gmtime(self.time))

        self.timer['text'] = text
        self.timer_id = self.after(1000, self.update_time)

    def insert_window(self, *_) -> None:
        string = askstring('Insert', 'Insert sudoku puzzle as string:\t\t')
        if string:
            self.board.load_string(string)

    def load_random(self, *_) -> None:
        string = (
            '..8...7...1..49.359.73....25...83.' +
            '.....4.2.........19.............897....9....358')
        self.board.load_string(string)

    def finished(self, *_) -> None:
        showinfo('You Won', 'Congratulations!')

    def ask_solve(self, *_) -> None:
        if askokcancel(
            'Solve puzzle?',
            'Are you sure you want to get the solved puzzle?'
        ):
            self.board.board = solver.solver(self.board.board)[0]
            self.board.create_cells()
            for child in self.board.winfo_children():
                child.unbind('FocusIn', child.high)

    def update_free(self, *_) -> None:
        c = Counter(self.board.board_to_string())
        c = {str(x): c[str(x)] for x in range(1, 10)}
        text = ',  '.join(x for x in c if c[x] < 9)
        self.free_digits['text'] = text

    def get_board(self, *_) -> None:
        string = self.board.board_to_string()
        self.clipboard_clear()
        self.clipboard_append(string)
        showinfo('Puzzle', 'Copied board to clipboard!\n' + string)


if __name__ == "__main__":
    Window()
