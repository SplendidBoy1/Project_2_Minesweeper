def check_empty_cnf(matrix):
    flag = True
    for element in matrix:
        if element:
            flag = False
    return flag

def convert_and_sort_result(input_dict):
    result_list = []

    for key, value in input_dict.items():
        if next(iter(value)) == 1:
            result_list.append(key)
        else:
            result_list.append(-key)

    sorted_list = sorted(result_list, key=lambda x: abs(x))
    return sorted_list

def create_variable_domains(cnf):
    variable_domains = {}

    for clause in cnf:
        for literal in clause:
            var = abs(literal)
            if var not in variable_domains:
                variable_domains[var] = {1, -1}

    return variable_domains

def simplify_cnf_remove_value(cnf, value_to_remove):
    cleaned_cnf = []
    count = 1
    temp = []
    for clause in cnf:
        if value_to_remove in clause:
            continue
        elif -value_to_remove in clause:
            cleaned_clause = [var for var in clause if var != -value_to_remove]
            cleaned_cnf.append(cleaned_clause)
        else:
            cleaned_cnf.append(clause)

    return cleaned_cnf

def update_variable_domains(variable_domains, unary):
    var = abs(unary)
    opposite_value = -1 if unary > 0 else 1

    if var in variable_domains:
        variable_domains[var] -= {opposite_value}
    #print('\n hjhj domain ne', variable_domains)
    return variable_domains


def simplify_cnf_and_update_domains(cnf, variable_domains):
    while True:
        unary_found = False
        unaries = set()

        # Tìm các giá trị unary trong CNF
        for clause in cnf:
            if len(clause) == 1:
                #print('hhmm', clause[0])
                unary_found = True
                unaries.add(clause[0])

        if not unary_found:
            break

        for unary in unaries:
            #print('unaryyyy phai xoa', unary)
            variable_domains = update_variable_domains(variable_domains, unary)
            cnf = simplify_cnf_remove_value(cnf, unary)
            #print('\n huhu cnf ne', cnf)

    return cnf, variable_domains


def backtrack_simplify_domains(cnf, variable_domains):
    
    if(check_empty_cnf(cnf)) and ((variable_domains[var]) for var in cnf):
        return variable_domains # trường hợp domain ban đầu đã là kết quả
    
    for var, domain in variable_domains.items():
        if len(domain) > 1:
            for value in domain.copy():
                # Thử gán giá trị vào miền của biến
                variable_domains[var] = {value}
                
                # Thêm var đó vào cnf để chút update
                cnf.append([var])
                
                # Cập nhật CNF và miền giá trị
                updated_cnf, updated_domains = simplify_cnf_and_update_domains(cnf, variable_domains)
                # print ('update backtrack', updated_cnf)
                # print('update domain', updated_domains)
                # print ('lennn', len(updated_cnf))
                
                
                if(check_empty_cnf(updated_cnf)) and ((variable_domains[var]) for var in cnf):
                    return updated_domains 
                #elif (len(updated_cnf)0) 
                # Kiểm tra xem miền gán mới có vi phạm CNF hay không
                elif len(updated_cnf) > 0:
                    # Gọi đệ quy để tiếp tục gán và kiểm tra
                    #print('backtrack thoiiii')
                    result_domains = backtrack_simplify_domains(updated_cnf, updated_domains)
                    return result_domains
                    
                # Khôi phục miền giá trị của biến
                variable_domains[var] = domain.copy()
    
    # Trả về None nếu không tìm thấy giải pháp
    return None


# #example_cnf = [[4, 5], [2, 5], [2, 4], [-2, -4, -5]]
# example_cnf = [
#     [5], [2], [4, 7, 8], [2, 7, 8], [2, 4, 8], [2, 4, 7], [-4, -7, -8],
#     [-2, -7, -8], [-2, -4, -8], [-2, -4, -7], [10], [7], [5], [2], [10],
#     [5], [8, 10, 12], [7, 10, 12], [7, 8, 12], [7, 8, 10], [-8, -10, -12],
#     [-7, -10, -12], [-7, -8, -12], [-7, -8, -10]
# ]

def backtracking_cnf(cnf_clauses):
    variable_domains = create_variable_domains(cnf_clauses)
    #simplified_result, updated_domains = simplify_cnf_and_update_domains(cnf_clauses, variable_domains)
    variable_domains= dict(sorted(variable_domains.items(), key=lambda item: item[1]))
    
    backtracked_domains = backtrack_simplify_domains(cnf_clauses, variable_domains)
    result = convert_and_sort_result(backtracked_domains)
    return result