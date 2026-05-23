# ============================================================
#  lexer.py -  Analisador Léxico da Linguagem FIN
# ============================================================

import re

# Palavras reservadas
RESERVED = {
    'ohj', 'lop',
    'kok', 'des', 'tek', 'tot',
    'jos', 'muu',
    'kun', 'var', 'do',
    'lue', 'kir',
    'totta', 'vaara',
    'ja', 'tai', 'ei',
    'de', 'ate', 'passo',
}

# Especificação dos tokens (ordem importa)
TOKEN_SPEC = [
    ('NUM',    r'\d+\.\d+|\d+'),          
    ('STR',    r'"[^"]*"'),                
    ('LE',     r'<='),                     
    ('GE',     r'>='),
    ('EQ',     r'=='),
    ('NEQ',    r'!='),
    ('ASSIGN', r':='),                     
    ('LT',     r'<'),
    ('GT',     r'>'),
    ('PLUS',   r'\+'),
    ('MINUS',  r'-'),
    ('TIMES',  r'\*'),
    ('DIVIDE', r'/'),
    ('MOD',    r'%'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COMMA',  r','),
    ('DOT',    r'\.'),
    ('ID',     r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('SKIP',   r'[ \t\r\n]+'),
    ('COMMENT',r'#[^\n]*'),
    ('MISMATCH', r'.'),
]

MASTER_RE = re.compile(
    '|'.join(f'(?P<{name}>{pat})' for name, pat in TOKEN_SPEC)
)


class Token:
    def __init__(self, type_, value, line):
        self.type  = type_
        self.value = value
        self.line  = line

    def __repr__(self):
        return f'Token({self.type}, {self.value!r}, linha={self.line})'


class LexerError(Exception):
    pass


def tokenize(source: str) -> list[Token]:
    """Converte o código-fonte FIN em lista de tokens."""
    tokens = []
    line   = 1

    for mo in MASTER_RE.finditer(source):
        kind  = mo.lastgroup
        value = mo.group()

        if kind == 'SKIP':
            line += value.count('\n')
            continue
        if kind == 'COMMENT':
            continue
        if kind == 'MISMATCH':
            raise LexerError(f'Caractere inválido {value!r} na linha {line}')

        # Identificador → pode ser palavra reservada
        if kind == 'ID' and value in RESERVED:
            kind = value.upper()   # ex.: 'ohj' → 'OHJ'

        tokens.append(Token(kind, value, line))

    tokens.append(Token('EOF', '', line))
    return tokens
