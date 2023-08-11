
#Tim ra cac bien tu CNF
def find_list_var(CNF_clauses):
    result = set()
    for clause in CNF_clauses:
        for i in clause:
            result.add(abs(i))
    return list(result)

#Tao ini_state cho thuat toan A*
def mapping_var_ini_state(ls_vars):
    state = dict()
    for i in ls_vars:
        state[i] = 0
    return state
