
# Trabalho de Matemática — Programação Linear e Branch-and-Bound

Este repositório contém uma implementação em Python de um resolvedor de problemas de Programação Linear (PL) contínua (usando o OR-Tools GLOP) e um método Branch-and-Bound simples para procurar soluções inteiras a partir da relaxação linear.

Principais arquivos
- `script.py` — implementação do solucionador contínuo (`PLSolver`) usando OR-Tools e do algoritmo `Branch_and_Bound` que gera subproblemas, faz poda e imprime o processo.
- `leitura.py` — leitor de arquivo de instância (`LP.txt`) que converte os dados para as estruturas necessárias e chama o Branch-and-Bound.
- `LP.txt` — exemplo de instância no formato esperado (descrito abaixo).

Requisitos
- Python 3.8+ (testado com CPython 3.10+ / 3.12).
- pacotes Python: `ortools` (Google OR-Tools). Também usa apenas a biblioteca padrão (`math`, etc.).

Instalação (Windows / PowerShell)

1. Recomendo criar um ambiente virtual (opcional, mas recomendado):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Atualize o pip e instale dependências:

```powershell
python -m pip install --upgrade pip
python -m pip install ortools
```

Como executar
- Para rodar a leitura do arquivo `LP.txt` e executar o Branch-and-Bound (exemplo):

```powershell
python leitura.py
```

Isso carrega `LP.txt`, resolve a relaxação linear com OR-Tools e aplica o procedimento de Branch-and-Bound, imprimindo subproblemas, podas e a solução final encontrada.

Formato do arquivo de entrada (`LP.txt`)
- Linha 1: dois inteiros separados por espaço — número de variáveis n e número de restrições m
- Linha 2: n coeficientes da função objetivo (c1 c2 ... cn)
- Próximas m linhas: cada linha contém n coeficientes da restrição seguida do lado direito (A_i1 A_i2 ... A_in b_i)

Exemplo (arquivo `LP.txt` do repositório):

```
2 3
3 7
1 0 3.5
5 -4 10
0.5714285714285714 2 9
```

Interpretação do exemplo:
- n = 2 variáveis, m = 3 restrições
- Função objetivo: max 3*x1 + 7*x2
- Restrição 1: 1*x1 + 0*x2 <= 3.5
- Restrição 2: 5*x1 + (-4)*x2 <= 10
- Restrição 3: 0.5714285714285714*x1 + 2*x2 <= 9

Observações e limitações
- O resolvedor contínuo (`PLSolver`) usa o solver GLOP de OR-Tools. Certifique-se de ter `ortools` instalado corretamente.
- O Branch-and-Bound implementado aqui é didático: gera subproblemas pela primeira variável fracionária encontrada e aplica poda por inviabilidade, integrabilidade e optimalidade com tolerância numérica. Não é optimizado para desempenho em grandes instâncias.
- A precisão de integridade é controlada por uma tolerância (1e-6 no código). Em instâncias numéricas, arredondamentos podem afetar o comportamento do branching.

Resolução de problemas comuns
- Erro: "ModuleNotFoundError: No module named 'ortools'" — instale com `python -m pip install ortools` no ambiente apropriado.
- Erro: solver não disponível — verifique a instalação do OR-Tools e a compatibilidade da versão do Python.

Contribuições
- Melhore o parser para aceitar caminhos de arquivos por argumento de linha de comando.
- Adicione testes automatizados e casos de benchmark.
- Otimize a estratégia de branching (por exemplo, escolher a variável com maior frac part ou usar limites heurísticos).


