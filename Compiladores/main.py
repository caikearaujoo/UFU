"""
COMPILADOR - MAIN
Arquivo principal que integra Análise Léxica e Análise Sintática
Uso: python main.py codigo.txt
"""

import sys
from analisador_lexico import AnalisadorLexico
from analisador_sintatico import AnalisadorSintatico, tabela_preditiva


def compilar(codigo_fonte):
    """
    Compila um código fonte completo.
    
    Args:
        codigo_fonte (str): Código fonte a ser compilado
    
    Returns:
        NoArvore: Árvore sintática se sucesso, None se erro
    """
    print("\n" + "="*70)
    print("CÓDIGO FONTE")
    print("="*70)
    print(codigo_fonte)
    print("="*70 + "\n")
    
    try:
        # Fase 1: Análise Léxica
        print("📝 Iniciando Análise Léxica...")
        lexer = AnalisadorLexico(codigo_fonte)
        
        # Fase 2: Análise Sintática
        print("🔍 Iniciando Análise Sintática...\n")
        parser = AnalisadorSintatico(lexer, tabela_preditiva)
        arvore = parser.analisar()
        
        # Sucesso - Imprime árvore
        print("\n" + "="*70)
        print("ÁRVORE SINTÁTICA")
        print("="*70 + "\n")
        arvore.imprimir_arvore()
        
        print("\n" + "="*70)
        print("✅ COMPILAÇÃO CONCLUÍDA COM SUCESSO!")
        print("="*70 + "\n")
        
        return arvore
        
    except Exception as e:
        print("\n" + "="*70)
        print("❌ COMPILAÇÃO FALHOU")
        print("="*70)
        print(f"\n{e}\n")
        return None


if __name__ == "__main__":
    # Verifica se passou o arquivo como argumento
    if len(sys.argv) < 2:
        print("\n❌ Uso: python main.py <arquivo.txt>")
        print("Exemplo: python main.py codigo.txt\n")
        sys.exit(1)
    
    arquivo = sys.argv[1]
    
    # Lê o arquivo
    try:
        print(f"\n📂 Lendo arquivo: {arquivo}")
        with open(arquivo, 'r', encoding='utf-8') as f:
            codigo = f.read()
        
        # Compila
        compilar(codigo)
        
    except FileNotFoundError:
        print(f"\n❌ Erro: Arquivo '{arquivo}' não encontrado.\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro ao ler arquivo: {e}\n")
        sys.exit(1)