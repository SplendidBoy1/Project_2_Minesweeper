from createCNF import *
from A_star import *
from utility import *

matrix = [
    [0,1,0,1,0,1,0,0,0],
    [1,1,0,1,1,1,0,0,0],
    [0,1,1,2,1,1,1,1,1],
    [0,1,0,2,0,2,2,0,1],
    [0,1,1,2,1,3,0,3,1],
    [0,0,0,0,0,3,0,3,0],
    [0,0,0,0,0,2,0,2,0],
    [1,1,1,0,1,2,2,1,0],
    [1,0,1,0,1,0,1,0,0]
]

input_board = format_board(matrix)
cnf_clauses = generate_cnf_from_input(input_board)
cnf_clauses  = [item if isinstance(item, list) else [item] for sublist in cnf_clauses for item in sublist]
# print(cnf_clauses)
list_vars = find_list_var(cnf_clauses)
ini_state = mapping_var_ini_state(list_vars)

# result = []
# for i in ini_state:
#     result.append([i, not(ini_state[i])])
# print(result)
problem = Problem(ini_state, cnf_clauses)
search = A_star()
result = search.solve_problem(problem)
print(result)
# print(result)