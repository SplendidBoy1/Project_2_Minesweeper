from itertools import combinations

def list_to_dict(variables):
    dict_variables = dict()

    for variable in variables:
        dict_variables[variable] = 1
    return dict_variables

def dict_to_list(variables, dict_variables):
    return [variable*dict_variables[variable] for variable in variables]

def check_valid_answer(cnf, dict_variables):
    '''
        Input: cnf: list các câu cnf cần kiểm tra
                dict_variables: bảng map phần tử với dấu của nó (Vd: {2: -1}  == -2)
    '''
    for cnf_clause in cnf:
        satisfied = False
        for item in cnf_clause:
            # vì mỗi câu cnf gồm các phần tử hội với nhau nên chỉ cần 1 phần tử đúng thì cả câu đúng
            if(abs(item)*dict_variables[abs(item)] == item):
                satisfied = True
                break
        if(not satisfied):
            return False    
    return True

def brute_force_cnf_util(variables, index, cnf, dict_variables):
    if(index == len(variables)):
        if(check_valid_answer(cnf, dict_variables)):
            return dict_variables
        return None
    
    result = brute_force_cnf_util(variables, index+1, cnf, dict_variables)
    if (result != None):
        return result
    
    dict_variables[variables[index]] = -1
    result = brute_force_cnf_util(variables, index+1, cnf, dict_variables)
    if (result != None):
        return result
    
    dict_variables[variables[index]] = 1
    return None

def brute_force_cnf(variables, cnf):
    dict_variables = list_to_dict(variables)

    result = brute_force_cnf_util(variables, 0, cnf, dict_variables)

    return dict_to_list(variables, result)

def mark(dict_variables, index_list):
    for i in index_list:
        dict_variables[i] = -1

def unmark(dict_variables, index_list):
    for i in index_list:
        dict_variables[i] = 1

def brute_force_cnf_combination(variables, cnf):
    dict_variables = list_to_dict(variables)

    for i in range(len(variables)):
        for item in combinations(variables, i+1):
            mark(dict_variables, item)
            if (check_valid_answer(cnf, dict_variables)):
                return dict_to_list(variables, dict_variables)
            unmark(dict_variables, item)
    return None

