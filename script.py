from ortools.linear_solver import pywraplp

def read(file):
    with open(file, 'r') as f:
        
        n, m = map(int, f.readline().strip().split())

        c = list(map(int, f.readline().strip().split()))

        A = []
        b = []

        for _ in range(m):
           *a, b_value = map(int, f.readline().strip().split())
           A.append(a)
           b.append(b_value) 

    return n, m, c, A, b

def PLSolver(c, A, b):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, None

    x = [solver.NumVar(0, solver.infinity(), f'x{i}') for i in range(len(c))]
    solver.Maximize(solver.Sum(c[i] * x[i] for i in range(len(c))))

    for i in range(len(A)):
        solver.Add(solver.Sum(A[i][j] * x[j] for j in range(len(c))) <= b[i])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        f_max = solver.Objective().Value()
        x_max = [var.solution_value() for var in x]
        return f_max, x_max
    else:
        return None, None
    
def BranchAndBound(c, A, b):
    best_solution = None
    best_value = float('-inf')

    subproblems = [({'c': c, 'A': A, 'b': b}, 'P0')]

    while subproblems:
        subproblem, label = subproblems.pop(0)
        
        f_max, x_max = PLSolver(subproblem['c'], subproblem['A'], subproblem['b'])

        if f_max is not None and f_max > best_value:
            if all(x.is_integer() for x in x_max):
                best_value = f_max
                best_solution = x_max
                print(f"Subproblema: {label}")
                print(f"Função Objetivo: {f_max}")
                print(f"Solução: {x_max}")
                print("Poda por Inteiro")
            
            else:

                for i, x_val in enumerate(x_max):
                    if not x_val.is_integer():
                        
                        lower_bound = int(x_val)
                        upper_bound = lower_bound + 1

                        new_A = subproblem['A'] + [[0] * i + [1] + [0] * (len(c) - i - 1)]
                        new_b = subproblem['b'] + [lower_bound]
                        subproblems.append(({'c': c, 'A': new_A, 'b': new_b}, f"{label}_L"))

                        new_A = subproblem['A'] + [[0] * i + [-1] + [0] * (len(c) - i - 1)]
                        new_b = subproblem['b'] + [-upper_bound]
                        subproblems.append(({'c': c, 'A': new_A, 'b': new_b}, f"{label}_U"))
                        break
        else:
            print(f"Subproblema: {label}")
            print("Inviável")

    print("\nSolução ótima:")
    print(f"Função Objetivo: {best_value}")
    print(f"Solução: {best_solution}")

n, m, c, A, b = read('exemp.txt')
BranchAndBound(c, A, b)
