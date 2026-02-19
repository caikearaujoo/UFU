"""
Analisador Sintático Preditivo
Implementação baseada em tabela preditiva para análise LL(1)
Constrói árvore sintática concreta (árvore de derivação)
"""

# ==============================================================================
# CLASSE: Nó da Árvore Sintática
# ==============================================================================
class NoArvore:
    """
    Representa um nó na árvore sintática concreta.
    Pode ser um nó não-terminal (com filhos) ou terminal (folha).
    """
    def __init__(self, simbolo, token=None):
        self.simbolo = simbolo      # Nome do símbolo (ex: '<programa>', 'MAIN', 'ID')
        self.token = token          # Token associado (apenas para terminais)
        self.filhos = []            # Lista de nós filhos
    
    def adicionar_filho(self, filho):
        """Adiciona um filho ao nó"""
        self.filhos.append(filho)
    
    def eh_terminal(self):
        """Verifica se o nó é terminal (não começa com '<')"""
        return not self.simbolo.startswith('<')
    
    def __str__(self):
        """Representação em string do nó"""
        if self.token:
            return f"{self.simbolo} {self.token}"
        return self.simbolo
    
    def imprimir_arvore(self, nivel=0, prefixo=""):
        """Imprime a árvore de forma hierárquica"""
        indent = "  " * nivel
        
        # Imprime o nó atual
        if self.eh_terminal() and self.token:
            print(f"{indent}{prefixo}{self.simbolo}: {self.token}")
        else:
            print(f"{indent}{prefixo}{self.simbolo}")
        
        # Imprime os filhos
        for i, filho in enumerate(self.filhos):
            if i == len(self.filhos) - 1:
                filho.imprimir_arvore(nivel + 1, "└─ ")
            else:
                filho.imprimir_arvore(nivel + 1, "├─ ")


# ==============================================================================
# CLASSE: Analisador Sintático Preditivo
# ==============================================================================
class AnalisadorSintatico:
    """
    Analisador sintático preditivo baseado em tabela.
    Implementa o algoritmo de análise descendente LL(1).
    """
    
    def __init__(self, lexer, tabela_preditiva):
        """
        Inicializa o analisador sintático.
        
        Args:
            lexer: Analisador léxico (objeto AnalisadorLexico)
            tabela_preditiva: Dicionário com a tabela preditiva
        """
        self.lexer = lexer
        self.tabela = tabela_preditiva
        self.pilha = []
        self.prox_token = None
        self.arvore_raiz = None
        self.pilha_nos = []  # Pilha auxiliar para construção da árvore
        
        # Armazena linhas do código fonte para exibir em erros
        self.linhas_codigo = lexer.codigo.split('\n')
    
    def empilha(self, simbolo):
        """Empilha um símbolo na pilha de análise"""
        self.pilha.append(simbolo)
    
    def desempilha(self):
        """Desempilha e retorna o topo da pilha"""
        if self.pilha:
            return self.pilha.pop()
        return None
    
    def topo(self):
        """Retorna o topo da pilha sem desempilhar"""
        if self.pilha:
            return self.pilha[-1]
        return None
    
    def pilha_vazia(self):
        """Verifica se a pilha está vazia"""
        return len(self.pilha) == 0
    
    def eh_terminal(self, simbolo):
        """Verifica se um símbolo é terminal (não começa com '<')"""
        return not simbolo.startswith('<')
    
    def obter_tipo_token(self, token):
        """Obtém o tipo do token atual"""
        if token is None:
            return '$'
        
        # Para RELOP, usamos o atributo específico
        if token.tipo == 'RELOP':
            return token.atributo  # Retorna: EQEQ, NE, LT, GT, LE, GE
        
        return token.tipo
    
    def erro_sintatico(self, mensagem, token=None):
        """
        Gera uma mensagem de erro sintático útil e aborta a análise.
        
        Args:
            mensagem: Descrição do erro
            token: Token onde o erro ocorreu (opcional)
        """
        if token:
            print(f"\n{'='*70}")
            print(f"ERRO SINTÁTICO na Linha {token.linha}, Coluna {token.coluna}")
            print(f"{'='*70}")
            
            # Mostra a linha do código onde ocorreu o erro
            if 1 <= token.linha <= len(self.linhas_codigo):
                linha_codigo = self.linhas_codigo[token.linha - 1]
                print(f"\n{token.linha:4} | {linha_codigo}")
                
                # Cria indicador visual da coluna (seta apontando para o erro)
                espacos = ' ' * (7 + token.coluna - 1)  # 7 = len("    | ")
                print(f"{espacos}^")
                print(f"{espacos}|")
                print(f"{espacos}Erro aqui\n")
            
            print(f"Token encontrado: {token}")
            print(f"Mensagem: {mensagem}")
            print(f"{'='*70}\n")
        else:
            print(f"\n{'='*70}")
            print(f"ERRO SINTÁTICO")
            print(f"{'='*70}")
            print(f"Mensagem: {mensagem}")
            print(f"{'='*70}\n")
        
        raise Exception(f"Erro Sintático: {mensagem}")
    
    def mensagem_esperado(self, esperados, token_atual):
        """
        Gera mensagem de erro indicando o que era esperado.
        
        Args:
            esperados: Lista de símbolos esperados
            token_atual: Token que foi encontrado
        """
        if len(esperados) == 1:
            return f"Esperado '{esperados[0]}', mas encontrado '{self.obter_tipo_token(token_atual)}'"
        else:
            esperados_str = "', '".join(esperados)
            return f"Esperado um dos seguintes: '{esperados_str}', mas encontrado '{self.obter_tipo_token(token_atual)}'"
    
    def buscar_producao(self, nao_terminal, terminal):
        """
        Busca uma produção na tabela preditiva.
        
        Args:
            nao_terminal: Símbolo não-terminal (ex: '<programa>')
            terminal: Terminal (tipo do token)
        
        Returns:
            Lista de símbolos da produção ou None se não encontrada
        """
        chave = (nao_terminal, terminal)
        return self.tabela.get(chave)
    
    def analisar(self):
        """
        Executa a análise sintática seguindo o algoritmo preditivo.
        
        Returns:
            NoArvore: Raiz da árvore sintática se análise bem-sucedida
        
        Raises:
            Exception: Se encontrar erro sintático
        """
        # Inicializa pilha com símbolo inicial
        simbolo_inicial = '<programa>'
        self.empilha(simbolo_inicial)
        
        # Cria nó raiz da árvore
        self.arvore_raiz = NoArvore(simbolo_inicial)
        self.pilha_nos.append(self.arvore_raiz)
        
        # Obtém primeiro token
        self.prox_token = self.lexer.proximo_token()
        
        # Loop principal do algoritmo
        while not self.pilha_vazia():
            X = self.topo()
            tipo_token_atual = self.obter_tipo_token(self.prox_token)
            
            # Caso 1: X é terminal
            if self.eh_terminal(X):
                if X == 'ε':
                    # Produção vazia - apenas desempilha
                    self.desempilha()
                    if self.pilha_nos:
                        self.pilha_nos.pop()
                    continue
                
                # Verifica se terminal casa com o token atual
                if X == tipo_token_atual:
                    # Casa! Avança no token
                    self.desempilha()
                    
                    # Adiciona token como folha na árvore
                    if self.pilha_nos:
                        no_pai = self.pilha_nos.pop()
                        no_folha = NoArvore(X, self.prox_token)
                        no_pai.adicionar_filho(no_folha)
                    
                    self.prox_token = self.lexer.proximo_token()
                else:
                    # Erro: terminal não casa
                    self.erro_sintatico(
                        f"Esperado '{X}', mas encontrado '{tipo_token_atual}'",
                        self.prox_token
                    )
            
            # Caso 2: X é não-terminal
            else:
                # Busca produção na tabela
                producao = self.buscar_producao(X, tipo_token_atual)
                
                if producao is None:
                    # Erro: sem entrada na tabela
                    # Tenta buscar possíveis produções para dar erro melhor
                    possiveis = [term for (nt, term) in self.tabela.keys() if nt == X]
                    msg = self.mensagem_esperado(possiveis, self.prox_token)
                    self.erro_sintatico(msg, self.prox_token)
                else:
                    # Produção encontrada: X → Y1 Y2 ... Yn
                    
                    # Desempilha X
                    self.desempilha()
                    no_atual = self.pilha_nos.pop()
                    
                    # Empilha símbolos da produção na ordem reversa
                    # (para que Y1 fique no topo da pilha)
                    simbolos_reversos = list(reversed(producao))
                    
                    # Cria nós filhos para a árvore
                    nos_filhos = []
                    for simbolo in producao:
                        if simbolo != 'ε':
                            filho = NoArvore(simbolo)
                            no_atual.adicionar_filho(filho)
                            nos_filhos.append(filho)
                    
                    # Empilha símbolos e nós correspondentes
                    for simbolo, no_filho in zip(simbolos_reversos, reversed(nos_filhos)):
                        if simbolo != 'ε':
                            self.empilha(simbolo)
                            self.pilha_nos.append(no_filho)
        
        # Verifica se toda a entrada foi consumida
        if self.prox_token is not None:
            self.erro_sintatico(
                f"Entrada não foi completamente consumida. Token inesperado: '{self.obter_tipo_token(self.prox_token)}'",
                self.prox_token
            )
        
        return self.arvore_raiz


# ==============================================================================
# TABELA PREDITIVA
# ==============================================================================
tabela_preditiva = {
    # ------------------------------------------------------------------
    # 0. <programa> -> MAIN ABRE_CHAVES <bloco> FECHA_CHAVES
    # ------------------------------------------------------------------
    ('<programa>', 'MAIN'): ['MAIN', 'ABRE_CHAVES', '<bloco>', 'FECHA_CHAVES'],

    # ------------------------------------------------------------------
    # 1. <bloco> -> <comando> <bloco>
    # (Acionado pelo FIRST de <comando>)
    # ------------------------------------------------------------------
    ('<bloco>', 'VOID'): ['<comando>', '<bloco>'],
    ('<bloco>', 'INT'): ['<comando>', '<bloco>'],
    ('<bloco>', 'CHAR'): ['<comando>', '<bloco>'],
    ('<bloco>', 'FLOAT'): ['<comando>', '<bloco>'],
    ('<bloco>', 'ID'): ['<comando>', '<bloco>'],
    ('<bloco>', 'IF'): ['<comando>', '<bloco>'],
    ('<bloco>', 'WHILE'): ['<comando>', '<bloco>'],
    ('<bloco>', 'FOR'): ['<comando>', '<bloco>'],

    # ------------------------------------------------------------------
    # 2. <bloco> -> ε
    # (Acionado pelo FOLLOW de <bloco> = FECHA_CHAVES)
    # ------------------------------------------------------------------
    ('<bloco>', 'FECHA_CHAVES'): ['ε'],

    # ------------------------------------------------------------------
    # 3. <comando> -> <declaracao> | <atribuicao> | <estrutura_controle>
    # ------------------------------------------------------------------
    ('<comando>', 'VOID'): ['<declaracao>'],
    ('<comando>', 'INT'): ['<declaracao>'],
    ('<comando>', 'CHAR'): ['<declaracao>'],
    ('<comando>', 'FLOAT'): ['<declaracao>'],
    ('<comando>', 'ID'): ['<atribuicao>'],
    ('<comando>', 'IF'): ['<estrutura_controle>'],
    ('<comando>', 'WHILE'): ['<estrutura_controle>'],
    ('<comando>', 'FOR'): ['<estrutura_controle>'],

    # ------------------------------------------------------------------
    # 6. <declaracao> -> <tipo> <lista_declaracao> PONTO_VIRGULA
    # ------------------------------------------------------------------
    ('<declaracao>', 'VOID'): ['<tipo>', '<lista_declaracao>', 'PONTO_VIRGULA'],
    ('<declaracao>', 'INT'): ['<tipo>', '<lista_declaracao>', 'PONTO_VIRGULA'],
    ('<declaracao>', 'CHAR'): ['<tipo>', '<lista_declaracao>', 'PONTO_VIRGULA'],
    ('<declaracao>', 'FLOAT'): ['<tipo>', '<lista_declaracao>', 'PONTO_VIRGULA'],

    # ------------------------------------------------------------------
    # 7-10. <tipo> (Terminais diretos)
    # ------------------------------------------------------------------
    ('<tipo>', 'VOID'): ['VOID'],
    ('<tipo>', 'INT'): ['INT'],
    ('<tipo>', 'CHAR'): ['CHAR'],
    ('<tipo>', 'FLOAT'): ['FLOAT'],

    # ------------------------------------------------------------------
    # 11. <lista_declaracao> -> <declaracao_simples> <lista_declaracao_rest>
    # ------------------------------------------------------------------
    ('<lista_declaracao>', 'ID'): ['<declaracao_simples>', '<lista_declaracao_rest>'],

    # ------------------------------------------------------------------
    # 12. <lista_declaracao_rest> -> VIRGULA ...
    # ------------------------------------------------------------------
    ('<lista_declaracao_rest>', 'VIRGULA'): ['VIRGULA', '<declaracao_simples>', '<lista_declaracao_rest>'],

    # ------------------------------------------------------------------
    # 13. <lista_declaracao_rest> -> ε
    # (Acionado quando a declaração acaba: FOLLOW = PONTO_VIRGULA)
    # ------------------------------------------------------------------
    ('<lista_declaracao_rest>', 'PONTO_VIRGULA'): ['ε'],

    # ------------------------------------------------------------------
    # 14. <declaracao_simples> -> ID <declaracao_simples_rest>
    # ------------------------------------------------------------------
    ('<declaracao_simples>', 'ID'): ['ID', '<declaracao_simples_rest>'],

    # ------------------------------------------------------------------
    # 16-17. <declaracao_simples_rest> -> [NUM] | = expr
    # ------------------------------------------------------------------
    ('<declaracao_simples_rest>', 'ABRE_COLC'): ['ABRE_COLC', 'NUM', 'FECHA_COLC'],
    ('<declaracao_simples_rest>', 'ASSIGN'): ['ASSIGN', '<expressao>'],

    # ------------------------------------------------------------------
    # 15. <declaracao_simples_rest> -> ε
    # (Acionado por FOLLOW: VIRGULA (se tiver mais var) ou PONTO_VIRGULA (se fim))
    # ------------------------------------------------------------------
    ('<declaracao_simples_rest>', 'VIRGULA'): ['ε'],
    ('<declaracao_simples_rest>', 'PONTO_VIRGULA'): ['ε'],

    # ------------------------------------------------------------------
    # 18. <atribuicao> -> ID <atribuicao_rest>
    # ------------------------------------------------------------------
    ('<atribuicao>', 'ID'): ['ID', '<atribuicao_rest>'],

    # ------------------------------------------------------------------
    # 19-20. <atribuicao_rest>
    # ------------------------------------------------------------------
    ('<atribuicao_rest>', 'ASSIGN'): ['ASSIGN', '<expressao>', 'PONTO_VIRGULA'],
    ('<atribuicao_rest>', 'ABRE_COLC'): ['ABRE_COLC', '<expressao>', 'FECHA_COLC', 'ASSIGN', '<expressao>', 'PONTO_VIRGULA'],

    # ------------------------------------------------------------------
    # 21-23. <estrutura_controle>
    # ------------------------------------------------------------------
    ('<estrutura_controle>', 'IF'): ['<if_then>'],
    ('<estrutura_controle>', 'WHILE'): ['<while>'],
    ('<estrutura_controle>', 'FOR'): ['<for>'],

    # ------------------------------------------------------------------
    # 24. <if_then>
    # ------------------------------------------------------------------
    ('<if_then>', 'IF'): ['IF', 'ABRE_PAREN', '<expressao_relacional>', 'FECHA_PAREN', 'THEN', '<bloco_comando>', '<elsif_part>'],

    # ------------------------------------------------------------------
    # 25. <elsif_part> -> ELSIF ...
    # ------------------------------------------------------------------
    ('<elsif_part>', 'ELSIF'): ['ELSIF', 'ABRE_PAREN', '<expressao_relacional>', 'FECHA_PAREN', 'THEN', '<bloco_comando>', '<elsif_part>'],

    # ------------------------------------------------------------------
    # 26. <elsif_part> -> <else_part>
    # (Se encontrar ELSE, vai para else_part. Se encontrar fim de bloco, vai para else_part que vira vazio)
    # ------------------------------------------------------------------
    ('<elsif_part>', 'ELSE'): ['<else_part>'],
    # Follows do IF (o que vem depois do IF inteiro?):
    ('<elsif_part>', 'FECHA_CHAVES'): ['<else_part>'],
    ('<elsif_part>', 'VOID'): ['<else_part>'],
    ('<elsif_part>', 'INT'): ['<else_part>'],
    ('<elsif_part>', 'FLOAT'): ['<else_part>'],
    ('<elsif_part>', 'CHAR'): ['<else_part>'],
    ('<elsif_part>', 'ID'): ['<else_part>'],
    ('<elsif_part>', 'IF'): ['<else_part>'],
    ('<elsif_part>', 'WHILE'): ['<else_part>'],
    ('<elsif_part>', 'FOR'): ['<else_part>'],

    # ------------------------------------------------------------------
    # 27. <else_part> -> ELSE ...
    # ------------------------------------------------------------------
    ('<else_part>', 'ELSE'): ['ELSE', '<bloco_comando>'],

    # ------------------------------------------------------------------
    # 28. <else_part> -> ε
    # (Acionado pelo FOLLOW do comando IF)
    # ------------------------------------------------------------------
    ('<else_part>', 'FECHA_CHAVES'): ['ε'],
    ('<else_part>', 'VOID'): ['ε'],
    ('<else_part>', 'INT'): ['ε'],
    ('<else_part>', 'FLOAT'): ['ε'],
    ('<else_part>', 'CHAR'): ['ε'],
    ('<else_part>', 'ID'): ['ε'],
    ('<else_part>', 'IF'): ['ε'],
    ('<else_part>', 'WHILE'): ['ε'],
    ('<else_part>', 'FOR'): ['ε'],

    # ------------------------------------------------------------------
    # 29-30. <bloco_comando>
    # ------------------------------------------------------------------
    ('<bloco_comando>', 'ABRE_CHAVES'): ['ABRE_CHAVES', '<bloco>', 'FECHA_CHAVES'],
    ('<bloco_comando>', 'VOID'): ['<comando>'],
    ('<bloco_comando>', 'INT'): ['<comando>'],
    ('<bloco_comando>', 'CHAR'): ['<comando>'],
    ('<bloco_comando>', 'FLOAT'): ['<comando>'],
    ('<bloco_comando>', 'ID'): ['<comando>'],
    ('<bloco_comando>', 'IF'): ['<comando>'],
    ('<bloco_comando>', 'WHILE'): ['<comando>'],
    ('<bloco_comando>', 'FOR'): ['<comando>'],

    # ------------------------------------------------------------------
    # 31. <while>
    # ------------------------------------------------------------------
    ('<while>', 'WHILE'): ['WHILE', 'ABRE_PAREN', '<expressao_relacional>', 'FECHA_PAREN', 'DO', '<bloco_comando>'],

    # ------------------------------------------------------------------
    # 32. <for>
    # ------------------------------------------------------------------
    ('<for>', 'FOR'): ['FOR', 'ABRE_PAREN', '<atribuicao_for>', 'PONTO_VIRGULA', '<expressao_relacional>', 'PONTO_VIRGULA', '<atribuicao_for>', 'FECHA_PAREN', 'DO', '<bloco_comando>'],

    # ------------------------------------------------------------------
    # 33. <atribuicao_for>
    # ------------------------------------------------------------------
    ('<atribuicao_for>', 'ID'): ['ID', 'ASSIGN', '<expressao>'],

    # ------------------------------------------------------------------
    # 34. <expressao_relacional>
    # ------------------------------------------------------------------
    ('<expressao_relacional>', 'ID'): ['<expressao>', '<expressao_relacional_rest>'],
    ('<expressao_relacional>', 'NUM'): ['<expressao>', '<expressao_relacional_rest>'],
    ('<expressao_relacional>', 'CONST_CHAR'): ['<expressao>', '<expressao_relacional_rest>'],
    ('<expressao_relacional>', 'ABRE_PAREN'): ['<expressao>', '<expressao_relacional_rest>'],
    ('<expressao_relacional>', 'SOMA'): ['<expressao>', '<expressao_relacional_rest>'],
    ('<expressao_relacional>', 'SUBTRACAO'): ['<expressao>', '<expressao_relacional_rest>'],

    # ------------------------------------------------------------------
    # 35. <expressao_relacional_rest> -> op rel ...
    # ------------------------------------------------------------------
    ('<expressao_relacional_rest>', 'EQEQ'): ['<relop>', '<expressao>'],
    ('<expressao_relacional_rest>', 'NE'): ['<relop>', '<expressao>'],
    ('<expressao_relacional_rest>', 'LT'): ['<relop>', '<expressao>'],
    ('<expressao_relacional_rest>', 'GT'): ['<relop>', '<expressao>'],
    ('<expressao_relacional_rest>', 'LE'): ['<relop>', '<expressao>'],
    ('<expressao_relacional_rest>', 'GE'): ['<relop>', '<expressao>'],

    # ------------------------------------------------------------------
    # 36. <expressao_relacional_rest> -> ε
    # (FOLLOW: FECHA_PAREN, PONTO_VIRGULA, etc.)
    # ------------------------------------------------------------------
    ('<expressao_relacional_rest>', 'FECHA_PAREN'): ['ε'],
    ('<expressao_relacional_rest>', 'PONTO_VIRGULA'): ['ε'],
    ('<expressao_relacional_rest>', 'DO'): ['ε'],
    ('<expressao_relacional_rest>', 'THEN'): ['ε'],

    # ------------------------------------------------------------------
    # 37-42. <relop>
    # ------------------------------------------------------------------
    ('<relop>', 'EQEQ'): ['EQEQ'],
    ('<relop>', 'NE'): ['NE'],
    ('<relop>', 'LT'): ['LT'],
    ('<relop>', 'GT'): ['GT'],
    ('<relop>', 'LE'): ['LE'],
    ('<relop>', 'GE'): ['GE'],

    # ------------------------------------------------------------------
    # 43. <expressao>
    # ------------------------------------------------------------------
    ('<expressao>', 'ID'): ['<termo>', '<expressao_rest>'],
    ('<expressao>', 'NUM'): ['<termo>', '<expressao_rest>'],
    ('<expressao>', 'CONST_CHAR'): ['<termo>', '<expressao_rest>'],
    ('<expressao>', 'ABRE_PAREN'): ['<termo>', '<expressao_rest>'],
    ('<expressao>', 'SOMA'): ['<termo>', '<expressao_rest>'],
    ('<expressao>', 'SUBTRACAO'): ['<termo>', '<expressao_rest>'],

    # ------------------------------------------------------------------
    # 44-45. <expressao_rest> -> + | -
    # ------------------------------------------------------------------
    ('<expressao_rest>', 'SOMA'): ['SOMA', '<termo>', '<expressao_rest>'],
    ('<expressao_rest>', 'SUBTRACAO'): ['SUBTRACAO', '<termo>', '<expressao_rest>'],

    # ------------------------------------------------------------------
    # 46. <expressao_rest> -> ε
    # (FOLLOW: tokens que encerram expressões aritméticas)
    # ------------------------------------------------------------------
    ('<expressao_rest>', 'PONTO_VIRGULA'): ['ε'],
    ('<expressao_rest>', 'FECHA_PAREN'): ['ε'],
    ('<expressao_rest>', 'FECHA_COLC'): ['ε'],
    ('<expressao_rest>', 'EQEQ'): ['ε'],
    ('<expressao_rest>', 'NE'): ['ε'],
    ('<expressao_rest>', 'LT'): ['ε'],
    ('<expressao_rest>', 'GT'): ['ε'],
    ('<expressao_rest>', 'LE'): ['ε'],
    ('<expressao_rest>', 'GE'): ['ε'],
    ('<expressao_rest>', 'THEN'): ['ε'],
    ('<expressao_rest>', 'DO'): ['ε'],

    # ------------------------------------------------------------------
    # 47. <termo>
    # ------------------------------------------------------------------
    ('<termo>', 'ID'): ['<potencia>', '<termo_rest>'],
    ('<termo>', 'NUM'): ['<potencia>', '<termo_rest>'],
    ('<termo>', 'CONST_CHAR'): ['<potencia>', '<termo_rest>'],
    ('<termo>', 'ABRE_PAREN'): ['<potencia>', '<termo_rest>'],
    ('<termo>', 'SOMA'): ['<potencia>', '<termo_rest>'],
    ('<termo>', 'SUBTRACAO'): ['<potencia>', '<termo_rest>'],

    # ------------------------------------------------------------------
    # 48-49. <termo_rest> -> * | /
    # ------------------------------------------------------------------
    ('<termo_rest>', 'MULTIPLICACAO'): ['MULTIPLICACAO', '<potencia>', '<termo_rest>'],
    ('<termo_rest>', 'DIVISAO'): ['DIVISAO', '<potencia>', '<termo_rest>'],

    # ------------------------------------------------------------------
    # 50. <termo_rest> -> ε
    # (FOLLOW: + e - (pois voltam pra expressao) e os followers de expressao)
    # ------------------------------------------------------------------
    ('<termo_rest>', 'SOMA'): ['ε'],
    ('<termo_rest>', 'SUBTRACAO'): ['ε'],
    ('<termo_rest>', 'PONTO_VIRGULA'): ['ε'],
    ('<termo_rest>', 'FECHA_PAREN'): ['ε'],
    ('<termo_rest>', 'FECHA_COLC'): ['ε'],
    ('<termo_rest>', 'EQEQ'): ['ε'],
    ('<termo_rest>', 'NE'): ['ε'],
    ('<termo_rest>', 'LT'): ['ε'],
    ('<termo_rest>', 'GT'): ['ε'],
    ('<termo_rest>', 'LE'): ['ε'],
    ('<termo_rest>', 'GE'): ['ε'],
    ('<termo_rest>', 'THEN'): ['ε'],
    ('<termo_rest>', 'DO'): ['ε'],

    # ------------------------------------------------------------------
    # 51. <potencia>
    # ------------------------------------------------------------------
    ('<potencia>', 'ID'): ['<fator>', '<potencia_rest>'],
    ('<potencia>', 'NUM'): ['<fator>', '<potencia_rest>'],
    ('<potencia>', 'CONST_CHAR'): ['<fator>', '<potencia_rest>'],
    ('<potencia>', 'ABRE_PAREN'): ['<fator>', '<potencia_rest>'],
    ('<potencia>', 'SOMA'): ['<fator>', '<potencia_rest>'],
    ('<potencia>', 'SUBTRACAO'): ['<fator>', '<potencia_rest>'],

    # ------------------------------------------------------------------
    # 52. <potencia_rest> -> ^ ...
    # ------------------------------------------------------------------
    ('<potencia_rest>', 'POTENCIA'): ['POTENCIA', '<fator>', '<potencia_rest>'],

    # ------------------------------------------------------------------
    # 53. <potencia_rest> -> ε
    # (FOLLOW: *, /, +, - e followers de expressao)
    # ------------------------------------------------------------------
    ('<potencia_rest>', 'MULTIPLICACAO'): ['ε'],
    ('<potencia_rest>', 'DIVISAO'): ['ε'],
    ('<potencia_rest>', 'SOMA'): ['ε'],
    ('<potencia_rest>', 'SUBTRACAO'): ['ε'],
    ('<potencia_rest>', 'PONTO_VIRGULA'): ['ε'],
    ('<potencia_rest>', 'FECHA_PAREN'): ['ε'],
    ('<potencia_rest>', 'FECHA_COLC'): ['ε'],
    ('<potencia_rest>', 'EQEQ'): ['ε'],
    ('<potencia_rest>', 'NE'): ['ε'],
    ('<potencia_rest>', 'LT'): ['ε'],
    ('<potencia_rest>', 'GT'): ['ε'],
    ('<potencia_rest>', 'LE'): ['ε'],
    ('<potencia_rest>', 'GE'): ['ε'],
    ('<potencia_rest>', 'THEN'): ['ε'],
    ('<potencia_rest>', 'DO'): ['ε'],

    # ------------------------------------------------------------------
    # 54-59. <fator>
    # ------------------------------------------------------------------
    ('<fator>', 'ID'): ['ID', '<fator_rest>'],
    ('<fator>', 'NUM'): ['NUM'],
    ('<fator>', 'CONST_CHAR'): ['CONST_CHAR'],
    ('<fator>', 'ABRE_PAREN'): ['ABRE_PAREN', '<expressao>', 'FECHA_PAREN'],
    ('<fator>', 'SOMA'): ['SOMA', '<fator>'],
    ('<fator>', 'SUBTRACAO'): ['SUBTRACAO', '<fator>'],

    # ------------------------------------------------------------------
    # 60. <fator_rest> -> [ ... ]
    # ------------------------------------------------------------------
    ('<fator_rest>', 'ABRE_COLC'): ['ABRE_COLC', '<expressao>', 'FECHA_COLC'],

    # ------------------------------------------------------------------
    # 61. <fator_rest> -> ε
    # (FOLLOW: ^, *, /, +, - e followers de expressao)
    # ------------------------------------------------------------------
    ('<fator_rest>', 'POTENCIA'): ['ε'],
    ('<fator_rest>', 'MULTIPLICACAO'): ['ε'],
    ('<fator_rest>', 'DIVISAO'): ['ε'],
    ('<fator_rest>', 'SOMA'): ['ε'],
    ('<fator_rest>', 'SUBTRACAO'): ['ε'],
    ('<fator_rest>', 'PONTO_VIRGULA'): ['ε'],
    ('<fator_rest>', 'FECHA_PAREN'): ['ε'],
    ('<fator_rest>', 'FECHA_COLC'): ['ε'],
    ('<fator_rest>', 'EQEQ'): ['ε'],
    ('<fator_rest>', 'NE'): ['ε'],
    ('<fator_rest>', 'LT'): ['ε'],
    ('<fator_rest>', 'GT'): ['ε'],
    ('<fator_rest>', 'LE'): ['ε'],
    ('<fator_rest>', 'GE'): ['ε'],
    ('<fator_rest>', 'THEN'): ['ε'],
    ('<fator_rest>', 'DO'): ['ε']
}
