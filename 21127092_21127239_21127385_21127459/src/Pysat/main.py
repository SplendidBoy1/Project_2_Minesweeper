from pysat.solvers import Glucose3
from createCNF import *


def solve_minesweeper(n, m, cnf_clauses):
    # Khởi tạo solver Glucose3
    
    solver = Glucose3()

    # Thêm các mệnh đề CNF vào solver
    for clause in cnf_clauses:
        
        solver.add_clause(clause)
   

    # Giải bài toán SAT
    if solver.solve():
        # Nếu tìm thấy giải pháp
        model = solver.get_model()
     
        minesweeper_solution = parse_solution(model, n, m)
        
        return minesweeper_solution
    else:
        # Không tìm thấy giải pháp
        return None

def parse_solution(model, n, m):
    # Phân tích giải pháp từ model
    minesweeper_solution = [[0] * m for _ in range(n)]
    for var in model:
        
        if var > 0:
            
            i, j = decode_var(model,var ,m)
            
            minesweeper_solution[i][j] = 1 
    
    return minesweeper_solution


def decode_var(arr, value, num_cols):
    index = arr.index(value)
    row = index // num_cols
    col = index % num_cols
    return row, col
   
    #return i, j
def print_minesweeper_solution(solution):
    if solution:
        for row in solution:
            row_str = " ".join(str(cell) if cell == 'X' else str(cell) for cell in row)
            print(row_str)
    else:
        print("Không tìm thấy giải pháp.")



# Sử dụng hàm solve_minesweeper để giải bài toán Minesweeper

# input_board = [
#     [3, 0, 0],
#     [0, 0, 0],
#     [0, 0, 0]
# ]
# input_board = [
#     [1, 0, 0],
#     [0, 0, 0],
#     [0 , 0, 0]
# ]
input_board = [
    [2, 0, 2, 0],
    [0, 4, 0, 0],
    [2, 0, 2, 0]
]



# input_board = [
#     [2, 0, 0, 1],
#     [2, 0, 3, 1],
#     [1, 1, 1, 0]
# ]

# input_board = [
#     [3, 0, 2, 0],
#     [0, 0, 2, 0],
#     [0, 0, 0, 0]
# ]
# input_board = [
#     [0,1,0,1,0,1,0,0,0],
#     [1,1,0,1,1,1,0,0,0],
#     [0,1,1,2,1,1,1,1,1],
#     [0,1,0,2,0,2,2,0,1],
#     [0,1,1,2,1,3,0,3,1],
#     [0,0,0,0,0,3,0,3,0],
#     [0,0,0,0,0,2,0,2,0],
#     [1,1,1,0,1,2,2,1,0],
#     [1,0,1,0,1,0,1,0,0]
# ]


n = len(input_board) # Số hàng
m = len(input_board[0]) # Số cột


input_board = format_board(input_board)

cnf_clauses =generate_cnf_from_input(input_board) 


cnf_clauses  = [item if isinstance(item, list) else [item] for sublist in cnf_clauses for item in sublist]
unique_subarrays = []
for subarray in cnf_clauses:
    # Nếu mảng con chưa tồn tại trong danh sách unique_subarrays, thì thêm vào
    if subarray not in unique_subarrays:
        unique_subarrays.append(subarray)
# print("cnf cuối cùng")
# print(unique_subarrays)

solution = solve_minesweeper(n, m, unique_subarrays)
if solution:
    print_minesweeper_solution(solution)
else:
    print("Không tìm thấy giải pháp.")
