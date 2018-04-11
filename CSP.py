import itertools as it
import numpy as np
from scipy.spatial.distance import pdist


def create_rows(n, rows):
    '''
    Create all possible rows which satisfy row constraints
    '''
    row = []
    create_row(n, row[:], rows)


def create_row(n, row, rows):
    '''
    Recursive function for creating rows in binary tree schema so that no element in the row
    equals two preceding
                                            x,y
                                           /   \
                                          x    y
                                         / \   ...
                                        x   y
                                         \ / \
                                         y x y
                                        ...

    :param n: length of the row according to the size specified by the user
    :param row: [] - row to which next element will be append till it is of lenght = n
    :param rows: [[]] - list of rows to which created rows are appended
    :return: [[]] -list n x n of n rows consisting of n values {x, y} so they satisfy row constraints
    '''
    if len(row) == n:
        rows.append(row[:])
        return True
    if len(row) > 1:
        if row[-1] == row[-2]:
            if row[-1] == -1:
                row.append(1)
                create_row(n, row[:], rows)
            else:
                row.append(-1)
                create_row(n, row[:], rows)
        else:
            _row = row[:]
            row.append(-1)
            create_row(n, row[:], rows)
            _row.append(1)
            create_row(n, _row[:], rows)
    else:
        _row = row[:]
        row.append(-1)
        create_row(n, row[:], rows)
        _row.append(1)
        create_row(n, _row[:], rows)


def make_rows_vectors(rows):
    '''

    :param rows: n x n list of rows [[1, -1, 1, 1, -1, ...]]
    :return: [numpy array 1xn] list of n length

    function which changes inside list of values in row into numpy matrix for easier
    mathematical interpretation
    '''
    vector_list = []
    for row in rows:
        row = np.asarray(row)
        row = row.reshape((1, len(row)))
        vector_list.append(row)
    return vector_list


def constraint_satisfied(matrix):
    if (-3 in matrix[-3:, :].sum(axis=0) or 3 in matrix[-3:, :].sum(axis=0)) and matrix.shape[0]>2:
        return False
    if matrix.shape[1] == matrix.shape[0]:
        zeros_vector = np.zeros(matrix.shape[1])
        if 0 in (pdist(matrix, metric='hamming')):
            return False
    return True


def append_row(matrix, domain):
    for row in domain:
        '''Add vector to matrix and check constraints'''
        matrix = np.append(matrix, row, axis=0)
        if matrix.shape[0] == matrix.shape[1] and constraint_satisfied(matrix):
            return matrix
        if constraint_satisfied(matrix):
            actual_domain = domain[:]
            i = 0
            for actual_row in actual_domain:
                if np.array_equal(actual_row, row):
                    del actual_domain[i]
                i += 1
            append_row(matrix, actual_domain)
        else:
            matrix = matrix[:-1, :]
        if len(domain) == 0:
            return 
    return


def solve_mosaic(rows):
    for row in rows:
        '''Set the first row and remove it from the domain'''
        matrix = row
        domain = rows[:]
        i = 0
        for actual_row in rows:
            if np.array_equal(actual_row, matrix):
                del domain[i]
            i += 1
        '''Start recurse'''
        ret = append_row(matrix, domain)
        if ret is not None:
            print("SOLVED")
            print(ret)
            return ret


def intersection(rowwise_matrix, columnwise_matrix):
    rowwise = rowwise_matrix.reshape((rowwise_matrix.shape[0], rowwise_matrix.shape[1]**2))
    columnwise = columnwise_matrix.reshape((columnwise_matrix.shape[0], columnwise_matrix.shape[1]**2))
    print(rowwise)
    print(rowwise.shape)
    print(columnwise)
    print(columnwise.shape)
    for row in rowwise:
        if any((columnwise[:] == row).all(1)):
            return row
    return


if __name__ == "__main__":
    map_size = int(input("Please specify the size: "))
    all_rows = []
    create_rows(map_size, all_rows)
    all_rows = make_rows_vectors(all_rows)
    solve_mosaic(all_rows)

