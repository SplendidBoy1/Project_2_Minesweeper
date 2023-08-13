from pysat.solvers import Glucose3

def pysat_cnf(cnf_clauses):
    # Khởi tạo solver Glucose3
    solver = Glucose3()

    # Thêm các mệnh đề CNF vào solver
    for clause in cnf_clauses:
        solver.add_clause(clause)

    # Giải bài toán SAT    
    if solver.solve():
        return solver.get_model()
    else:
        return None
    