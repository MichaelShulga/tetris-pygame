def matrix_count(matrix, elem):
    return sum([i.count(elem) for i in matrix])


def transpose(matrix):
    return [[j[i] for j in matrix] for i in reversed(range(len(matrix)))]


def copy(matrix):
    return [i[:] for i in matrix]
