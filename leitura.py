from script import PLSolver, branch_and_bound


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
        *a, value = map(float, linhas[i].split())
        A.append(a)
        b.append(value)

    # Resolver o problema usando Branch-and-Bound
    valor_maximo, solucao_maxima = branch_and_bound(c, A, b)

    # Imprimir a solução final
    print("\nSolução final:")
    print(f"Função Objetivo: {valor_maximo}")
    print(f"Solução: {solucao_maxima}")


# Chamada principal para resolver o problema a partir do arquivo LP.txt
ler("LP.txt")