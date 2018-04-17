from hitori_csp import *
from propagators import *
from orderings import *


def solve_hitori(initial_hitori_board, propType, var_ord_type, val_ord_type, trace=False):
    csp = hitori_csp_model(initial_hitori_board)[0]
    solver = BT(csp)
    if trace:
        solver.trace_on()
    if propType == 'BT':
        solver.bt_search(prop_BT, var_ord_type, val_ord_type)


if __name__ == "__main__":
    solve_hitori([[4, 8, 1, 6, 3, 2, 5, 7], [3, 6, 7, 2, 1, 6, 5, 4], [2, 3, 4, 8, 2, 8, 6, 1], [4, 1, 6, 5, 7, 7, 3, 5],
                  [7, 2, 3, 1, 8, 5, 1, 2], [3, 5, 6, 7, 3, 1, 8, 4], [6, 4, 2, 3, 5, 4, 7, 8], [8, 7, 1, 4, 2, 3, 5, 6]],
                 'BT', ord_mrv, val_lcv)
