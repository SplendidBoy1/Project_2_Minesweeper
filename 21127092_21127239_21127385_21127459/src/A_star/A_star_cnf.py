import heapq
from copy import deepcopy
from abc import ABC, abstractmethod

class Search(ABC):
    @property
    @abstractmethod
    def solve_problem(self, problem, measure):
        pass

class Node(ABC):
    def __init__(self, cur_state):
        self.cur_state = cur_state

class Problem:
    def __init__(self, ini_state, CNF_clauses):
        self.ini_state = ini_state
        self.path_cost = 0
        self.CNF_clauses = CNF_clauses
    
    def goal_test(self, state):
        num_wrong = 0
        for clause in self.CNF_clauses:
            #bien de xem clause co dung hay khong
            flag = bool()
            for sen in clause:
                if sen > 0:
                    if state[sen] == 0:
                        flag = False
                        continue
                    else:
                        flag = True
                        break
                else:
                    if state[abs(sen)] == 0:
                        flag = True
                        break
                    else:
                        flag = False
                        continue
            if flag == True:
                continue
            else:
                num_wrong += 1
        return num_wrong
        
    def actions(state):
        # the list of state that can action
        result = []
        for i in state:
            result.append([i, not(state[i])])
        return result

class Node_A_star(Node):
    #constructor
    def __init__(self, cur_state : dict, cost, heuristic):
        super().__init__(cur_state)
        self.cost = cost
        self.heuristic = heuristic
        
    #to string
    
    def __eq__(self, other):
        return self.cur_state == other.cur_state
    
    def __ne__(self, other):
        return self.cur_state != other.cur_state

    def __lt__(self, other):
        return (self.cost < other.cost)

    def __gt__(self, other):
        return (self.cost > other.cost)

    def __le__(self, other):
        return (self.cost < other.cost)

    def __ge__(self, other):
        return (self.cost > other.cost)
           
    @staticmethod
    def child_node(problem, node, action):   
        child_state = node.cur_state.copy()
        child_state[action[0]] = action[1]
        # print(child_state)
        child_heuristic = problem.goal_test(child_state)
        # print(child_heuristic)
        child_node = Node_A_star(child_state.copy(), node.cost - node.heuristic + 1 + child_heuristic, child_heuristic)
        return child_node

class A_star(Search):
    def __init__(self):
        self.frontier = []
        self.explored = set()
    
    def solve_problem(self, problem):
    #create initial node
        ini_state = problem.ini_state
        heuristic = problem.goal_test(ini_state)
        node = Node_A_star(ini_state, problem.path_cost + heuristic, heuristic)
    #create a list to store, solution is each step that can has a result and save as list
    #frontier is a queue
    #create frontier in initial node
        heapq.heappush(self.frontier, node)
    # sort frontier
        while(len(self.frontier)):
            temp = heapq.heappop(self.frontier)
            self.explored.add(tuple(temp.cur_state))
            if temp.heuristic == 0:
                return temp.cur_state
            for action in Problem.actions(temp.cur_state):
                child = Node_A_star.child_node(problem, temp, action)
                # print(child.cur_state)
                if tuple(child.cur_state.values()) not in self.explored and child not in self.frontier:
                    heapq.heappush(self.frontier, child)
        return 0

#Tim ra cac bien tu CNF
def find_list_var(CNF_clauses):
    result = set()
    for clause in CNF_clauses:
        for i in clause:
            result.add(abs(i))
    return list(result)

#Tao ini_state cho thuat toan A*
def mapping_var_ini_state(ls_vars):
    state = dict()
    for i in ls_vars:
        state[i] = 0
    return state

# matrix = [
#     [1, 0, 0],
#     [0, 0, 0],
#     [0 , 0, 0]
# ]

# matrix = [
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

# input_board = format_board(matrix)
# cnf_clauses = generate_cnf_from_input(input_board)
# cnf_clauses  = [item if isinstance(item, list) else [item] for sublist in cnf_clauses for item in sublist]
# print(cnf_clauses)
def A_star_cnf(cnf_clauses):
    list_vars = find_list_var(cnf_clauses)
    ini_state = mapping_var_ini_state(list_vars)

# result = []
# for i in ini_state:
#     result.append([i, not(ini_state[i])])
# print(result)
    problem = Problem(ini_state, cnf_clauses)
    search = A_star()
    result = search.solve_problem(problem)
    ls_cnf = []
    for i in result:
        if result[i] == True or result[i] == 1:
            ls_cnf.append(i)
        else:
            ls_cnf.append(-i)
    return ls_cnf
# print(list_bomb)
# print(result)