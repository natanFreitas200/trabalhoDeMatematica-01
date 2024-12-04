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
        xmax = []  # Inicializar a lista de soluções
        for i in range(n):
            xmax.append(variaveis[i].solution_value())  # Adicionar valor da variável à lista
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

        # Verificar se a solução é inteira
        inteiro = True
        for valor in solucao_maxima:
            if abs(valor - round(valor)) >= 1e-6:
                inteiro = False
                break

        if inteiro:
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
                valor_atual = solucao_maxima[i]
                if abs(valor_atual - round(valor_atual)) > 1e-6:
                    # Criar subproblema da esquerda
                    A1 = A.copy()  # Copia a matriz A original
                    nova_restricao1 = []
                    for j in range(len(c)):
                        if j == i:
                            nova_restricao1.append(1)  # Se j é o índice atual, adiciona 1
                        else:
                            nova_restricao1.append(0)  # Caso contrário, adiciona 0
                    A1.append(nova_restricao1)  # Adiciona nova restrição à matriz A1
                    b1 = b.copy()  # Copia o vetor b original
                    b1.append(math.floor(valor_atual))  # Adiciona o limite da nova restrição
                    subproblemas.append({"id": f"{id_prob} Esquerda", "c": c, "A": A1, "b": b1})

                    # Criar subproblema da direita
                    A2 = A.copy()  # Copia a matriz A original
                    nova_restricao2 = []
                    for j in range(len(c)):
                        if j == i:
                            nova_restricao2.append(-1)  # Se j é o índice atual, adiciona -1
                        else:
                            nova_restricao2.append(0)  # Caso contrário, adiciona 0
                    A2.append(nova_restricao2)  # Adiciona nova restrição à matriz A2
                    b2 = b.copy()  # Copia o vetor b original
                    b2.append(-math.ceil(valor_atual))  # Adiciona o limite da nova restrição
                    subproblemas.append({"id": f"{id_prob} Direita", "c": c, "A": A2, "b": b2})

                    break  # Divide apenas no primeiro valor fracionário encontrado

    # Print da solução final
    print("\nSolução ótima:")
    print(f"Função Objetivo: {melhor_valor}")
    print(f"Solução: {melhor_solucao}")
    return melhor_valor, melhor_solucao





