#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random

'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    ord_type(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    ord_type returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''


def ord_random(csp):
    '''
    ord_random(csp):
    A var_ordering function that takes a CSP object csp and returns a Variable object var at random.  var must be an unassigned variable.
    '''
    var = random.choice(csp.get_all_unasgn_vars())
    return var


def val_arbitrary(csp,var):
    '''
    val_arbitrary(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a value in var's current domain arbitrarily.
    '''
    return var.cur_domain()


def ord_mrv(csp):
    '''
    ord_mrv(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var, 
    according to the Minimum Remaining Values (MRV) heuristic as covered in lecture.  
    MRV returns the variable with the most constrained current domain 
    (i.e., the variable with the fewest legal values).
    '''
    #IMPLEMENT
    vars_list = csp.get_all_unasgn_vars()
    min_val = 99999
    for var in vars_list:
        if var.cur_domain_size() < min_val:
            min_val = var.cur_domain_size()
            min_var = var
    return min_var
        
def ord_dh(csp):
    '''
    ord_dh(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to the Degree Heuristic (DH), as covered in lecture.
    Given the constraint graph for the CSP, where each variable is a node, 
    and there exists an edge from two variable nodes v1, v2 iff there exists
    at least one constraint that includes both v1 and v2,
    DH returns the variable whose node has highest degree.
    '''    
#IMPLEMENT
    vars = csp.get_all_unasgn_vars()
    constr = csp.get_all_cons()
    track = {}
    for cons in constr:
        for i in cons.get_scope():
            if cons.get_unasgn_vars().count(i) != 0:
                if i not in track:
                    track[i] = len(cons.get_unasgn_vars())
                else:
                    k = track[i]
                    track[i] = k + len(cons.get_unasgn_vars())
    result = max(track, key=track.get)
    return result

def val_lcv(csp,var):
    '''
    val_lcv(csp,var):
    A val_ordering function that takes CSP object csp and Variable object var,
    and returns a list of Values [val1,val2,val3,...]
    from var's current domain, ordered from best to worst, evaluated according to the 
    Least Constraining Value (LCV) heuristic.
    (In other words, the list will go from least constraining value in the 0th index, 
    to most constraining value in the $j-1$th index, if the variable has $j$ current domain values.) 
    The best value, according to LCV, is the one that rules out the fewest domain values in other 
    variables that share at least one constraint with var.
    '''    
#IMPLEMENT 
    result = {}
    domain = var.cur_domain() 
    constr = csp.get_cons_with_var(var)
    for k in domain:
        var.assign(k)
        count = 0
        for con in constr:
            for v in con.get_unasgn_vars():
                for t in v.cur_domain():
                    if con.has_support(v,t)==False:
                        count += 1
        var.unassign()
        result[k] = count
    return sorted(result, key = result.get, reverse=False)    
    

def ord_custom(csp):
    '''
    ord_custom(csp):
    A var_ordering function that takes CSP object csp and returns Variable object var,
    according to a Heuristic of your design.  This can be a combination of the ordering heuristics 
    that you have defined above.
    '''    
#IMPLEMENT
    #use DH if all dimain sizes are the same for all variables, otherwise use MRV
    for i in csp.get_all_unasgn_vars():
        for k in csp.get_all_unasgn_vars():
            if k != i:
                if k.cur_domain_size() != i.cur_domain_size():
                    return ord_mrv(csp)      
    return ord_dh(csp)
