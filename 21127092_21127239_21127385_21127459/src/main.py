from fileProcessor import FileProcessor
from makeCNF import *
from Pysat.PySAT import pysat_cnf
from BruteForce.bruteForce import brute_force_cnf, brute_force_cnf_combination
from A_star.A_star_cnf import A_star_cnf
from Backtracking.backtracking import backtracking_cnf
from planBomb import *
import sys, os, time

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Missing input file path. Please try again.")
        sys.exit(1)
    file_path = sys.argv[1]
    if not os.path.isabs(file_path):
        file_path = os.path.abspath(file_path)

    print(file_path)
    if not os.path.exists(file_path):
        print("Non-existent file path")
        sys.exit(1)

    # Đọc input
    input_board = FileProcessor.read_file(file_path)
    print('Input board: ')
    for row in input_board:
        print(row)

    # Tạo CNF
    print("----------------------------------------")
    print("Automatically generating CNFs...")
    cnf_clauses, pending_cells = generate_cnf_from_input(input_board)
    print("Generated CNFs for input board:")
    print(cnf_clauses)
    print("Number of clauses: {count}".format(count = len(cnf_clauses)))

    # Dùng các giải thuật giải CNF
    print("----------------------------------------")
    print("Select algorithm to solve CNF")
    print("1. PySAT")
    print("2. A*")
    print("3. Brute Force")
    print("4. Backtracking")
    choice = int(input("Enter your choice: "))

    result = None
    print("----------------------------------------")
    match choice:
        case 1:
            print("Solving CNF with PySAT...")
            start = time.time()

            result = pysat_cnf(cnf_clauses)

            end = time.time()
            print("Result: ", end='')
            print(result)
            print("Elapsed time: {time:.15f}s".format(time = end-start))
            
        case 2:
            print("Solving CNF with A*...")
            start = time.time()

            result = A_star_cnf(cnf_clauses)

            end = time.time()
            print("Result: ", end='')
            print(result)
            print("Elapsed time: {time:.15f}s".format(time = end-start))
            
        case 3:
            print("Solving CNF with Brute Force...")
            start = time.time()

            result = brute_force_cnf(pending_cells, cnf_clauses)

            end = time.time()
            print("Result: ", end='')
            print(result)
            print("Elapsed time: {time:.15f}s".format(time = end-start))
            
        case 4:
            print("Solving CNF with Backtracking...")
            start = time.time()

            result = backtracking_cnf(cnf_clauses)

            end = time.time()
            print("Result: ", end='')
            print(result)
            print("Elapsed time: {time:.15f}s".format(time = end-start))
            
        case default:
            print("Not an option")

    # In kết quả vào file ouput
    print("----------------------------------------")
    print("Writing result board to output.txt...")
    FileProcessor.write_file("output.txt", plan_bombs(input_board, result))