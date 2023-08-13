import copy

def decode_var(index, num_cols):
    row = (index - 1) // num_cols
    col = (index - 1) % num_cols
    return row, col

def plan_bombs(input_board, cnf_result):
    result = copy.deepcopy(input_board)
    n = len(result)
    if(cnf_result != None):
        for index in cnf_result:
            if index < 0:
                continue
            row, col = decode_var(index, n)
            result[row][col] = 'X'
    return result
