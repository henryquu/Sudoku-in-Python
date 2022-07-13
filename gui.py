from time import gmtime, strftime
import tkinter as tk
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo, askokcancel
from typing import Counter, Tuple
from rules import CLOCK, DIFFICULTY
import solver


highlight_style = {'highlightthickness': 1, 'highlightbackground': 'black'}


class Cell(tk.Canvas):
    def __init__(self, master, y: int, x: int):
        tk.Canvas.__init__(self, master, bg='white')
        self.config(**highlight_style, highlightcolor='red')

        self.digits = {}
        self.singled = False
        self.default_bg = 'white'

        self.row = y
        self.column = x
        cord_y = y * 50 + (y // 3) * 4
        cord_x = x * 50 + (x // 3) * 4
        self.place(y=cord_y, x=cord_x, height=50, width=50)

        self.focus = self.bind('<Button-1>', lambda *_: self.focus_set())

        self.bind('<FocusIn>', lambda _: master.highlight(y, x, 'yellow'))
        self.bind('<FocusOut>', lambda _: master.highlight(y, x))

        init_val = master.board[y][x]
        if init_val != 0:
            self.create_text(25, 25, text=init_val, font='Arial, 18')
            self.config(bg='#D3D3D3', highlightcolor='black')
            self.default_bg = '#D3D3D3'
        else:
            self.bind('<KeyRelease>', lambda a: self.input(a.keysym))

    def input(self, key: str) -> None:
        n = len(self.digits)
        if n > 0:
            last_digit = list(self.digits.keys())[-1]

        if key == 'Return' and n == 1 and not self.singled:
            self.remove_digit(last_digit)
            self.single(last_digit)

        elif key == 'BackSpace' and n > 0:
            self.remove_digit(last_digit)

        elif len(key) == 2 and key[0] == 'F' and '0' < key[1] <= '9':
            key = key[1]
            if self.singled:
                self.remove_digit(last_digit)
                self.singled = False
                self.multiple(last_digit, key)
            else:
                if key not in self.digits:
                    self.multiple(key)
                else:
                    self.remove_digit(key)

        elif len(key) == 1 and '0' < key <= '9':
            if key in self.digits and self.singled:
                self.remove_digit(key)
            else:
                for digit in list(self.digits):
                    self.remove_digit(digit)
                self.single(key)

    def single(self, digit: str) -> None:
        id = self.create_text(25, 25, text=digit, font='Arial, 18')
        self.digits[digit] = id
        self.singled = True

        self.master.board[self.row][self.column] = int(digit)
        self.master.highlight(self.row, self.column, 'yellow')
        self.event_generate('<<DigitInsertion>>')
        if solver.is_solved(self.master.board):
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
        self.singled = False

        self.master.board[self.row][self.column] = 0
        self.master.master.update_free_digits()


class Board(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg='black')
        self.pack(fill='both', expand=True)

        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.cells = [[Cell(self, y, x) for x in range(9)] for y in range(9)]

    def recreate_cells(self) -> None:
        if self.cells:
            for child in self.winfo_children():
                child.destroy()

        self.cells = [[Cell(self, y, x) for x in range(9)] for y in range(9)]

    def load_from_string(self, string: str) -> None:
        if len(string) != 81:
            return None
        for i, val in enumerate(string.replace(' ', '')):
            self.board[i // 9][i % 9] = int(val) if '0' < val <= '9' else 0

        self.master.reset_timer()
        self.recreate_cells()

    def board_to_string(self) -> str:
        string = ''
        for row in self.board:
            string += ''.join(map(lambda x: str(x) if x != 0 else '.', row))

        return string

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

        self.option_add('tk.Frame.background', 'green')

        self.frame = tk.Frame(self, height=70, **highlight_style)
        self.frame.pack(fill='x')
        self.frame.option_add('*Background', 'green')
        self.frame.grid_propagate(False)

        self.random = tk.Button(
            self.frame, text='Load random', command=self.load_random)
        self.random.grid(row=0, column=0, padx=5, pady=5)

        self.insert = tk.Button(
            self.frame, text='Insert puzzle', command=self.insert_string)
        self.insert.grid(row=1, column=0, padx=5, sticky='ew')

        self.timer_id = None
        self.time = 0
        text = CLOCK + strftime("%M:%S", gmtime(self.time))
        self.timer = tk.Label(self.frame, text=text, font='Arial, 14')
        self.timer.grid(row=0, column=3, pady=5)

        self.timer_button = tk.Button(
            self.frame, text='Start timer', command=self.update_time)
        self.timer_button.grid(row=1, column=3, sticky='s')

        self.frame.columnconfigure(3, weight=5)

        self.bottom_frame = tk.Frame(self, height=25, **highlight_style)
        self.bottom_frame.propagate(False)
        self.bottom_frame.pack(fill='both', side='bottom')

        self.counter = {x: 0 for x in range(1, 10)}
        self.free_digits = tk.Label(self.bottom_frame, font='Arial, 13')
        self.free_digits.pack(pady=3, padx=5, anchor='w')

        self.board = Board(self)
        self.update_free_digits()

        self.copy = tk.Button(
            self.frame, text='Copy board', command=self.get_board)
        self.copy.grid(row=1, column=2, padx=5, sticky='ew')

        self.solve = tk.Button(
            self.frame, text='Solve', command=self.auto_solve)
        self.solve.grid(row=0, column=4, padx=5, sticky='ew')

        self.bind('<<DigitInsertion>>', self.update_free_digits)

        self.mainloop()

    def update_time(self) -> None:
        self.time += 1
        if self.time / 60 < 60:
            text = CLOCK + strftime("%M:%S", gmtime(self.time))
        else:
            text = CLOCK + strftime("%H:%M:%S", gmtime(self.time))

        self.timer['text'] = text
        self.timer_id = self.after(1000, self.update_time)

    def reset_timer(self) -> None:
        if self.timer_id:
            self.time = 0
            self.after_cancel(self.timer_id)
            self.timer_id = None
        self.update_time()

    def insert_string(self, *_) -> None:
        string = askstring('Insert', 'Insert sudoku board as string:\t\t')
        if string:
            self.board.load_from_string(string)

    def load_random(self, *_) -> None:
        string = (
            '..8...7...1..49.359.73....25...83.' +
            '.....4.2.........19.............897....9....358')
        self.board.load_from_string(string)
        self.reset_timer()

    def finished(self, *_) -> None:
        showinfo('You Won', 'Congratulations!')
        self.after_cancel(self.timer_id)
        self.timer_id = None

    def auto_solve(self, *_) -> None:
        if askokcancel(
            'Solve puzzle?',
            'Are you sure you want to get the solved puzzle?'
        ):
            self.after_cancel(self.timer_id)
            self.timer_id = None
            self.board.board = solver.solve(self.board.board)[0]
            self.board.recreate_cells()
            self.update_free_digits()
            for child in self.board.winfo_children():
                child.unbind('<Button-1>', child.focus)

    def update_free_digits(self, *_) -> None:
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
