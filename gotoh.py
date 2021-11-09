import numpy as np
import sys

g_o = -1.5
g_e = -0.3

counter = 0


def score(i, j):
    global seq_1
    global seq_2

    if seq_1[i] == seq_2[j]:
        return 1
    else:
        return -1


def fill_A(i, j):
    # matrix lookup:
    global matrix
    if matrix[i, j] < np.inf:
        return matrix[i, j]
    if i == 0 and j == 0:
        return 0
    elif i == 0 and j == 1:
        return g_o
    elif i == 1 and j == 0:
        return g_o
    elif i == 0 and j > 1:
        return fill_A(0, j - 1) + g_e
    elif i > 1 and j == 0:
        return fill_A(i - 1, 0) + g_e
    else:
        global counter
        counter += 1
        match_mismatch = fill_A(i - 1, j - 1) + score(i, j)
        deletion = fill_R(i, j)
        insertion = fill_L(i, j)
        return max(match_mismatch, deletion, insertion)


def fill_R(i, j):
    """
    Alignment ends with gap in S
    """
    if j == 0:
        return 0
    elif i == 0 and j == 1:
        return g_o
    if i == 0 and j > 1:
        return fill_R(0, j - 1) + g_e
    else:
        open_gap = fill_A(i - 1, j) + g_o
        extend_gap = fill_R(i - 1, j) + g_e
        return max(open_gap, extend_gap)


def fill_L(i, j):
    """
    Alignment ends with gap in T
    """
    if i == 0:
        return 0
    elif i == 1 and j == 0:
        return g_o
    elif i > 1 and j == 0:
        return fill_L(i - 1, 0) + g_e
    else:
        open_gap = fill_A(i, j - 1) + g_o
        extend_gap = fill_L(i, j - 1) + g_e
        return max(open_gap, extend_gap)


def backtrack(i, j, current_score):
    # TODO:
    global out_1
    global out_2
    print(current_score)

    if i > 0 and fill_A(i - 1, j) + g_o == current_score:
        out_1 = seq_1[i] + out_1
        out_2 = '_' + out_2
        backtrack(i - 1, j, fill_A(i - 1, j))
    elif j > 0 and fill_A(i, j - 1) + g_o == current_score:
        out_1 = '_' + out_1
        out_2 = seq_2[j] + out_2
        backtrack(i, j - 1, fill_A(i, j - 1))
    elif fill_A(i - 1, j - 1) + score(i, j) == current_score:
        # match or mismatch
        out_1 = seq_1[i] + out_1
        out_2 = seq_2[j] + out_2
        backtrack(i - 1, j - 1, fill_A(i - 1, j - 1))
    elif i == 0 == j:
        print("DONE!")
    else:
        print("SOMETHING WENT WRONG WHILE BACKTRACKING!")


if __name__ == "__main__":
    seq_1 = '_' + str(sys.argv[1])
    seq_2 = '_' + str(sys.argv[2])
    out_1 = ''
    out_2 = ''

    matrix = np.full((len(seq_1), len(seq_2)), np.inf)

    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            matrix[i, j] = fill_A(i, j)

    print(matrix)
    print(counter)
    print("Score: {}".format(matrix[matrix.shape[0] - 1, matrix.shape[1] - 1]))

    # backtrack(matrix.shape[0] - 1, matrix.shape[1] - 1, matrix[matrix.shape[0] - 1, matrix.shape[1] - 1])
    print(out_1)
    print(out_2)
