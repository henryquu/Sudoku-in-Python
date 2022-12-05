class Board:
    pass

RANGE = range(9)
DIGITS = range(1, 10)

DIFFICULTY = {
    'Beginner': (46, 55),
    'Easy': (36, 45),
    'Normal': (27, 36),
    'Hard': (19, 26),
    'Very Hard': (17, 18)
}

CLOCK = u"\U0001F551"


DIGITS_TO_BITS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16, 6: 32, 7: 64, 8: 128, 9: 256, 0: 0}
BITS_TO_DIGITS = {1: 1, 2: 2, 4: 3, 8: 4, 16: 5, 32: 6, 64: 7, 128: 8, 256: 9, 0: 0}

CORDS = {(y, x) for x in RANGE for y in RANGE}
CORD_TO_BOX = {}


from itertools import product

for box in RANGE:
    y_plus = 3*(box // 3)
    x_plus = 3*(box % 3)

    for j, k in product((0, 1, 2), (0, 1, 2)):
        y, x = j + y_plus, k + x_plus
        CORD_TO_BOX[(y, x)] = box
