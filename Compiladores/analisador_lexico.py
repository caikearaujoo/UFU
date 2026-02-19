class Token:
    def __init__(self, tipo, linha, coluna, atributo=None):
        self.tipo = tipo
        self.linha = linha
        self.coluna = coluna
        self.atributo = atributo
    
    def __str__(self):
        # Se tiver atributo (ex: LE, GT, ponteiro tab simbolo), imprime ele na tupla
        if self.atributo is not None:
            valor = self.atributo
        else:
            valor = " "
        return f"<{self.tipo}, {valor}> (L:{self.linha}, C:{self.coluna})"


class AnalisadorLexico:
    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.pos = 0
        self.linha = 1
        self.coluna = 1
        self.tamanho = len(codigo_fonte)
        
        # Armazena linhas do código para exibir em erros
        self.linhas_codigo = codigo_fonte.split('\n')
        
        # --- Tabela Híbrida ---
        self.tabela_dados = []  # Lista (0, 1, 2...) para guardar os dados
        self.tabela_busca = {} 
        
        # Inicializa com Palavras Reservadas
        palavras_iniciais = {
            'main': 'MAIN',
            'int': 'INT',
            'float': 'FLOAT',
            'char': 'CHAR',
            'void': 'VOID',
            'if': 'IF',
            'else': 'ELSE',
            'elsif': 'ELSIF',
            'then': 'THEN',
            'while': 'WHILE',
            'do': 'DO',
            'for': 'FOR',
        }
        
        for palavra, token in palavras_iniciais.items():
            self._add_tabela(palavra, token)
    
    def _add_tabela(self, lexema, tipo_token):
        """Adiciona algo na tabela e retorna o índice (int)"""
        idx = len(self.tabela_dados)
        self.tabela_dados.append({'lexema': lexema, 'tipo': tipo_token})
        self.tabela_busca[lexema] = idx
        return idx
    
    def instalar_id(self, lexema):
        """Verifica se o ID existe. Se não, cria. Retorna (Tipo, Atributo)"""
        idx = self.tabela_busca.get(lexema)
        if idx is not None:
            # Já existe (pode ser palavra chave ou ID antigo)
            dados = self.tabela_dados[idx]
            if dados['tipo'] == 'ID':
                return "ID", idx  # Retorna ID e o índice na tabela
            else:
                return dados['tipo'], None  # Palavras reservadas não precisam de atributo
        else:
            # Novo ID
            novo_idx = self._add_tabela(lexema, 'ID')
            return "ID", novo_idx
    
    def erro_lexico(self, mensagem, linha, coluna):
        """
        Gera uma mensagem de erro léxico útil com indicador visual de coluna.
        
        Args:
            mensagem: Descrição do erro
            linha: Linha onde ocorreu o erro
            coluna: Coluna onde ocorreu o erro
        """
        print(f"\n{'='*70}")
        print(f"ERRO LÉXICO na Linha {linha}, Coluna {coluna}")
        print(f"{'='*70}")
        
        # Mostra a linha do código onde ocorreu o erro
        if 1 <= linha <= len(self.linhas_codigo):
            linha_codigo = self.linhas_codigo[linha - 1]
            print(f"\n{linha:4} | {linha_codigo}")
            
            # Cria indicador visual da coluna (seta apontando para o erro)
            espacos = ' ' * (7 + coluna - 1)  # 7 = len("    | ")
            print(f"{espacos}^")
            print(f"{espacos}|")
            print(f"{espacos}Erro aqui\n")
        
        print(f"Mensagem: {mensagem}")
        print(f"{'='*70}\n")
        
        raise Exception(f"Erro Léxico: {mensagem}")
    
    def proximo_char(self):
        if self.pos >= self.tamanho:
            return None  # Fim de arquivo (EOF)
        char = self.codigo[self.pos]
        self.pos += 1
        if char == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
        return char
    
    def retract(self):
        """Volta um caractere"""
        if self.pos > 0:
            self.pos -= 1
            if self.pos < len(self.codigo) and self.codigo[self.pos] == '\n':
                self.linha -= 1
            else:
                self.coluna -= 1
    
    def proximo_token(self):
        estado = 0
        lexema = ""
        inicio_coluna = self.coluna
        inicio_linha = self.linha
        
        while True:
            char = self.proximo_char()
            
            # --- ESTADO 0: ESTADO INICIAL ---
            if estado == 0:
                if char is None:
                    return None  # Fim da análise
                
                inicio_coluna = self.coluna - 1
                inicio_linha = self.linha
                lexema = char
                
                # Identificadores e Palavras Reservadas
                if char.isalpha() or char == '_':
                    estado = 44
                # Números (Dígitos)
                elif char.isdigit():
                    estado = 32
                # Operadores Relacionais e Lógicos
                elif char == '<':
                    estado = 8
                elif char == '>':
                    estado = 11
                elif char == '=':
                    estado = 14
                elif char == '!':
                    estado = 16
                # Delimitadores
                elif char == ';':
                    return Token("PONTO_VIRGULA", inicio_linha, inicio_coluna)
                elif char == ',':
                    return Token("VIRGULA", inicio_linha, inicio_coluna)
                elif char == '(':
                    return Token("ABRE_PAREN", inicio_linha, inicio_coluna)
                elif char == ')':
                    return Token("FECHA_PAREN", inicio_linha, inicio_coluna)
                elif char == '}':
                    return Token("FECHA_CHAVES", inicio_linha, inicio_coluna)
                elif char == '[':
                    return Token("ABRE_COLC", inicio_linha, inicio_coluna)
                elif char == ']':
                    return Token("FECHA_COLC", inicio_linha, inicio_coluna)
                elif char == '{':
                    estado = 21
                # Operadores Aritméticos
                elif char == '+':
                    return Token("SOMA", inicio_linha, inicio_coluna)
                elif char == '-':
                    return Token("SUBTRACAO", inicio_linha, inicio_coluna)
                elif char == '/':
                    return Token("DIVISAO", inicio_linha, inicio_coluna)
                elif char == '*':
                    estado = 1
                # Assign
                elif char == ':':
                    estado = 6
                # CONST_CHAR
                elif char == "'":
                    estado = 39
                    lexema = ""
                # WS
                elif char.isspace():
                    estado = 42
                    lexema = ""
                else:
                    self.erro_lexico(f"Caractere inválido '{char}'", self.linha, self.coluna)
            
            # --- ESTADO 44: IDENTIFICADORES ---
            elif estado == 44:
                if char is not None and (char.isalnum() or char == '_'):
                    lexema += char
                else:
                    self.retract()
                    tipo, atributo_idx = self.instalar_id(lexema)
                    return Token(tipo, inicio_linha, inicio_coluna, atributo=atributo_idx)
            
            # --- ESTADOS NUMÉRICOS ---
            elif estado == 32:
                if char is not None and char.isdigit():
                    lexema += char
                elif char == '.':
                    lexema += char
                    estado = 33
                elif char == 'E':
                    lexema += char
                    estado = 36
                else:
                    self.retract()
                    idx = self._add_tabela(lexema, "NUM")
                    return Token("NUM", inicio_linha, inicio_coluna, atributo=idx)
            
            elif estado == 33:
                if char is not None and char.isdigit():
                    lexema += char
                    estado = 34
                else:
                    self.erro_lexico(f"Esperado dígito após '.' no número '{lexema}'", self.linha, self.coluna)
            
            elif estado == 34:
                if char is not None and char.isdigit():
                    lexema += char
                elif char == 'E':
                    lexema += char
                    estado = 36
                else:
                    self.retract()
                    idx = self._add_tabela(lexema, "NUM")
                    return Token("NUM", inicio_linha, inicio_coluna, atributo=idx)
            
            elif estado == 36:
                if char == '+' or char == '-':
                    lexema += char
                    estado = 37
                elif char is not None and char.isdigit():
                    lexema += char
                    estado = 38
                else:
                    self.erro_lexico(f"Malformação em número exponencial '{lexema}'", self.linha, self.coluna)
            
            elif estado == 37:
                if char is not None and char.isdigit():
                    lexema += char
                    estado = 38
                else:
                    self.erro_lexico(f"Esperado dígito no expoente de '{lexema}'", self.linha, self.coluna)
            
            elif estado == 38:
                if char is not None and char.isdigit():
                    lexema += char
                else:
                    self.retract()
                    idx = self._add_tabela(lexema, "NUM")
                    return Token("NUM", inicio_linha, inicio_coluna, atributo=idx)
            
            # --- OPERADORES RELACIONAIS ---
            elif estado == 8:
                if char == '=':
                    return Token("RELOP", inicio_linha, inicio_coluna, atributo="LE")
                else:
                    self.retract()
                    return Token("RELOP", inicio_linha, inicio_coluna, atributo="LT")
            
            elif estado == 11:
                if char == '=':
                    return Token("RELOP", inicio_linha, inicio_coluna, atributo="GE")
                else:
                    self.retract()
                    return Token("RELOP", inicio_linha, inicio_coluna, atributo="GT")
            
            elif estado == 14:
                if char == '=':
                    return Token("RELOP", inicio_linha, inicio_coluna, atributo="EQEQ")
                else:
                    self.erro_lexico("'=' isolado não é válido. Use ':=' para atribuição ou '==' para comparação", inicio_linha, inicio_coluna)
            
            elif estado == 16:
                if char == '=':
                    return Token("RELOP", inicio_linha, inicio_coluna, atributo="NE")
                else:
                    self.erro_lexico("Esperado '=' após '!' para formar '!='", self.linha, self.coluna)
            
            # --- COMENTÁRIOS ---
            elif estado == 21:
                if char == '%':
                    estado = 22
                else:
                    self.retract()
                    return Token("ABRE_CHAVES", inicio_linha, inicio_coluna)
            
            elif estado == 22:
                if char is None:
                    self.erro_lexico(f"Comentário não fechado iniciado na linha {inicio_linha}", self.linha, self.coluna)
                elif char == '%':
                    estado = 23
                # Continua lendo o comentário
            
            elif estado == 23:
                if char == '}':
                    # Comentário fechado, volta ao estado inicial
                    estado = 0
                    lexema = ""
                elif char == '%':
                    # Continua no estado 23 (múltiplos %)
                    pass
                else:
                    # Volta a ler conteúdo do comentário
                    estado = 22
            
            # --- POTÊNCIA OU MULTIPLICAÇÃO ---
            elif estado == 1:
                if char == '*':
                    return Token("POTENCIA", inicio_linha, inicio_coluna)
                else:
                    self.retract()
                    return Token("MULTIPLICACAO", inicio_linha, inicio_coluna)
            
            # --- ASSIGN ---
            elif estado == 6:
                if char == '=':
                    return Token("ASSIGN", inicio_linha, inicio_coluna)
                else:
                    self.retract()
                    self.erro_lexico("Esperado '=' após ':' para formar ':='", self.linha, self.coluna)
            
            # --- CONST_CHAR ---
            elif estado == 39:
                if char is None:
                    self.erro_lexico(f"Caractere literal não fechado iniciado na linha {inicio_linha}", self.linha, self.coluna)
                elif char == '\n' or char == '\t':
                    self.erro_lexico("Caractere literal não pode conter quebra de linha ou tab", self.linha, self.coluna)
                elif char == "'":
                    self.erro_lexico("Caractere literal vazio", self.linha, self.coluna)
                else:
                    lexema = char
                    estado = 40
            
            elif estado == 40:
                if char == "'":
                    idx = self._add_tabela(lexema, "CONST_CHAR")
                    return Token("CONST_CHAR", inicio_linha, inicio_coluna, atributo=idx)
                else:
                    self.erro_lexico(f"Esperado \"'\" para fechar caractere literal '{lexema}'", self.linha, self.coluna)
            
            # --- WHITESPACE ---
            elif estado == 42:
                if char is not None and char.isspace():
                    pass  # Continua ignorando espaços.
                else:
                    # Encontrou um caractere não-espaço.
                    if char is not None:
                        self.retract()
                    estado = 0
                    lexema = ""
                    continue  # Força nova iteração do loop para processar no estado 0.


# --- TESTE DO CÓDIGO ---
if __name__ == "__main__":
    codigo_teste = """
main {
    float contador := 10;
    int maximo := 50;
    {% Inicio do comentário de teste %}
    if (contador >= 10) then {
        contador := contador + 1;
    }
    while (contador < maximo) do {
        contador := contador + 2;
    }
}
"""
    
    print("=== Iniciando Análise Léxica ===\n")
    lexer = AnalisadorLexico(codigo_teste)
    
    print(f"--- Tabela Inicial ({len(lexer.tabela_dados)} itens) ---")
    print("IDX | TIPO       | LEXEMA")
    print("-" * 35)
    for i, item in enumerate(lexer.tabela_dados):
        print(f"{i:3} | {item['tipo']:10} | {item['lexema']}")
    print()
    
    try:
        print("--- Tokens Gerados ---")
        while True:
            token = lexer.proximo_token()
            if token is None:
                break
            print(token)
        
        print("\n=== Análise Concluída ===")
        
        # Imprime a tabela final.
        print("\n--- Tabela de Símbolos Final ---")
        print("IDX | TIPO       | LEXEMA")
        print("-" * 35)
        for i, item in enumerate(lexer.tabela_dados):
            if i >= 12:  # Mostra apenas itens adicionados durante análise.
                print(f"{i:3} | {item['tipo']:10} | {item['lexema']}")
    
    except Exception as e:
        print(f"\n[ERRO] {e}")
