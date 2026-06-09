# Transpilador FIN → Python
### Documentação Técnica Completa

**Disciplina:** Teoria da Computação e Compiladores  
**Professor:** Eduardo Xavier

---

## Integrantes do Grupo

- Camila Louzada Moraes
- Nicolle Brasil dos Santos Nery
- Gustavo Burgos Bittencourt Figueiredo
- Diego Amaro Ferreira
- Juan Pablo dos Santos Rodrigues

---

## 1. Introdução

O Transpilador FIN é um programa que converte código escrito na Linguagem FIN — uma linguagem didática com palavras-chave derivadas do idioma finlandês — para código Python 3 equivalente, executável sem erros.

O projeto utiliza a ferramenta ANTLR4 (Another Tool for Language Recognition) para as fases de análise léxica e sintática, com as fases semântica e de geração de código implementadas manualmente em Python usando o padrão Visitor.

| Item | Descrição |
|---|---|
| Linguagem de origem | FIN (palavras-chave em finlandês) |
| Linguagem de destino | Python 3 |
| Ferramenta de parsing | ANTLR 4.9.3 |
| Estratégia | Gramática formal + Visitor Pattern |
| Interface | Web (Flask + HTML/JS) |

---

## 2. A Linguagem FIN

### 2.1 Estrutura de um Programa

Todo programa FIN começa com `ohj` e termina com `lop`. As declarações de variáveis vêm logo após `ohj`, seguidas pelos comandos.

```
ohj
kok a, b.
des media.
a := 10.
b := 20.
media := (a + b) / 2.
kir(media).
lop
```

### 2.2 Tipos de Dados

| Tipo FIN | Original (FI) | Python | Valor Padrão | Exemplo |
|---|---|---|---|---|
| `kok` | kokonaisluku | int | 0 | `kok x, y.` |
| `des` | desimaali | float | 0.0 | `des media.` |
| `tek` | teksti | str | '' | `tek nome.` |
| `tot` | totuus | bool | False | `tot ativo.` |

### 2.3 Palavras Reservadas

| Token FIN | Original (FI) | Python | Descrição |
|---|---|---|---|
| `ohj` | ohjelma | — | Início do programa |
| `lop` | loppu | — | Fim do programa |
| `kok` | kokonaisluku | int | Tipo inteiro |
| `des` | desimaali | float | Tipo decimal |
| `tek` | teksti | str | Tipo texto |
| `tot` | totuus | bool | Tipo booleano |
| `jos` | jos | if | Condicional |
| `muu` | muuten | else | Alternativa |
| `kun` | kun | while | Laço while |
| `var` | varten | for | Laço for |
| `do` | — | while True | Laço do-while |
| `lue` | lukea | input() | Leitura do teclado |
| `kir` | kirjoita | print() | Impressão na tela |
| `totta` | totta | True | Booleano verdadeiro |
| `vaara` | vaara | False | Booleano falso |
| `ja` | ja | and | Operador lógico E |
| `tai` | tai | or | Operador lógico OU |
| `ei` | ei | not | Operador lógico NÃO |
| `de` | — | — | Início do intervalo (for) |
| `ate` | asti | range() | Fim do intervalo (for) |

### 2.4 Operadores

| Operador | Tipo | Exemplo FIN | Python gerado |
|---|---|---|---|
| `+` `-` `*` `/` `%` | Aritmético | `a + b * c` | `(a + (b * c))` |
| `<` `>` `<=` `>=` `==` `!=` | Relacional | `a >= b` | `a >= b` |
| `:=` | Atribuição | `x := 10.` | `x = 10` |
| `ja` | Lógico E | `a ja b` | `a and b` |
| `tai` | Lógico OU | `a tai b` | `a or b` |
| `ei` | Lógico NÃO | `ei a` | `not a` |

---

## 3. Gramática Formal

Gramática BNF estendida, sem recursão à esquerda e sem produções vazias. O parser é LL(1), gerado pelo ANTLR4.

```
prog     → ohj decl+ cmd+ lop EOF

decl     → tipo ID (',' ID)* '.'
tipo     → kok | des | tek | tot

cmd      → cmdAtrib | cmdLeitura | cmdEscrita
         | cmdIf | cmdKun | cmdVar | cmdDoKun

cmdAtrib   → ID ':=' expr '.'
cmdLeitura → lue '(' ID ')' '.'
cmdEscrita → kir '(' expr ')' '.'
cmdIf      → jos '(' cond ')' '{' cmd+ '}' (muu '{' cmd+ '}')?
cmdKun     → kun '(' cond ')' '{' cmd+ '}'
cmdVar     → var ID de expr ate expr '{' cmd+ '}'
cmdDoKun   → do '{' cmd+ '}' kun '(' cond ')' '.'

cond  → ei expr
      | expr opRel expr
      | expr opLog expr

opRel → '<' | '>' | '<=' | '>=' | '==' | '!='
opLog → ja | tai

expr  → expr ('*'|'/'|'%') expr   ← maior precedência
      | expr ('+'|'-') expr
      | '(' expr ')'
      | NUM | STR | ID | totta | vaara

NUM   → [0-9]+ ('.' [0-9]+)?
STR   → '"' (~["\r\n])* '"'
ID    → [a-zA-Z_][a-zA-Z0-9_]*
```

---

## 4. Arquitetura do Transpilador

```
arquivo .fin
      │
      ▼
┌──────────────────────┐
│  FINLexer.py (ANTLR) │  Análise Léxica — tokenização automática
└──────────────────────┘
      │  stream de tokens
      ▼
┌───────────────────────┐
│  FINParser.py (ANTLR) │  Análise Sintática — árvore gerada automaticamente
└───────────────────────┘
      │  Parse Tree
      ▼
┌──────────────────┐
│  semantic_antlr  │  Análise Semântica — Visitor manual
└──────────────────┘
      │  Parse Tree + tabela de símbolos
      ▼
┌─────────────────┐
│  codegen_antlr  │  Geração de Código — Visitor manual
└─────────────────┘
      │
      ▼
arquivo .py
```

### 4.1 FINLexer.py e FINParser.py — Gerados pelo ANTLR

O ANTLR lê o arquivo `FIN.g4` e gera automaticamente o lexer e o parser. Comando usado:

```bash
java -jar antlr4.jar -Dlanguage=Python3 -visitor FIN.g4
```

### 4.2 semantic_antlr.py — Análise Semântica

Implementa o padrão Visitor sobre a Parse Tree. Verifica:

- Variável declarada antes do uso
- Redeclaração de variável
- Compatibilidade de tipo em atribuições
- Variável de controle do `for` deve ser do tipo `kok`

### 4.3 codegen_antlr.py — Geração de Código

Visitor que percorre a árvore e emite o Python equivalente, gerenciando indentação automaticamente.

### 4.4 app.py — Servidor Flask

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Serve a interface web |
| `/transpilar` | POST | Recebe código FIN, retorna Python |
| `/executar` | POST | Executa o Python com inputs fornecidos |
| `/testes` | GET | Lista arquivos `.fin` da pasta testes/ |
| `/testes/<nome>` | GET | Retorna conteúdo de um arquivo `.fin` |

---

## 5. Visitor Pattern com ANTLR

A escolha do ANTLR4 permite usar o padrão Visitor para percorrer a árvore. Cada construção da linguagem tem um método próprio, tornando o código mais organizado do que a abordagem manual com `isinstance()`.

```python
# Abordagem manual (sem ANTLR)
def process(node):
    if isinstance(node, If):
        ...
    elif isinstance(node, While):
        ...

# Com ANTLR + Visitor
class CodeGenerator(FINVisitor):
    def visitCmdIf(self, ctx):
        ...
    def visitCmdKun(self, ctx):
        ...
```

Os labels na gramática (`# exprMult`, `# exprAdd`) geram métodos separados automaticamente, facilitando o tratamento de precedência de operadores.

---

## 6. Tabela de Equivalência FIN → Python

| Linguagem FIN | Python gerado |
|---|---|
| `ohj ... lop` | *(sem equivalente direto)* |
| `kok x.` | `x = 0` |
| `des pi.` | `pi = 0.0` |
| `tek nome.` | `nome = ''` |
| `tot ativo.` | `ativo = False` |
| `x := expr.` | `x = expr` |
| `lue(x).` *(x é kok)* | `x = int(input())` |
| `lue(x).` *(x é des)* | `x = float(input())` |
| `lue(x).` *(x é tek)* | `x = input()` |
| `kir("texto").` | `print('texto')` |
| `kir(x).` | `print(x)` |
| `jos (cond) { ... }` | `if cond: ...` |
| `jos (cond) { } muu { }` | `if cond: ... else: ...` |
| `kun (cond) { ... }` | `while cond: ...` |
| `var i de 1 ate 10 { }` | `for i in range(1, 11): ...` |
| `do { } kun (cond).` | `while True: ... if not cond: break` |
| `a ja b` | `a and b` |
| `a tai b` | `a or b` |
| `ei a` | `not a` |
| `totta / vaara` | `True / False` |

---

## 7. Exemplo Completo

**Entrada — calculadora.fin:**

```
ohj
kok a, b, soma.
des media.
kir("Digite o primeiro numero:").
lue(a).
kir("Digite o segundo numero:").
lue(b).
soma := a + b.
media := soma / 2.
kir("Soma:").
kir(soma).
jos (media >= 5) {
    kir("Media suficiente!").
} muu {
    kir("Media insuficiente.").
}
lop
```

**Saída gerada — calculadora.py:**

```python
# Gerado automaticamente pelo transpilador FIN

a = 0
b = 0
soma = 0
media = 0.0

print('Digite o primeiro numero:')
a = int(input())
print('Digite o segundo numero:')
b = int(input())
soma = (a + b)
media = (soma / 2)
print('Soma:')
print(soma)
if (media >= 5):
    print('Media suficiente!')
else:
    print('Media insuficiente.')
```

---

## 8. Tratamento de Erros

| Tipo | Exemplo de mensagem |
|---|---|
| Léxico | `Caractere inválido '@' na linha 3` |
| Sintático | `Linha 5, coluna 8: missing '.' at 'lop'` |
| Semântico | `Linha 7: variável "y" não foi declarada.` |
| Semântico | `Variável "x" já foi declarada.` |
| Semântico | `Linha 3: não é possível atribuir texto à variável "n" do tipo kok.` |

---

## 9. Estrutura do Projeto

```
transpilador-fin/
├── app.py                  ← servidor Flask
├── interface.html          ← interface web
├── antlr/
│   ├── FIN.g4              ← gramática da linguagem FIN
│   ├── FINLexer.py         ← gerado pelo ANTLR
│   ├── FINParser.py        ← gerado pelo ANTLR
│   └── FINVisitor.py       ← gerado pelo ANTLR
├── src/
│   ├── semantic_antlr.py   ← análise semântica (Visitor)
│   ├── codegen_antlr.py    ← geração de código (Visitor)
│   └── main_antlr.py       ← execução via terminal
└── testes/
    ├── 01_tipos_de_dados.fin
    ├── 02_if_else.fin
    ├── 03_while.fin
    ├── 04_for.fin
    ├── 05_do_while.fin
    ├── 06_operadores_logicos.fin
    ├── 07_precedencia.fin
    ├── 08_tabuada.fin
    ├── 09_maior_menor.fin
    └── 10_media_turma.fin
```