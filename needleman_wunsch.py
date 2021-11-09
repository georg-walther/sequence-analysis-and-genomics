import numpy as np
import sys

g = -1
counter = 0


def score(i, j):
    global seq_1
    global seq_2

    if seq_1[i] == seq_2[j]:
        return 1
    else:
        return -1


def M(i, j):
    # matrix lookup:
    global matrix
    if matrix[i, j] < np.inf:
        return matrix[i, j]
    else:
        global counter
        counter += 1
        match_mismatch = M(i - 1, j - 1) + score(i, j)
        deletion = M(i - 1, j) + g
        insertion = M(i, j - 1) + g
        return max(match_mismatch, deletion, insertion)


def backtrack(i, j, current_score):
    global out_1
    global out_2
    print(current_score)

    if i > 0 and M(i - 1, j) + g == current_score:
        out_1 = seq_1[i] + out_1
        out_2 = '_' + out_2
        backtrack(i - 1, j, M(i - 1, j))
    elif j > 0 and M(i, j - 1) + g == current_score:
        out_1 = '_' + out_1
        out_2 = seq_2[j] + out_2
        backtrack(i, j - 1, M(i, j - 1))
    elif M(i - 1, j - 1) + score(i, j) == current_score:
        # match or mismatch
        out_1 = seq_1[i] + out_1
        out_2 = seq_2[j] + out_2
        backtrack(i - 1, j - 1, M(i - 1, j - 1))
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
    for j in range(matrix.shape[1]):
        matrix[0, j] = j * g
    for i in range(matrix.shape[0]):
        matrix[i, 0] = i * g

    for i in range(1, matrix.shape[0]):
        for j in range(1, matrix.shape[1]):
            matrix[i, j] = M(i, j)

    print(matrix)
    print(counter)

    backtrack(matrix.shape[0] - 1, matrix.shape[1] - 1, matrix[matrix.shape[0] - 1, matrix.shape[1] - 1])
    print(out_1)
    print(out_2)
