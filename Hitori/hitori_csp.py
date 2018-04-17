from cspbase import *
import itertools

def hitori_csp_model(initial_hitori_board):
    variables = initialize_variables(initial_hitori_board)
    dimension = len(variables)
    hitori_csp = CSP("Hitori_model_1", vars=list(itertools.chain.from_iterable(variables))) 
    #constraints = []
    
    #add row constraints 
    for i in range(dimension):
        row = get_row(variables, i)
        for j in range(dimension):
            for k in range(j + 1, dimension):
                cell_1 = row[j]
                cell_2 = row[k]
                 #Check if the cells are adjacent to each other
                if k == j +1:
                    constr = Constraint(str('row') + cell_1.name + cell_2.name, [cell_1, cell_2])
                    constr.add_satisfying_tuples(satisfy_tuples_model1_case1(cell_1.cur_domain(), cell_2.cur_domain()))                    
                else:    
                    constr = Constraint(str('row') + cell_1.name + cell_2.name, [cell_1, cell_2])
                    constr.add_satisfying_tuples(satisfy_tuples_model1_case2(cell_1.cur_domain(), cell_2.cur_domain()))
                hitori_csp.add_constraint(constr)
              
    #add column constraints 
    for i in range(dimension):
        col = get_column(variables, i)
        for j in range(dimension):
            for k in range(j + 1, dimension):
                cell_1 = col[j]
                cell_2 = col[k]
                #Check if the cells are adjacent to each other
                if k == j+1:
                    constr = Constraint(str('col') + cell_1.name + cell_2.name, [cell_1, cell_2])
                    constr.add_satisfying_tuples(satisfy_tuples_model1_case1(cell_1.cur_domain(), cell_2.cur_domain()))                    
                else:    
                    constr = Constraint(str('col') + cell_1.name + cell_2.name, [cell_1, cell_2])
                    constr.add_satisfying_tuples(satisfy_tuples_model1_case2(cell_1.cur_domain(), cell_2.cur_domain()))
                hitori_csp.add_constraint(constr)
    
    return hitori_csp, variables

####Helper Functions########

def initialize_variables(initial_hitori_board):
    '''Initialize the Hitori board and return the list of initialized variables '''
    dimension = len(initial_hitori_board)
    variables = []
    for row in range(dimension):
        var_list = []
        for column in range(dimension):
            value = initial_hitori_board[row][column]
            var = Variable('V' + str(row+1) + ','+ str(column+1), [0, value])
            var_list.append(var)
        variables.append(var_list)
    return variables

def get_row(board, i):
    '''Return the row i of the grid'''
    return board[i]

def get_column(board, i):
    '''Return the column i of the grid'''
    return [board[k][i] for k in range(len(board))]

def satisfy_tuples_model1_case1(domain1, domain2):
    '''Return a list of all possible satifying tuples for the case that 2 variables are next to each other in Hitori Model 1'''
    return [(x,y) for x in domain1 for y in domain2 if x != y]

def satisfy_tuples_model1_case2(domain1, domain2):
    '''Return a list of all possible satifying tuples for the case that 2 variables are not adjacent to each other in Hitori Model 1'''
    return [(x,y) for x in domain1 for y in domain2 if ((x != y) or ((x==0) or (y==0)))]

def verify_satisfactory_list(li):
    '''Checks if the list of possible variables assignments satifies the constraints of Hitori'''
    if 0 not in li:
        if len(set(li)) == len(li):
            return True
    else:
        for i in range(len(li)):
            if i < len(li) - 1:
                #checks the case where there are adjacent black squares
                if li[i] == 0 and li[i+1] == 0:
                    return False
        list2 = li
        while 0 in list2:
            list2.remove(0) 
        if len(set(list2)) == len(li) - li.count(0):
            return True
        else:
            return False