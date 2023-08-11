import heapq
import time
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
        return (self.cost < other.cost) or (self.cost == other.cost)

    def __ge__(self, other):
        return (self.cost > other.cost) or (self.cost == other.cost)
           
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
        # print(node.cur_state)
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

# x_positions = [-1, -1, -1, 0, 0, 1, 1, 1]
# y_positions = [-1, 0, 1, -1, 1, -1, 0, 1]

# index_position = [0, 1, 2, 3, 4, 5, 6, 7]

# #khoi tao de ra co bao nhieu o ke voi so
# def Input_State(matrix):
#     rows = len(matrix)
#     cols = len(matrix[0])
#     for i in range(len(matrix)):
#         temp = []
#         for j in range(len(matrix[0])):
#             if i == 0 or j == 0 or i == rows - 1 or j == cols - 1:
#                 if i == j or abs(i - j) == rows - 1 or abs(i - j) == cols - 1:
#                     temp.append(3)
#                 else:
#                     temp.append(5)
#             else:
#                 temp.append(8)
#         adj.append(temp)
#     return adj

# def CNF_clause(clause, k, n):
#     print('cls:', clause)
#     print('k:', k)
#     print('n:', n)
#     if k == 0:
#         flag = bool()
#         for i in range(n):
#             check_pos = clause[i]
#             if matrix[check_pos[0]][check_pos[1]] != -2:
#                 flag = True
#             else:
#                 flag = False
#                 break
#         if flag:
#             return n + 1
#         else:
#             return -1
#         return -1
#     elif k == n:
#         flag = bool()
#         for i in range(n):
#             check_pos = clause[i]
#             if matrix[check_pos[0]][check_pos[1]] == -2:
#                 flag = True
#             else:
#                 flag = False
#                 break
#         if flag:
#             return k
#         else:
#             return -1
#     index = clause[n - 1]
#     # if matrix[index[0]][index[1]] == 10:
#     # print('matrix:', matrix[index[0]][index[1]])
#     # return (bool(not(matrix[index[0]][index[1]] == -2)) or bool(CNF_clause(clause, k - 1 , n - 1))) and (bool(matrix[index[0]][index[1]] == -2) or bool(CNF_clause(clause, k, n - 1)))
#     if matrix[index[0]][index[1]] == -2:
#         return CNF_clause(clause, k - 1, n - 1)
#     else:
#         return CNF_clause(clause, k, n - 1)

# def makeCNF():
#     num_row = len(matrix)
#     num_col = len(matrix[0])
#     clauses = []
#     for i in range(len(matrix)):
#         for j in range(len(matrix[0])):
#             if matrix[i][j] > -1:
#                 # less = combinations([0, 1, 2, 3, 4, 5, 6, 7], adj[i][j] - matrix[i][j] + 1)
#                 # most = combinations([0, 1, 2, 3, 4, 5, 6, 7], matrix[i][j] + 1)
#                 #clause that has index
#                 clause = []
#                 for one in index_position:
#                     x = i + x_positions[one]
#                     y = j + y_positions[one]
#                     if x < 0 or y < 0 or x > num_row - 1 or y > num_col - 1:
#                         continue
#                     elif matrix[x][y] > -1:
#                         adj[i][j] -= 1
#                         continue
#                     clause.append([x, y])
#                 clauses.append(clause)
#     return clauses

# Input_State(matrix)                     
# vectors = makeCNF()
# print(adj)
# flag = CNF_clause(vectors[0], matrix[0][0], adj[0][0])
# print(flag)
# # print(Input_State(matrix))

# def CNF():
#     pass