from createCNF import *
from backtracking import *

matrix = [
    [5, 0, 0],
    [0, 0, 0],
    [0, 0, 0]]

input_board = format_board(matrix)
cnf_clauses = generate_cnf_from_input(input_board)
cnf_clauses  = [item if isinstance(item, list) else [item] for sublist in cnf_clauses for item in sublist]

variable_domains = create_variable_domains(cnf_clauses)
simplified_result, updated_domains = simplify_cnf_and_update_domains(cnf_clauses, variable_domains)
updated_domains= dict(sorted(updated_domains.items(), key=lambda item: item[1]))

print("Original CNF:")
print(cnf_clauses)

# print("Simplified CNF after removing unaries:")
# print(simplified_result)

print("Updated Variable Domains:")
print(updated_domains)

backtracked_domains = backtrack_simplify_domains(simplified_result, updated_domains)
result = convert_and_sort_result(backtracked_domains)
print("Result")
#print(backtracked_result)
print(result)