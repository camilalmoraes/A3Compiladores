# Transpilador FIN → Python

Transpilador que converte código escrito na **Linguagem FIN** (palavras-chave em finlandês) para **Python 3**.

Desenvolvido para a disciplina de **Teoria da Computação e Compiladores** - Prof. Eduardo Xavier.

---

## Integrantes

- Camila Louzada Moraes
- Nicolle Brasil dos Santos Nery
- Gustavo Burgos Bittencourt Figueiredo
- Diego Amaro Ferreira
- Juan Pablo dos Santos Rodrigues

---

## Tecnologias

| Ferramenta | Uso |
|---|---|
| Python 3.10+ | Linguagem principal |
| ANTLR 4.9.3 | Geração do lexer e parser |
| Flask | Servidor web da interface |
| Java 8+ | Necessário para rodar o ANTLR |

---

## Instalação

```bash
pip install antlr4-python3-runtime==4.9.3
pip install flask
```

---

## Como rodar

### Interface web (recomendado)

```bash
python app.py
```

Acesse `http://localhost:5000` no navegador.

A interface permite:
- Selecionar arquivos `.fin` da pasta `testes/`
- Ver o Python gerado lado a lado
- Executar o código e ver o resultado na tela

### Terminal

```bash
python src/main_antlr.py testes/01_tipos_de_dados.fin
```

A saída é salva com o mesmo nome e extensão `.py`.

```bash
# Especificando arquivo de saída
python src/main_antlr.py meu_programa.fin -o saida.py
```

---

## Estrutura

```
transpilador-fin/
├── app.py               ← servidor Flask
├── interface.html       ← interface web
├── antlr/
│   ├── FIN.g4           ← gramática da linguagem
│   ├── FINLexer.py      ← gerado pelo ANTLR
│   ├── FINParser.py     ← gerado pelo ANTLR
│   └── FINVisitor.py    ← gerado pelo ANTLR
├── src/
│   ├── semantic_antlr.py
│   ├── codegen_antlr.py
│   └── main_antlr.py
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

---

## Exemplo

**Entrada (`soma.fin`):**
```
ohj
kok a, b, soma.
lue(a).
lue(b).
soma := a + b.
kir(soma).
lop
```

**Saída (`soma.py`):**
```python
# Gerado automaticamente pelo transpilador FIN

a = 0
b = 0
soma = 0

a = int(input())
b = int(input())
soma = (a + b)
print(soma)
```

---

## Regenerar o lexer e parser (se necessário)

Caso o arquivo `FIN.g4` seja modificado, rode:

```bash
java -jar C:\antlr\antlr4.jar -Dlanguage=Python3 -visitor antlr/FIN.g4
```