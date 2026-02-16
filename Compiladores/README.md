# Analisador Sintático Preditivo

Implementação de um analisador sintático preditivo (parser LL(1)) para uma linguagem de programação imperativa, desenvolvido como projeto da disciplina de Compiladores.

---

## Visão Geral

Este projeto implementa um analisador sintático preditivo baseado em tabela para análise de programas escritos em uma linguagem imperativa simplificada. O analisador utiliza a abordagem top-down (descendente) com lookahead de um token (LL(1)).

### Características Principais

- Análise sintática preditiva manual (sem uso de geradores como YACC/Bison)
- Construção de árvore sintática concreta (árvore de derivação)
- Estrutura de dados encadeada para representação da árvore
- Mensagens de erro sintático detalhadas com linha e coluna
- Suporte completo à gramática LL(1) fornecida

---

## Requisitos do Projeto

O projeto atende aos seguintes requisitos especificados:

### 1. Implementação Manual de Analisador Sintático Preditivo

- Utiliza abordagem baseada em tabela preditiva M[A, a]
- Implementação do algoritmo clássico de análise preditiva
- Sem uso de bibliotecas externas de parsing

### 2. Construção de Árvore Sintática Concreta

- Estrutura encadeada para representação da árvore
- Cada nó contém símbolo gramatical e lista de filhos
- Preserva todas as derivações (incluindo produções vazias)

### 3. Mensagens de Erro Úteis

- Indicação de linha e coluna do erro
- Token encontrado vs. token(s) esperado(s)
- Formatação clara e legível

---

## Estrutura do Projeto

```
projeto/
├── analisador_lexico.py       # Analisador léxico (fornecido)
├── analisador_sintatico.py    # Analisador sintático (implementado)
├── main.py                     # Programa principal
├── teste_completo.txt          # Arquivo de teste completo
├── exemplo1_declaracoes.txt    # Testes individuais
├── exemplo2_inicializacao.txt
├── ...
└── README.md                   # Esta documentação
```

### Descrição dos Arquivos

**analisador_lexico.py**
- Analisador léxico previamente implementado
- Gera tokens a partir do código fonte
- Mantém tabela de símbolos

**analisador_sintatico.py**
- Classe `NoArvore`: Estrutura para nós da árvore sintática
- Classe `AnalisadorSintatico`: Implementação do parser preditivo
- Tabela preditiva completa da gramática

**main.py**
- Interface de linha de comando
- Integração léxico + sintático
- Exibição da árvore sintática

---

## Instalação e Uso

### Requisitos

- Python 3.7 ou superior
- Nenhuma biblioteca externa necessária (usa apenas biblioteca padrão)

### Execução

```bash
python main.py arquivo.txt
```

Onde `arquivo.txt` contém o código fonte a ser analisado.

### Exemplo de Execução

```bash
python main.py exemplo1_declaracoes.txt
```

### Saída Esperada

```
======================================================================
CÓDIGO FONTE
======================================================================
main {
    int x;
    float y := 10.5;
}
======================================================================

Iniciando Análise Léxica...
Iniciando Análise Sintática...

======================================================================
ÁRVORE SINTÁTICA
======================================================================

<programa>
├─ MAIN
├─ ABRE_CHAVES
├─ <bloco>
│  ├─ <comando>
│  │  └─ <declaracao>
│  │     ├─ <tipo>
│  │     │  └─ INT
│  │     └─ <lista_declaracao>
│  │        └─ <declaracao_simples>
│  │           └─ ID: x
│  └─ <bloco>
│     └─ <comando>
│        └─ <declaracao>
│           ├─ <tipo>
│           │  └─ FLOAT
│           └─ <lista_declaracao>
│              └─ <declaracao_simples>
│                 ├─ ID: y
│                 └─ ASSIGN
│                    └─ <expressao>
│                       └─ NUM: 10.5
└─ FECHA_CHAVES

======================================================================
COMPILAÇÃO CONCLUÍDA COM SUCESSO!
======================================================================
```

---

## Gramática da Linguagem

A linguagem suporta as seguintes construções:

### Programa

Todo programa começa com `main` seguido de um bloco delimitado por chaves.

```
<programa> → MAIN ABRE_CHAVES <bloco> FECHA_CHAVES
```

### Tipos de Dados

- `int` - Inteiros
- `float` - Ponto flutuante
- `char` - Caractere
- `void` - Vazio

### Declarações

```c
int x;                    // Declaração simples
float y := 10.5;          // Declaração com inicialização
int vetor[10];            // Declaração de array
int a, b, c;              // Múltiplas declarações
```

### Atribuições

```c
x := 10;                  // Atribuição simples
vetor[0] := 100;          // Atribuição em array
resultado := a + b * c;   // Atribuição com expressão
```

### Estruturas de Controle

**IF-THEN-ELSE:**
```c
if (x > 5) then {
    x := x + 1;
} else {
    x := x - 1;
}
```

**IF-ELSIF-ELSE:**
```c
if (nota >= 90) then {
    conceito := 'A';
} elsif (nota >= 80) then {
    conceito := 'B';
} else {
    conceito := 'C';
}
```

**WHILE:**
```c
while (i < 10) do {
    i := i + 1;
}
```

**FOR:**
```c
for (i := 0; i < 10; i := i + 1) do {
    soma := soma + i;
}
```

### Expressões

**Operadores Aritméticos:**
- `+` Adição
- `-` Subtração
- `*` Multiplicação
- `/` Divisão
- `**` Potenciação

**Operadores Relacionais:**
- `==` Igualdade
- `!=` Diferença
- `<` Menor que
- `>` Maior que
- `<=` Menor ou igual
- `>=` Maior ou igual

**Precedência (do mais alto para o mais baixo):**
1. `**` (associativo à direita)
2. `*`, `/`
3. `+`, `-`
4. Operadores relacionais

**Parênteses:**
```c
resultado := (a + b) * (c - d);
```

### Comentários

```c
{% Comentário de bloco %}
```

---

## Implementação

### Algoritmo Preditivo

O analisador segue o algoritmo clássico de análise sintática preditiva:

```
Início Algoritmo
    inicializa_pilha(P)
    empilha(P, <programa>)
    proxToken ← lex()
    
    enquanto (P não vazia) faça
        X ← topo(P)
        
        se (X é terminal) então
            se (X = proxToken) então
                desempilha(P)
                proxToken ← lex()
            senão
                Erro()
        senão
            se (Tab[X, proxToken] = ∅) então
                Erro()
            senão
                desempilha(P)
                empilha(P, símbolos da produção em ordem reversa)
    
    se (proxToken ≠ EOF) então
        Erro()
    senão
        Aceita
Fim
```

### Estrutura de Dados

**Classe NoArvore:**
```python
class NoArvore:
    def __init__(self, simbolo, token=None):
        self.simbolo = simbolo      # '<programa>', 'MAIN', 'ID', etc.
        self.token = token          # Token original (se terminal)
        self.filhos = []            # Lista de nós filhos
```

**Classe AnalisadorSintatico:**
```python
class AnalisadorSintatico:
    def __init__(self, lexer, tabela_preditiva):
        self.lexer = lexer                  # Analisador léxico
        self.tabela = tabela_preditiva      # Tabela M[A, a]
        self.pilha = []                     # Pilha de símbolos
        self.prox_token = None              # Lookahead
        self.arvore_raiz = None             # Raiz da árvore
        self.pilha_nos = []                 # Pilha auxiliar da árvore
```

### Tabela Preditiva

A tabela preditiva M[A, a] é implementada como um dicionário Python:

```python
tabela_preditiva = {
    ('<programa>', 'MAIN'): ['MAIN', 'ABRE_CHAVES', '<bloco>', 'FECHA_CHAVES'],
    ('<bloco>', 'INT'): ['<comando>', '<bloco>'],
    ('<bloco>', 'FECHA_CHAVES'): ['ε'],
    # ... mais entradas
}
```

**Formato:**
- Chave: `(não-terminal, terminal)`
- Valor: Lista de símbolos da produção

**Produções Vazias:**
- Representadas por `['ε']`
- Acionadas quando lookahead está no FOLLOW do não-terminal

### Construção da Árvore

A árvore é construída simultaneamente à análise:

1. Ao empilhar uma produção, cria-se nós filhos para cada símbolo
2. Ao casar um terminal, adiciona-se o token como folha
3. Produções vazias (ε) não geram nós na árvore

**Exemplo de derivação:**

Para o código `int x;`, a árvore gerada é:

```
<declaracao>
├─ <tipo>
│  └─ INT
├─ <lista_declaracao>
│  ├─ <declaracao_simples>
│  │  ├─ ID (x)
│  │  └─ <declaracao_simples_rest> (ε)
│  └─ <lista_declaracao_rest> (ε)
└─ PONTO_VIRGULA
```

---

## Exemplos de Uso

### Exemplo 1: Declarações Simples

**Entrada (exemplo1_declaracoes.txt):**
```c
main {
    int x;
    float y;
    char letra;
}
```

**Execução:**
```bash
python main.py exemplo1_declaracoes.txt
```

**Resultado:** Árvore sintática completa exibida, análise bem-sucedida.

### Exemplo 2: Estrutura IF-ELSE

**Entrada (exemplo3_if_else.txt):**
```c
main {
    int idade := 25;
    
    if (idade >= 18) then {
        int adulto := 1;
    } else {
        int menor := 1;
    }
}
```

**Execução:**
```bash
python main.py exemplo3_if_else.txt
```

**Resultado:** Análise reconhece corretamente a estrutura condicional.

### Exemplo 3: Loop FOR

**Entrada (exemplo6_for.txt):**
```c
main {
    int i;
    int soma := 0;
    
    for (i := 1; i <= 10; i := i + 1) do {
        soma := soma + i;
    }
}
```

**Execução:**
```bash
python main.py exemplo6_for.txt
```

**Resultado:** Estrutura de repetição corretamente analisada.

---

## Tratamento de Erros

O analisador detecta e reporta erros sintáticos com informações detalhadas.

### Tipos de Erros Detectados

**1. Terminal não casa com lookahead:**
```
Esperado 'PONTO_VIRGULA', mas encontrado 'ID'
```

**2. Não existe produção na tabela:**
```
Esperado um dos seguintes: 'VOID', 'INT', 'CHAR', 'FLOAT',
mas encontrado 'ID'
```

**3. Entrada não consumida completamente:**
```
Entrada não foi completamente consumida. Token inesperado: 'FECHA_CHAVES'
```

### Formato das Mensagens de Erro

```
======================================================================
ERRO SINTÁTICO na Linha 3, Coluna 10
======================================================================
Token encontrado: <ID, x> (L:3, C:10)
Mensagem: Esperado 'PONTO_VIRGULA', mas encontrado 'ID'
======================================================================
```

**Informações incluídas:**
- Linha e coluna exatas do erro
- Token problemático (tipo e valor)
- Token(s) esperado(s) naquele contexto
- Formatação clara e destacada

### Exemplo de Código com Erro

**Entrada (erro1_falta_ponto_virgula.txt):**
```c
main {
    int x := 10
    int y := 20;
}
```

**Saída:**
```
======================================================================
ERRO SINTÁTICO na Linha 3, Coluna 5
======================================================================
Token encontrado: <INT, > (L:3, C:5)
Mensagem: Esperado 'PONTO_VIRGULA', mas encontrado 'INT'
======================================================================
```

**Explicação:** O analisador detectou que após a expressão `10` deveria haver um ponto-e-vírgula, mas encontrou `int` (início de nova declaração).

---

## Testes

O projeto inclui uma suíte completa de testes.

### Arquivos de Teste Fornecidos

**Testes Bem-Sucedidos (sintaxe correta):**

| Arquivo | Descrição |
|---------|-----------|
| `teste_completo.txt` | Teste abrangente com todas as funcionalidades |
| `exemplo1_declaracoes.txt` | Declarações simples |
| `exemplo2_inicializacao.txt` | Declarações com inicialização |
| `exemplo3_if_else.txt` | Estrutura IF-ELSE |
| `exemplo4_elsif.txt` | Estrutura IF-ELSIF-ELSE |
| `exemplo5_while.txt` | Loop WHILE |
| `exemplo6_for.txt` | Loop FOR |
| `exemplo7_expressoes.txt` | Expressões aritméticas complexas |
| `exemplo8_arrays.txt` | Declaração e uso de arrays |
| `exemplo9_completo.txt` | Programa completo com comentários |
| `exemplo10_aninhado.txt` | Estruturas aninhadas |

**Testes de Erro (sintaxe incorreta):**

| Arquivo | Erro Esperado |
|---------|---------------|
| `erro1_falta_ponto_virgula.txt` | Falta `;` após declaração |
| `erro2_falta_then.txt` | Falta `then` no IF |
| `erro3_falta_do.txt` | Falta `do` no WHILE |
| `erro4_parenteses.txt` | Parênteses não fechado |

### Executando os Testes

**Teste individual:**
```bash
python main.py exemplo1_declaracoes.txt
```

**Teste completo:**
```bash
python main.py teste_completo.txt
```

**Teste de detecção de erro:**
```bash
python main.py erro1_falta_ponto_virgula.txt
```

### Teste Completo

O arquivo `teste_completo.txt` é um teste abrangente que exercita:

- Todos os tipos de dados (int, float, char, void)
- Declarações simples e com inicialização
- Arrays com indexação
- Todas as operações aritméticas (+, -, *, /, **)
- Todos os operadores relacionais (==, !=, <, >, <=, >=)
- Estruturas condicionais (if, elsif, else)
- Estruturas de repetição (while, for)
- Estruturas aninhadas (3 níveis)
- Precedência e associatividade de operadores
- Comentários
- Produções vazias (ε)

**Executar:**
```bash
python main.py teste_completo.txt
```

**Resultado esperado:** Análise bem-sucedida com árvore sintática de aproximadamente 1000 linhas.

---

## Limitações Conhecidas

### Limitações da Gramática

1. **Múltiplas declarações com inicialização:**
   - Permitido: `int a, b, c;` (sem inicialização)
   - Permitido: `int a := 1;` (uma variável)
   - **Não permitido:** `int a := 1, b := 2;` (vírgula após expressão)

2. **Bloco de comando:**
   - IF/WHILE/FOR podem ter bloco `{}` ou comando único
   - Comando único não pode ser outra estrutura de controle sem chaves

### Limitações da Implementação

1. **Tamanho da árvore:**
   - Árvore concreta pode ficar muito grande para programas complexos
   - Todas as derivações são preservadas (incluindo produções vazias)

2. **Performance:**
   - Não otimizada para programas muito grandes
   - Adequada para fins didáticos e exemplos de tamanho médio

3. **Mensagens de erro:**
   - Mostra apenas o primeiro erro encontrado
   - Não realiza recuperação de erros (modo pânico)

---

## Conceitos Teóricos

### Análise Preditiva (LL(1))

**LL(1)** significa:
- **L** (Left-to-right): Leitura da esquerda para direita
- **L** (Leftmost derivation): Derivação mais à esquerda
- **1**: Um token de lookahead

**Características:**
- Top-down (descendente): Constrói árvore da raiz para as folhas
- Determinística: Cada passo é único, sem backtracking
- Baseada em tabela: Consulta M[A, a] para decidir produção

### Conjuntos FIRST e FOLLOW

**FIRST(α):** Conjunto de terminais que podem iniciar strings derivadas de α.

**FOLLOW(A):** Conjunto de terminais que podem aparecer imediatamente após A.

**Uso:** Determinar entradas da tabela preditiva:
- `M[A, a] = A → α` se `a ∈ FIRST(α)`
- `M[A, a] = A → α` se `ε ∈ FIRST(α)` e `a ∈ FOLLOW(A)`

### Árvore Sintática Concreta vs. Abstrata

**Concreta (implementada neste projeto):**
- Mostra TODAS as derivações da gramática
- Inclui produções vazias (ε)
- Preserva estrutura completa da gramática
- Útil para debugging e validação

**Abstrata (AST - usada em fases posteriores):**
- Mostra apenas informações essenciais
- Remove produções auxiliares
- Estrutura otimizada para análise semântica
- Árvore muito menor e mais eficiente

**Exemplo:**

Para `x := 5`, a árvore **concreta** é:
```
<atribuicao>
├─ ID (x)
└─ <atribuicao_rest>
   ├─ ASSIGN
   ├─ <expressao>
   │  ├─ <termo>
   │  │  ├─ <potencia>
   │  │  │  ├─ <fator>
   │  │  │  │  └─ NUM (5)
   │  │  │  └─ <potencia_rest> (ε)
   │  │  └─ <termo_rest> (ε)
   │  └─ <expressao_rest> (ε)
   └─ PONTO_VIRGULA
```

A árvore **abstrata** seria simplesmente:
```
:=
├─ x
└─ 5
```

---
