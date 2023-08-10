from itertools import combinations, permutations

boom = 10

matrix = [[1, 1, -1, -1], [-2, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]]

adj = list()

x_positions = [-1, -1, -1, 0, 0, 1, 1, 1]
y_positions = [-1, 0, 1, -1, 1, -1, 0, 1]

index_position = [0, 1, 2, 3, 4, 5, 6, 7]

#khoi tao de ra co bao nhieu o ke voi so
def Input_State(matrix):
    rows = len(matrix)
    cols = len(matrix[0])
    for i in range(len(matrix)):
        temp = []
        for j in range(len(matrix[0])):
            if i == 0 or j == 0 or i == rows - 1 or j == cols - 1:
                if i == j or abs(i - j) == rows - 1 or abs(i - j) == cols - 1:
                    temp.append(3)
                else:
                    temp.append(5)
            else:
                temp.append(8)
        adj.append(temp)
    return adj

def CNF_clause(clause, k, n):
    print('cls:', clause)
    print('k:', k)
    print('n:', n)
    if k == 0:
        flag = bool()
        for i in range(n):
            check_pos = clause[i]
            if matrix[check_pos[0]][check_pos[1]] != -2:
                flag = True
            else:
                flag = False
                break
        if flag:
            return n + 1
        else:
            return -1
        return -1
    elif k == n:
        flag = bool()
        for i in range(n):
            check_pos = clause[i]
            if matrix[check_pos[0]][check_pos[1]] == -2:
                flag = True
            else:
                flag = False
                break
        if flag:
            return k
        else:
            return -1
    index = clause[n - 1]
    # if matrix[index[0]][index[1]] == 10:
    # print('matrix:', matrix[index[0]][index[1]])
    # return (bool(not(matrix[index[0]][index[1]] == -2)) or bool(CNF_clause(clause, k - 1 , n - 1))) and (bool(matrix[index[0]][index[1]] == -2) or bool(CNF_clause(clause, k, n - 1)))
    if matrix[index[0]][index[1]] == -2:
        return CNF_clause(clause, k - 1, n - 1)
    else:
        return CNF_clause(clause, k, n - 1)

def makeCNF():
    num_row = len(matrix)
    num_col = len(matrix[0])
    clauses = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] > -1:
                # less = combinations([0, 1, 2, 3, 4, 5, 6, 7], adj[i][j] - matrix[i][j] + 1)
                # most = combinations([0, 1, 2, 3, 4, 5, 6, 7], matrix[i][j] + 1)
                #clause that has index
                clause = []
                for one in index_position:
                    x = i + x_positions[one]
                    y = j + y_positions[one]
                    if x < 0 or y < 0 or x > num_row - 1 or y > num_col - 1:
                        continue
                    elif matrix[x][y] > -1:
                        adj[i][j] -= 1
                        continue
                    clause.append([x, y])
                clauses.append(clause)
    return clauses

Input_State(matrix)                     
vectors = makeCNF()
print(adj)
flag = CNF_clause(vectors[0], matrix[0][0], adj[0][0])
print(flag)
# print(Input_State(matrix))

def CNF():
    pass