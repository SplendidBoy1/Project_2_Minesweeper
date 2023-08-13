def format_board(board):
    # Convert the board to a list of lists of integers
    formatted_board = []
    for row in board:
        formatted_row = []
        for cell in row:
            formatted_row.append(cell)
        formatted_board.append(formatted_row)
    return formatted_board

def get_adjacent_cells(i, j, m, n,input_board):
    # Get a list of adjacent cells to a given cell (i, j)
    # lấy các vị trí để từ position hiện tại thao tác với các vị trí kề đơn vị sẽ rra các vị trí kề
    
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    adjacent_cells = []
    for dx, dy in directions:
        x, y = i + dx, j + dy
        
        if 0 <= x < m and 0 <= y < n:
            if input_board[x][y] > 0 :
                continue
            else:
                adjacent_cells.append((x, y))
    return adjacent_cells

def var(i, j, n):
    # biến đổi tọa độ thành chỉ số index trong mảng
    # Convert cell coordinates (i, j) to a variable index
    return i * n + j + 1

def generate_subarrays_recursive(arr, k):
    result = []
    n = len(arr)
    
    if k -1 <= 0:
        return [arr] if len(arr) > 0 else []
    
    for i in range(n):
        subarray = arr[:i] + arr[i+1:]
        subarrays = generate_subarrays_recursive(subarray, k - 1)
        result.extend(subarrays)
    
    return result

def remove_duplicates(arrays):
    seen_arrays = set()
    result = []
    for arr in arrays:
        arr_tuple = tuple(arr)
        if arr_tuple not in seen_arrays:
            seen_arrays.add(arr_tuple)
            result.append(arr)
    return result

def convert_pending_cells(arr):
    flat_array = [item for sublist in arr for item in sublist]

    unique_elements = list(dict.fromkeys(flat_array))
    return unique_elements

def make_final_cnf(cnf_clauses):
    cnf_clauses  = [item for sublist in cnf_clauses for item in sublist]
    unique_subarrays = []
    for subarray in cnf_clauses:
        # Nếu mảng con chưa tồn tại trong danh sách unique_subarrays, thì thêm vào
        if subarray not in unique_subarrays:
            unique_subarrays.append(subarray)
    return unique_subarrays

def generate_cnf_from_input(input_board):
    m, n = len(input_board), len(input_board[0])
    # List for storing cnf clauses
    cnf_clauses = []
    # List for storing cells' index that can be bombs
    pending_cells = []

    # Loop through each cell in the input board
    for i in range(m):
        for j in range(n):
            #đối với mỗi ô
            cell_value = input_board[i][j]
            # If the cell is not empty, it contains a number (not a mine)
            if cell_value != 0: 
                # b1: đi tìm các ô kề với ô hiện tại mà là ô chứa số 0
                adjacent_cells = get_adjacent_cells(i, j, m, n, input_board)

                # b2: chuyển đổi vị trí i, j của các ô có thể có mìn
                # thành index của mảng 1 chiều để biểu thị CNF
                adjacent_mine_vars = [var(x, y, n) for x, y in adjacent_cells]
                adjacent_mine_vars_negated = [-var(x, y, n) for x, y in adjacent_cells]

                pending_cells.append(adjacent_mine_vars)
                
                num_adj_cells = len(adjacent_mine_vars)

                # b3: tìm các CNF clause
                # Constraint L: với mọi n(số lượng ô kề)-k(số lượng bom)+1 ô, có ít nhất 1 ô có bom
                L = generate_subarrays_recursive(adjacent_mine_vars, cell_value)
                L = remove_duplicates(L)
                cnf_clauses.append(L)
                if(cell_value != num_adj_cells):
                    # Constraint U: với mọi k(số lượng bom)+1 ô, có ít nhất 1 ô không có bom
                    U = generate_subarrays_recursive(adjacent_mine_vars_negated, num_adj_cells - cell_value)
                    U = remove_duplicates(U)
                    cnf_clauses.append(U)   
                    
    cnf_clauses = make_final_cnf(cnf_clauses)
    pending_cells = convert_pending_cells(pending_cells)                
    return cnf_clauses, pending_cells