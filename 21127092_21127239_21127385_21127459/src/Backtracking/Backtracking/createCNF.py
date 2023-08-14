# from pysat.solvers import Glucose3
from itertools import combinations, permutations
# Input and output boards (replace with your actual input and output)


def format_board(board):
    # Convert the board to a list of lists of integers
    formatted_board = []
    for row in board:
        formatted_row = []
        for cell in row:
            formatted_row.append(cell)
        formatted_board.append(formatted_row)
    return formatted_board

def generate_cnf_from_input(input_board):
    m, n = len(input_board), len(input_board[0])
    cnf_clauses = []
    mang_comin = []

    # Loop through each cell in the input board
    for i in range(m):
        for j in range(n):
            #đối với mỗi ô
            cell_value = input_board[i][j]
            # If the cell is not empty, it contains a number (not a mine)
            if cell_value != 0:
                
                #cnf_clauses.append([-var(i, j, n)])
               
                
               
                #b1: đi tìm các ô kề với ô hiện tại, có 
                adjacent_cells = get_adjacent_cells(i, j, m, n,input_board)
                
                
                
                # b2: chuyển đổi vị trí i,j của các ô có thể có mìn
                # thành index của mảng 1 chiều để biểu thị CNF
                adjacent_mine_vars = [var(x, y, n) for x, y in adjacent_cells]
                adjacent_mine_vars_negated = [-var(x, y, n) for x, y in adjacent_cells]
                
                
                mang_comin.append(adjacent_mine_vars)
                
                
                soluongke = len(adjacent_mine_vars)
                
           
                
                L = generate_subarrays_recursive(adjacent_mine_vars, cell_value)
                L = remove_duplicates(L)
                cnf_clauses.append(L)
                if(cell_value != soluongke):
                    U = generate_subarrays_recursive(adjacent_mine_vars_negated, soluongke - cell_value)
                    U = remove_duplicates(U)
                    cnf_clauses.append(U)   
                    
             
    convert_mangCoMin(mang_comin)                
    return cnf_clauses


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
#biểu diễn trạng thái của ô chứa mìn
def var(i, j, n):
    # biến đổi tọa độ thành  chỉ số index trong mảng
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
def convert_mangCoMin(arr):
    flat_array = [item for sublist in arr for item in sublist]

# Remove duplicates while preserving order (Python 3.7+)
    unique_elements = list(dict.fromkeys(flat_array))

    #print(unique_elements)
    return unique_elements




