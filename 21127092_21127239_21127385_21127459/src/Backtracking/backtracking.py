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
    
    if(len(cnf)==0) and ((variable_domains[var]) for var in cnf):
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
                
                
                if(len(updated_cnf)==0) and ((variable_domains[var]) for var in cnf):
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


#example_cnf = [[4, 5], [2, 5], [2, 4], [-2, -4, -5]]
example_cnf = [
    [5], [2], [4, 7, 8], [2, 7, 8], [2, 4, 8], [2, 4, 7], [-4, -7, -8],
    [-2, -7, -8], [-2, -4, -8], [-2, -4, -7], [10], [7], [5], [2], [10],
    [5], [8, 10, 12], [7, 10, 12], [7, 8, 12], [7, 8, 10], [-8, -10, -12],
    [-7, -10, -12], [-7, -8, -12], [-7, -8, -10]
]

# example_cnf = [[1, 3, 12], [-3, -12], [-1, -12], [-1, -3], [3, 5, 12], [-5, -12], [-3, -12], [-3, -5], [5, 7, 16], [-7, -16], [-5, -16], [-5, -7], [1, 19], [-1, -19], [1, 3, 12, 19], [-12, -19], [-3, -19], [-3, -12], [-1, -19], [-1, -12], [-1, -3], [3, 5, 12], [-5, -12], [-3, -12], [-3, -5], [5], [5, 7, 16], [-7, -16], [-5, -16], [-5, -7], [12, 19, 28, 30], [-28, -30], [-19, -30], [-19, -28], [-12, -30], [-12, -28], [-12, -19], [12, 30], [-12, -30], [30, 32], [12, 32], [12, 30], [-12, -30, -32], [32], [16, 32], [-16, -32], [16, 17, 35], [-17, -35], [-16, -35], [-16, -17], [16, 17, 18, 35], [-18, -35], [-17, -35], [-17, -18], [-16, -35], [-16, -18], [-16, -17], [17, 18, 35], [-18, -35], [-17, -35], [-17, -18], [19, 28, 30, 37], [-30, -37], [-28, -37], [-28, -30], [-19, -37], 
# [-19, -30], [-19, -28], [32], [30], [43], [32], [43], [35], [35], [28, 30, 37, 46, 47, 48], [-47, -48], [-46, -48], [-46, -47], [-37, -48], [-37, -47], [-37, -46], [-30, -48], [-30, -47], [-30, -46], [-30, -37], [-28, -48], [-28, -47], [-28, -46], [-28, -37], [-28, -30], [30, 47, 48, 49], [-48, -49], [-47, -49], [-47, -48], [-30, -49], [-30, -48], [-30, -47], [32, 48, 49, 50], [30, 48, 49, 50], [30, 32, 49, 50], [30, 32, 48, 50], [30, 32, 48, 49], [-48, -49, -50], [-32, -49, -50], [-32, -48, -50], [-32, -48, 
# -49], [-30, -49, -50], [-30, -48, -50], [-30, -48, -49], [-30, -32, -50], [-30, -32, -49], [-30, -32, -48], [32, 49, 50], [-49, -50], [-32, -50], [-32, -49], [50, 52], [43, 52], [43, 50], [32, 52], [32, 50], [32, 43], [-32, -43, -50, -52], [52, 54], [43, 54], [43, 52], [35, 54], [35, 52], [35, 43], [-35, -43, -52, -54], [35, 54], [-35, -54], [52, 59, 61], [50, 59, 61], [50, 52, 61], [50, 52, 59], [43, 59, 61], [43, 52, 61], [43, 52, 59], [43, 50, 61], [43, 50, 59], [43, 50, 52], [-50, -52, -59, -61], [-43, -52, -59, -61], [-43, -50, -59, -61], [-43, -50, -52, -61], [-43, -50, -52, -59], [54, 61, 63], [52, 61, 63], [52, 54, 63], [52, 54, 61], [43, 61, 63], [43, 54, 63], [43, 54, 61], [43, 52, 63], [43, 52, 61], [43, 52, 54], [-52, -54, -61, -63], [-43, -54, -61, -63], [-43, -52, -61, -63], [-43, -52, -54, -63], [-43, -52, -54, -61], [52, 59, 61], [50, 59, 61], [50, 52, 61], [50, 52, 59], [-52, -59, -61], [-50, -59, -61], [-50, -52, -61], [-50, -52, -59], [54, 61, 63, 72], [52, 61, 63, 72], [52, 54, 63, 72], [52, 54, 61, 72], [52, 54, 61, 63], [-61, -63, -72], [-54, -63, -72], [-54, -61, -72], [-54, -61, -63], [-52, -63, -72], [-52, -61, -72], [-52, -61, -63], [-52, -54, -72], [-52, -54, -63], [-52, -54, -61], [55, 56, 74], [-56, -74], [-55, -74], [-55, -56], [55, 56, 57, 74], [-57, -74], [-56, -74], [-56, -57], [-55, -74], [-55, -57], [-55, -56], [56, 57, 58, 67, 74, 76], [-74, -76], [-67, -76], [-67, -74], [-58, -76], [-58, -74], [-58, -67], [-57, -76], [-57, -74], [-57, -67], [-57, -58], [-56, -76], [-56, -74], [-56, -67], [-56, -58], [-56, -57], [58, 59, 67, 76, 78], [-76, -78], [-67, -78], [-67, -76], [-59, -78], [-59, -76], [-59, -67], [-58, -78], [-58, -76], [-58, -67], [-58, -59], [61, 78], [59, 78], [59, 61], [-59, -61, -78], [78, 80], [61, 80], [61, 78], [-61, 
# -78, -80], [61, 63, 72, 80, 81], [-80, -81], [-72, -81], [-72, -80], [-63, -81], [-63, -80], [-63, -72], [-61, -81], [-61, -80], [-61, -72], [-61, -63], [74], [67, 74, 76], [-74, -76], [-67, -76], [-67, -74], [67, 76, 78], [-76, -78], [-67, -78], [-67, -76], [78, 80], [-78, -80]]
# #variable_domains = create_variable_domains(example_cnf)
# print('love at')
# print(variable_domains)

# simplified_result, updated_domains = simplify_cnf_and_update_domains(example_cnf, variable_domains)
# updated_domains= dict(sorted(updated_domains.items(), key=lambda item: item[1]))
# backtracked_result, backtracked_domains = backtrack_simplify_domains(simplified_result, updated_domains)

# print("Original CNF:")
# print(example_cnf)

# print('after update')
# print(simplified_result)
# print(updated_domains)
# print("Backtracked CNF and Domains:")
# print(backtracked_result)
# print(backtracked_domains)

# variable_domains = create_variable_domains(example_cnf)

# simplified_result, updated_domains = simplify_cnf_and_update_domains(example_cnf, variable_domains)

# updated_domains= dict(sorted(updated_domains.items(), key=lambda item: item[1]))

# print("Original CNF:")
# print(example_cnf)

# print("Simplified CNF after removing unaries:")
# print(simplified_result)

# print("Updated Variable Domains:")
# print(updated_domains)

# backtracked_domains = backtrack_simplify_domains(simplified_result, updated_domains)
# print("Backtracked CNF and Domains:")
# #print(backtracked_result)
# print(backtracked_domains)