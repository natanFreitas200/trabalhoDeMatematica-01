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
    # Criação do solver para resolver o problema de programação linear
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    # Verifica se o solver foi criado corretamente
    if not solver:
        print("Erro: Solver não disponível.")
        return None, None

    # Número de variáveis (tamanho do vetor c)
    n = len(c)
    variaveis = []
    
    # Criando as variáveis de decisão xi >= 0 (restrição não negativa)
    for i in range(n):
        variaveis.append(solver.NumVar(0, solver.infinity(), f'x{i+1}'))

    # Definir a função objetivo, que é maximizar a expressão: c1*x1 + c2*x2 + ... + cn*xn
    expressao_objetivo = solver.Sum([c[i] * variaveis[i] for i in range(n)])  # Soma de todas as variáveis com seus coeficientes
    solver.Maximize(expressao_objetivo)  # Maximizar a função objetivo

    # Adicionar as restrições: somatório(Aij * xj) <= bi
    for i in range(len(A)):
        restricao = solver.Sum([A[i][j] * variaveis[j] for j in range(n)])  # Para cada linha de A, cria a expressão para a restrição
        solver.Add(restricao <= b[i])  # Adiciona a restrição ao solver

    # Resolve o problema
    status = solver.Solve()
    
    # Verifica se a solução é ótima
    if status == pywraplp.Solver.OPTIMAL:
        fmax = solver.Objective().Value()  # Valor da função objetivo ótima
        xmax = []
        
        # Armazena os valores das variáveis que otimizam a função objetivo
        for i in range(n):
            xmax.append(variaveis[i].solution_value())
        
        return fmax, xmax  # Retorna o valor ótimo e a solução (valores das variáveis)
    
    # Caso não haja solução ótima, retorna None
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
    # Lista de subproblemas a serem resolvidos, começando com o problema original
    subproblemas = [{"num": "P0", "c": c, "A": A, "b": b}]
    melhor_solucao = None
    melhor_valor = float('-inf')  # Inicializa o melhor valor como infinito negativo
    contador_subproblemas = 1  # Contador para numerar os subproblemas

    # Enquanto houver subproblemas para resolver
    while subproblemas:
        subproblema = subproblemas.pop(0)  # Pega o primeiro subproblema da lista
        num_prob = subproblema["num"]
        c = subproblema["c"]
        A = subproblema["A"]
        b = subproblema["b"]

        # Resolve o subproblema contínuo
        valor_maximo, solucao_maxima = PLSolver(c, A, b)
        
        # Se o subproblema for inviável (não encontrar solução), imprime a poda por inviabilidade e continua
        if valor_maximo is None:
            print(f"Subproblema: {num_prob}")
            print("Poda por Inviabilidade")
            print()
            continue

        # Exibe as informações do subproblema
        print(f"Subproblema: {num_prob}")
        print(f"Função Objetivo: {valor_maximo}")
        print(f"Solução: {solucao_maxima}")
        print()

        # Verifica se a solução encontrada é inteira (não contém valores fracionários)
        inteiro = True
        for valor in solucao_maxima:
            if abs(valor - round(valor)) >= 1e-6:  # Se o valor não for inteiro (diferente de seu arredondado)
                inteiro = False
                break

        # Se a solução for inteira
        if inteiro:
            if valor_maximo > melhor_valor:  # Se for uma melhor solução, armazena a nova melhor solução
                melhor_valor = valor_maximo
                melhor_solucao = []  # Cria uma lista para armazenar a melhor solução
                for x in solucao_maxima:  # Cópia explícita da solução
                    melhor_solucao.append(x)
            print("Poda por Integrabilidade")  # Solução inteira encontrada
            print()
        # Se o valor máximo for menor ou igual ao melhor valor encontrado, poda o subproblema (não gera mais ramificações)
        elif valor_maximo <= melhor_valor:
            print("Poda por Optimalidade")
            print()
        else:
            # Para cada variável, se não for inteira, cria subproblemas (branching)
            for i in range(len(solucao_maxima)):
                valor_atual = solucao_maxima[i]
                if abs(valor_atual - round(valor_atual)) > 1e-6:  # Se a variável não for inteira
                    # Criar subproblema da esquerda (valor fracionário <= inteiro)
                    novo_num_esq = f"P{contador_subproblemas}"
                    contador_subproblemas += 1
                    A1 = []  # Copia a matriz A para o subproblema da esquerda
                    for linha in A:  
                        nova_linha = []
                        for valor in linha:
                            nova_linha.append(valor)
                        A1.append(nova_linha)
                    nova_restricao1 = []  # Cria a nova restrição
                    for j in range(len(c)):
                        if j == i:
                            nova_restricao1.append(1)  # Restrição para o subproblema da esquerda
                        else:
                            nova_restricao1.append(0)
                    A1.append(nova_restricao1)
                    b1 = []  # Cópia do vetor b para o subproblema da esquerda
                    for valor in b:
                        b1.append(valor)
                    b1.append(math.floor(valor_atual))  # Ajuste para o valor fracionário da variável
                    subproblemas.append({"num": novo_num_esq, "c": c, "A": A1, "b": b1})

                    # Criar subproblema da direita (valor fracionário >= inteiro)
                    novo_num_dir = f"P{contador_subproblemas}"
                    contador_subproblemas += 1
                    A2 = []  # Copia a matriz A para o subproblema da direita
                    for linha in A:
                        nova_linha = []
                        for valor in linha:
                            nova_linha.append(valor)
                        A2.append(nova_linha)
                    nova_restricao2 = []  # Cria a nova restrição
                    for j in range(len(c)):
                        if j == i:
                            nova_restricao2.append(-1)  # Restrição para o subproblema da direita
                        else:
                            nova_restricao2.append(0)
                    A2.append(nova_restricao2)
                    b2 = []  # Cópia do vetor b para o subproblema da direita
                    for valor in b:
                        b2.append(valor)
                    b2.append(-math.ceil(valor_atual))  # Ajuste para o valor fracionário da variável
                    subproblemas.append({"num": novo_num_dir, "c": c, "A": A2, "b": b2})

                    break  # Divide apenas no primeiro valor fracionário encontrado

    # Imprime a solução ótima encontrada
    print("Solução ótima:")
    print(f"Função Objetivo: {melhor_valor}")
    print(f"Solução: {melhor_solucao}")
    return melhor_valor, melhor_solucao