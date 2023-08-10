from pysat.solvers import Glucose3
from itertools import combinations, permutations
# Input and output boards (replace with your actual input and output)
input_board = [
    [0, 0, 0],
    [1, 1, 1]
]

# output_board = [
#     [3, 'X', 0, 0],
#     ['X', 'X', 0, 0],
#     [0, 0, 0, 0]
# ]

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

    # Loop through each cell in the input board
    for i in range(m):
        for j in range(n):
            #đối với mỗi ô
            cell_value = input_board[i][j]
            # If the cell is not empty, it contains a number (not a mine)
            if cell_value != 0:
                
                cnf_clauses.append([-var(i, j, n)])
               
                #b1: đi tìm các ô kề với ô hiện tại, có 
                adjacent_cells = get_adjacent_cells(i, j, m, n,input_board)
                
                
                #print("vị trí kề:")
                #print(adjacent_cells)
                # b2: chuyển đổi vị trí i,j của các ô có thể có mìn
                # thành index của mảng 1 chiều để biểu thị CNF
                adjacent_mine_vars = [var(x, y, n) for x, y in adjacent_cells]
                adjacent_mine_vars_negated = [-var(x, y, n) for x, y in adjacent_cells]
                soluongke = len(adjacent_mine_vars)
                
                #print("vị trí trong mảng của các ô có thể chứa mìn: ")
                #print(adjacent_mine_vars)

                # Generate clauses to satisfy the cell's number constraint
                #b3: tạo mệnh đề: nếu ô hiện tại i,j không chưa mìn thì các ô lân cận
                # có thể chứa mìn
                #[-var(i, j, n)] +
                
                L = generate_subarrays_recursive(adjacent_mine_vars, cell_value)
                L = remove_duplicates(L)
                cnf_clauses.append(L)
                if(cell_value != soluongke):
                    U = generate_subarrays_recursive(adjacent_mine_vars_negated, soluongke - cell_value)
                    U = remove_duplicates(U)
                    cnf_clauses.append(U)   
                    
                #cnf_clauses.append(adjacent_mine_vars)
                # phải xét có ít nhất các ô lận cận chưa mình từ 1 -> giá trị max 
                # để đảm bảo không bị xót
                # for k in range(1, cell_value + 1):
                #     # Generate clauses to ensure there are at least k mines around the cell
                #     for mine_comb in get_combinations(adjacent_mine_vars, k):
                #         #mine_comb sẽ là những sự kết hợp giữa các ô mìn
                #         #kết hợp tiếp giữa có ít nhất k ô mìn với ô hiện tại không có mìn
                #         # nếu ô hiện tại không có mình
                #         #thì có ít nhất k ô lân cận chứa mìn
                #         #
                #         print("check mine_comb")
                #         print(mine_comb)
                #         mine_clause = [-var(i, j, n)] + mine_comb
                #         cnf_clauses.append(mine_clause)
                        
    return cnf_clauses

def get_adjacent_cells(i, j, m, n,input_board):
    # Get a list of adjacent cells to a given cell (i, j)
    # lấy các vị trí để từ position hiện tại thao tác với các vị trí kề đơn vị sẽ rra các vị trí kề
    
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    adjacent_cells = []
    for dx, dy in directions:
        x, y = i + dx, j + dy
        
        if 0 <= x < m and 0 <= y < n:
            if(input_board[x][y] > 0):
                continue
            else:
                adjacent_cells.append((x, y))
    return adjacent_cells
#biểu diễn trạng thái của ô chứa mìn
def var(i, j, n):
    # biến đổi tọa độ thành  chỉ số index trong mảng
    # Convert cell coordinates (i, j) to a variable index
    return i * n + j + 1

def get_combinations(lst, k):
    # Get all combinations of length k from a list lst
    #kết hợp k phần tử trong mảng lại với nhau
    # ví dụ: danh sách có: 1 2 3 
    #                      4 5 6
    # k = 2 thì 12, 13, 14,...
    return [list(comb) for comb in combinations(lst, k)]
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

# Convert input and output boards to lists of lists of integers
#input_board = format_board(input_board)


#output_board = format_board(output_board)

# Generate CNF clauses from the input board
#cnf_clauses = generate_cnf_from_input(input_board)

# TODO: Solve the CNF clauses to find mine positions
# ...

#Print the CNF clauses (for demonstration purposes)
# for clause in cnf_clauses:
#     print(clause)

