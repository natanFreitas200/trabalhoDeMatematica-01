from ortools.linear_solver import pywraplp
import math

def read_input(file_path):
    """
    Lê o arquivo de entrada e extrai os parâmetros c, A e b.
    
    Parâmetros:
        file_path (str): Caminho para o arquivo de entrada
        
    Retorna:
        c (list): Coeficientes da função objetivo
        A (list of lists): Matriz de coeficientes das restrições
        b (list): Vetor dos termos independentes das restrições
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Primeira linha: número de variáveis e número de restrições
    n, m = map(int, lines[0].split())

    # Segunda linha: vetor c
    c = list(map(int, lines[1].split()))

    # Próximas m linhas: matriz A e vetor b
    A = []
    b = []
    for i in range(m):
        *row, bi = map(int, lines[2 + i].split())
        A.append(row)
        b.append(bi)
    
    return c, A, b

def PLSolver(c, A, b):
    """
    Resolve o problema de programação linear relaxado:
    max c^T * x
    sujeito a Ax <= b, x >= 0
    
    Parâmetros:
        c (list): Coeficientes da função objetivo
        A (list of lists): Matriz de coeficientes das restrições
        b (list): Vetor dos termos independentes das restrições
    
    Retorna:
        fmax (float): Valor ótimo da função objetivo
        xmax (list): Solução ótima
    """
    # Criando o solver
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None, None

    # Criando as variáveis
    n = len(c)
    x = [solver.NumVar(0, solver.infinity(), f'x{i+1}') for i in range(n)]

    # Adicionando a função objetivo
    solver.Maximize(solver.Sum(c[i] * x[i] for i in range(n)))

    # Adicionando as restrições
    for i in range(len(A)):
        solver.Add(solver.Sum(A[i][j] * x[j] for j in range(n)) <= b[i])

    # Resolver o problema
    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        fmax = solver.Objective().Value()  # Valor ótimo da função objetivo
        xmax = [var.solution_value() for var in x]  # Solução ótima
        return fmax, xmax
    else:
        return None, None

def BranchAndBound(c, A, b):
    """
    Implementa o método Branch-and-Bound para resolver o problema inteiro:
    max c^T * x
    sujeito a Ax <= b, x >= 0 e x ∈ Z^n
    
    Parâmetros:
        c, A, b: Igual à função PLSolver
        
    Retorna:
        fmax_final (float): Valor ótimo da função objetivo
        xmax_final (list): Solução inteira ótima
    """
    subproblems = [(c, A, b)]  # Lista de subproblemas, começando pelo problema original
    best_solution = None
    best_value = -math.inf
    problem_counter = 0  # Contador para nomear os subproblemas

    while subproblems:
        # Identifica o subproblema
        problem_counter += 1
        subproblem_name = f"P{problem_counter}"
        current_c, current_A, current_b = subproblems.pop(0)

        # Resolve o subproblema
        fmax, xmax = PLSolver(current_c, current_A, current_b)
        
        # Imprime informações do subproblema
        print(f"\nSubproblema: {subproblem_name}")
        if fmax is None:
            print("Função Objetivo: Inviável")
            print("Poda por Inviabilidade")
            continue
        
        print(f"Função Objetivo: {fmax}")
        print(f"Solução: {xmax}")
        
        # Verifica se a solução é inteira
        if all(math.isclose(x, round(x)) for x in xmax):
            if fmax > best_value:
                best_value = fmax
                best_solution = xmax
            print("Poda por Integrabilidade")
        else:
            # Divide o problema em dois subproblemas
            for i, x in enumerate(xmax):
                if not math.isclose(x, round(x)):
                    # Cria subproblemas com cortes para x <= floor(x) e x >= ceil(x)
                    floor_constraint = (
                        current_A + [[0] * i + [1] + [0] * (len(xmax) - i - 1)],
                        current_b + [math.floor(x)]
                    )
                    ceil_constraint = (
                        current_A + [[0] * i + [-1] + [0] * (len(xmax) - i - 1)],
                        current_b + [-math.ceil(x)]
                    )
                    subproblems.append((current_c, *floor_constraint))
                    subproblems.append((current_c, *ceil_constraint))
                    print("Poda por Optimalidade")
                    break  # Divide em uma variável por vez

    # Resultado final
    print("\nSolução ótima")
    print(f"Função Objetivo: {best_value}")
    print(f"Solução: {best_solution}")
    return best_value, best_solution

# Leitura dos dados do arquivo
file_path = 'exemp.txt'  # Substitua pelo caminho correto do seu arquivo
c, A, b = read_input(file_path)

# Executa Branch-and-Bound
fmax, xmax = BranchAndBound(c, A, b)
