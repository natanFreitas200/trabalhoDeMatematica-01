from ortools.linear_solver import pywraplp
import math


def verif_inteiro(solucao):
    """
    Verifica se todos os valores da solução são inteiros.

    Parâmetros:
        solucao (list): Vetor solução.

    Retorna:
        bool: True se todos os valores forem inteiros, False caso contrário.
    """
    return all(abs(valor - round(valor)) < 1e-6 for valor in solucao)


# Função para resolver problemas de programação linear contínua (PL)
def PLSolver(c, A, b):
    """
    Resolve um problema de programação linear contínua (PL).

    Parâmetros:
        c (list): Coeficientes da função objetivo.
        A (list): Matriz das restrições.
        b (list): Vetor dos limites das restrições.

    Retorna:
        tuple: (fmax, xmax), onde fmax é o valor ótimo da função objetivo
               e xmax é o vetor solução que maximiza a função objetivo.
    """
    # Criação do solver (GLOP - Google Linear Optimization Package)
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Erro: Solver não disponível.")
        return None, None

    # Criar as variáveis de decisão: xi >= 0
    n = len(c)  # Número de variáveis
    variaveis = [solver.NumVar(0, solver.infinity(), f'x{i+1}') for i in range(n)]

    # Definir a função objetivo: max c1*x1 + c2*x2 + ... + cn*xn
    solver.Maximize(solver.Sum(c[i] * variaveis[i] for i in range(n)))

    # Adicionar as restrições: somatório(Aij * xj) <= bi
    for i in range(len(A)):
        solver.Add(solver.Sum(A[i][j] * variaveis[j] for j in range(n)) <= b[i])

    # Resolver o problema
    status = solver.Solve()

    # Verificar se a solução é ótima e retornar resultados
    if status == pywraplp.Solver.OPTIMAL:
        fmax = solver.Objective().Value()  # Valor da função objetivo
        xmax = [variaveis[i].solution_value() for i in range(n)]  # Solução encontrada
        return fmax, xmax
    else:
        # Retornar None caso a solução não seja encontrada
        return None, None


# Função para resolver problemas de programação inteira usando Branch-and-Bound
def branch_and_bound(c, A, b):
    """
    Implementa o método Branch-and-Bound para encontrar soluções inteiras.

    Parâmetros:
        c (list): Coeficientes da função objetivo.
        A (list): Matriz das restrições.
        b (list): Vetor dos limites das restrições.

    Retorna:
        tuple: (fmax, xmax), onde fmax é o valor ótimo da função objetivo
               e xmax é a solução inteira que maximiza a função.
    """
    # Lista de subproblemas para explorar, iniciando com o problema original
    subproblemas = [{"id": "P0", "c": c, "A": A, "b": b}]
    melhor_solucao = None  # Melhor solução inteira encontrada
    melhor_valor = float('-inf')  # Melhor valor da função objetivo

    while subproblemas:
        # Pegar o próximo subproblema
        subproblema = subproblemas.pop(0)
        id_prob, c, A, b = subproblema["id"], subproblema["c"], subproblema["A"], subproblema["b"]

        # Resolver o subproblema contínuo
        valor_maximo, solucao_maxima = PLSolver(c, A, b)
        if valor_maximo is None:
            # Subproblema inviável
            print(f"{id_prob}: inviável (Poda por Inviabilidade)")
            continue

        # Print das informações do subproblema
        print(f"Subproblema: {id_prob}")
        print(f"Função Objetivo: {valor_maximo}")
        print(f"Solução: {solucao_maxima}")

        if verif_inteiro(solucao_maxima):
            # Se a solução é inteira, verificar se é melhor que a solução atual
            if valor_maximo > melhor_valor:
                melhor_valor = valor_maximo
                melhor_solucao = solucao_maxima
                print(f"{id_prob}: Inteiro (Poda por Integrabilidade)")
        elif valor_maximo <= melhor_valor:
            # Poda por Optimalidade
            print(f"{id_prob}: Poda por Optimalidade")
        else:
            # Divisão (branching) para gerar novos subproblemas
            for i in range(len(solucao_maxima)):
                if abs(solucao_maxima[i] - round(solucao_maxima[i])) > 1e-6:
                    # Criar dois subproblemas: xi <= floor(xi) e xi >= ceil(xi)
                    A1 = A + [[1 if j == i else 0 for j in range(len(c))]]
                    b1 = b + [math.floor(solucao_maxima[i])]
                    subproblemas.append({"id": f"{id_prob}L", "c": c, "A": A1, "b": b1})

                    A2 = A + [[-1 if j == i else 0 for j in range(len(c))]]
                    b2 = b + [-math.ceil(solucao_maxima[i])]
                    subproblemas.append({"id": f"{id_prob}R", "c": c, "A": A2, "b": b2})
                    break  # Divide apenas no primeiro valor fracionário encontrado

    # Print da solução final
    print("\nSolução ótima:")
    print(f"Função Objetivo: {melhor_valor}")
    print(f"Solução: {melhor_solucao}")
    return melhor_valor, melhor_solucao


# Função para ler os dados de um arquivo e resolver o problema
def ler(arqu):
    """
    Lê os dados do arquivo de entrada e resolve o problema utilizando Branch-and-Bound.

    Parâmetros:
        arqu (str): Caminho do arquivo de entrada.
    """
    with open(arqu, 'r') as arquivo:
        linhas = arquivo.readlines()

    # Ler o número de variáveis (n) e restrições (m)
    n, m = map(int, linhas[0].split())

    # Ler os coeficientes da função objetivo
    c = list(map(float, linhas[1].split()))

    # Ler as restrições (matriz A e vetor b)
    A = []
    b = []
    for i in range(2, 2 + m):
        *a, bi = map(float, linhas[i].split())
        A.append(a)
        b.append(bi)

    # Resolver o problema usando Branch-and-Bound
    valor_maximo, solucao_maxima = branch_and_bound(c, A, b)

    # Imprimir a solução final
    print("\nSolução final:")
    print(f"Função Objetivo: {valor_maximo}")
    print(f"Solução: {solucao_maxima}")


# Chamada principal para resolver o problema a partir do arquivo LP.txt
ler("LP.txt")
