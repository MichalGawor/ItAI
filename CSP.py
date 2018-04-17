import itertools as it
import numpy as np
from scipy.spatial.distance import pdist
import time

'''
This script finds a solution to CSP problem stated as:
In square map nxn fill all the cell using letters x and y in the way that there are no more
then two same consecutive letters neither in rows nor in columns and all rows and columns 
are unique
'''


def create_rows(n, rows):
    '''
    Create all possible rows which satisfy row constraints
    '''
    row = []
    create_row(n, row[:], rows)


def create_row(n, row, rows):
    '''
    Recursive function for creating rows in binary tree schema so that no element in the row
    equals two predecessors
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
    :return: [[]] -list n x n of n rows consisting of n values {-1, 1} (numerical interpretation
    of {x, y} so they satisfy row constraints
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
    if (-3 in matrix[-3:, :].sum(axis=0) or 3 in matrix[-3:, :].sum(axis=0)) and matrix.shape[0] > 2:
        return False
    if matrix.shape[1] == matrix.shape[0]:
        if 0. in (pdist(matrix.transpose(), metric='euclidean')):
            return False
    return True


def del_from_domain(domain, row):
    i = 0
    for actual_row in domain:
        if np.array_equal(actual_row, row):
            del domain[i]
            return domain
        i += 1


def forward_check(matrix, domain):
    '''
    :param matrix: actual state of matrix
    :param domain: actual domain for choosing row to append
    :return: removes from the domain rows which will not satisfy the problem
    '''
    new_domain = []
    summed_rows = matrix[-2:, :].sum(axis=0)
    for row in domain:
        doubled_row = 2 * row
        if 0. not in summed_rows - doubled_row:
            new_domain.append(row)
    return new_domain


def append_rows(matrix, domain):
    if matrix.shape[0] > 1:
        checked_domain = forward_check(matrix, domain)
    else:
        checked_domain = domain
    for row in checked_domain:
        '''Add vector to matrix and check constraints'''
        matrix = np.append(matrix, row, axis=0)
        # print(matrix, '\n')
        if matrix.shape[0] == matrix.shape[1] and constraint_satisfied(matrix):
            return matrix
        elif constraint_satisfied(matrix):
            actual_domain = domain[:]
            actual_domain = del_from_domain(actual_domain, row)
            return append_rows(matrix, actual_domain)
        matrix = matrix[:-1, :]
    return


def solve_mosaic(rows):
    j = 0
    for row in rows:
        j += 1
        '''Set the first row and remove it from the domain'''
        matrix = row
        domain = rows[:]
        i = 0
        domain = del_from_domain(domain, matrix)
        '''Start recurse'''
        ret = append_rows(matrix, domain)
        if ret is not None:
            print("SOLVED")
            print(ret)
            return ret
    print("THERE IS NO SOLUTION FOR MOSAIC PROBLEM OF SIZE", rows[0].shape[1])
    return

if __name__ == "__main__":
    map_size = int(input("Please specify the size: "))
    start = time.time()
    all_rows = []
    create_rows(map_size, all_rows)
    all_rows = make_rows_vectors(all_rows)
    solve_mosaic(all_rows)
    finish = time.time()
    print("It took ", finish-start, "s to solve mosaic")
