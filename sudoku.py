from copy import deepcopy
import numpy as np


SIZE = 9

def allowed(matrix):
    a = np.hsplit(matrix,  3)
    boxes = np.array(list(map(lambda x: np.vsplit(x, 3), a))).reshape((9, 9))

    for i in range(SIZE):
        if sum(np.unique(matrix[i])) != sum(matrix[i]):
            return False
        if sum(np.unique(matrix[:, i])) != sum(matrix[:, i]):
            return False
        if sum(np.unique(boxes[i])) != sum(boxes[i]):
            return False
    return True


def finished(matrix):
    if np.sum(matrix) == sum(range(1, 10)) * 9:
        return True


def brute_force(matrix):
    def dfs(matrix, y, x):
        matrix = deepcopy(matrix)
        for i in range(1, 10):
            matrix[y][x] = i
            if allowed(matrix):
                if finished(matrix):
                    return matrix
                next = dfs_loop(matrix)
                if next is not None:
                    return next


    def dfs_loop(matrix):
        zeros = np.argwhere(matrix == 0)
        print(zeros)
        for y, x in zeros:
            if matrix[y][x] == 0:
                result = dfs(matrix, y, x)
                if result is not None:
                    return result


    return dfs_loop(matrix)


def profiling(game):
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        a = brute_force(game)
        print(a)

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats(5)

def main():
    # game = np.array([
    #     [0, 4, 6, 1, 5, 0, 0, 0, 2],
    #     [0, 0, 0, 0, 0, 0, 0, 7, 5],
    #     [5, 7, 0, 2, 0, 0, 0, 1, 6],
    #     [3, 0, 0, 6, 7, 2, 8, 0, 0],
    #     [4, 0, 9, 8, 3, 0, 5, 2, 0],
    #     [2, 0, 0, 5, 4, 0, 1, 0, 0],
    #     [0, 0, 2, 0, 1, 5, 0, 0, 0],
    #     [8, 1, 0, 7, 6, 0, 0, 4, 0],
    #     [0, 0, 4, 0, 2, 0, 6, 0, 0]
    # ])
    game = np.array([
        [9, 4, 6, 1, 5, 7, 3, 8, 2],
        [1, 2, 8, 3, 0, 6, 4, 7, 5],
        [5, 7, 0, 0, 8, 0, 0, 1, 6],
        [3, 5, 1, 6, 0, 2, 8, 9, 4],
        [4, 0, 9, 8, 3, 0, 0, 2, 0],
        [2, 0, 0, 5, 4, 0, 1, 0, 0],
        [6, 0, 2, 0, 1, 0, 0, 0, 0],
        [8, 1, 5, 7, 6, 3, 2, 4, 9],
        [7, 3, 4, 9, 2, 8, 6, 5, 1]
    ])
    print(brute_force(game))

if __name__ == "__main__":
    main()
