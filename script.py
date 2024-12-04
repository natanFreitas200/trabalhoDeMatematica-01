from ortools.linear_solver import pywraplp
import math


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
    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        print("Erro: Solver não disponível.")
        return None, None

    n = len(c)
    variaveis = []
    for i in range(n):
        variaveis.append(solver.NumVar(0, solver.infinity(), f'x{i+1}'))

    solver.Maximize(solver.Sum(c[i] * variaveis[i] for i in range(n)))

    for i in range(len(A)):
        restricao = solver.Sum(A[i][j] * variaveis[j] for j in range(n))
        solver.Add(restricao <= b[i])

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        fmax = solver.Objective().Value()
        xmax = []
        for i in range(n):
            xmax.append(variaveis[i].solution_value())
        return fmax, xmax
    return None, None


# Função para resolver problemas de programação inteira usando Branch-and-Bound
def Branch_and_Bound(c, A, b):
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
    subproblemas = [{"id": "P0", "c": c, "A": A, "b": b}]
    melhor_solucao = None
    melhor_valor = float('-inf')
    contador_subproblemas = 1

    while subproblemas:
        subproblema = subproblemas.pop(0)
        id_prob, c, A, b = subproblema["id"], subproblema["c"], subproblema["A"], subproblema["b"]

        valor_maximo, solucao_maxima = PLSolver(c, A, b)
        if valor_maximo is None:
            print(f"Subproblema: {id_prob}")
            print("Poda por Inviabilidade")
            print()
            continue

        print(f"Subproblema: {id_prob}")
        print(f"Função Objetivo: {valor_maximo}")
        print(f"Solução: {solucao_maxima}")
        print()

        inteiro = True
        for valor in solucao_maxima:
            if abs(valor - round(valor)) >= 1e-6:
                inteiro = False
                break

        if inteiro:
            if valor_maximo > melhor_valor:
                melhor_valor = valor_maximo
                melhor_solucao = solucao_maxima
            print("Poda por Integrabilidade")
            print()
        elif valor_maximo <= melhor_valor:
            print("Poda por Optimalidade")
        else:
            for i in range(len(solucao_maxima)):
                valor_atual = solucao_maxima[i]
                if abs(valor_atual - round(valor_atual)) > 1e-6:
                    # Criar subproblema da esquerda
                    nova_id_esq = f"P{contador_subproblemas}"
                    contador_subproblemas += 1
                    A1 = []
                    for linha in A:
                        A1.append(linha[:])  # Copiar cada linha da matriz
                    nova_restricao1 = []
                    for j in range(len(c)):
                        if j == i:
                            nova_restricao1.append(1)
                        else:
                            nova_restricao1.append(0)
                    A1.append(nova_restricao1)
                    b1 = b[:]
                    b1.append(math.floor(valor_atual))
                    subproblemas.append({"id": nova_id_esq, "c": c, "A": A1, "b": b1})

                    # Criar subproblema da direita
                    nova_id_dir = f"P{contador_subproblemas}"
                    contador_subproblemas += 1
                    A2 = []
                    for linha in A:
                        A2.append(linha[:])  # Copiar cada linha da matriz
                    nova_restricao2 = []
                    for j in range(len(c)):
                        if j == i:
                            nova_restricao2.append(-1)
                        else:
                            nova_restricao2.append(0)
                    A2.append(nova_restricao2)
                    b2 = b[:]
                    b2.append(-math.ceil(valor_atual))
                    subproblemas.append({"id": nova_id_dir, "c": c, "A": A2, "b": b2})

                    break  # Divide apenas no primeiro valor fracionário encontrado

    print("Solução ótima:")
    print(f"Função Objetivo: {melhor_valor}")
    print(f"Solução: {melhor_solucao}")
    return melhor_valor, melhor_solucao
