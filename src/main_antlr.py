#!/usr/bin/env python3
# ============================================================
#  main.py  —  Transpilador FIN → Python usando ANTLR4
#  Uso:  python main.py <arquivo.fin> [-o saida.py]
# ============================================================

import sys
import os

# Paths
SRC_DIR   = os.path.dirname(__file__)
ANTLR_DIR = os.path.join(SRC_DIR, '..', 'antlr')
sys.path.insert(0, SRC_DIR)
sys.path.insert(0, ANTLR_DIR)

from antlr4 import CommonTokenStream, FileStream, ParseTreeWalker
from antlr4.error.ErrorListener import ErrorListener

from FINLexer  import FINLexer
from FINParser import FINParser
from semantic_antlr import SemanticError, analyze
from codegen_antlr  import generate


# Listener de erros do ANTLR
class FINErrorListener(ErrorListener):
    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.errors.append(
            f'Linha {line}, coluna {column}: {msg}'
        )


def transpile(input_path: str) -> str:
    """Recebe caminho do .fin e retorna código Python como string."""

    # 1. Leitura do arquivo
    stream = FileStream(input_path, encoding='utf-8')

    # 2. Análise léxica
    lexer        = FINLexer(stream)
    token_stream = CommonTokenStream(lexer)

    # 3. Análise sintática
    parser        = FINParser(token_stream)
    error_listener = FINErrorListener()
    parser.removeErrorListeners()
    parser.addErrorListener(error_listener)

    tree = parser.prog()

    if error_listener.errors:
        for err in error_listener.errors:
            print(f'[Erro Sintático] {err}')
        sys.exit(1)

    # 4. Análise semântica
    symbols = analyze(tree, parser)

    # 5. Geração de código
    return generate(tree, symbols)


def main():
    if len(sys.argv) < 2:
        print('Uso: python main.py <arquivo.fin> [-o saida.py]')
        sys.exit(1)

    input_path = sys.argv[1]

    if '-o' in sys.argv:
        output_path = sys.argv[sys.argv.index('-o') + 1]
    else:
        output_path = os.path.splitext(input_path)[0] + '.py'

    try:
        with open(input_path, encoding='utf-8'):
            pass
    except FileNotFoundError:
        print(f'Erro: arquivo "{input_path}" não encontrado.')
        sys.exit(1)

    try:
        python_code = transpile(input_path)
    except SemanticError as e:
        print(f'[Erro Semântico] {e}')
        sys.exit(1)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(python_code)

    print(f'✓ Transpilação concluída: "{input_path}" → "{output_path}"')


if __name__ == '__main__':
    main()
