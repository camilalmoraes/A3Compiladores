# ============================================================
#  codegen.py:  Geração de Código Python usando Visitor do ANTLR
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'antlr'))

from FINVisitor import FINVisitor
from FINParser  import FINParser


# Valores padrão por tipo
DEFAULT_VALUE = {
    'kok': '0',
    'des': '0.0',
    'tek': "''",
    'tot': 'False',
}

# Conversão de input por tipo
INPUT_CONV = {
    'kok': 'int(input())',
    'des': 'float(input())',
    'tek': 'input()',
    'tot': 'bool(input())',
}

# Operadores lógicos FIN → Python
LOGIC_OP = {
    'ja':  'and',
    'tai': 'or',
}


class CodeGenerator(FINVisitor):

    def __init__(self, symbols: dict[str, str]):
        self.symbols  = symbols
        self._indent  = 0
        self._lines   = []

    # Saída
    def _emit(self, line: str = ''):
        self._lines.append('    ' * self._indent + line)

    def _indent_in(self):  self._indent += 1
    def _indent_out(self): self._indent -= 1

    def get_code(self) -> str:
        return '\n'.join(self._lines) + '\n'

    # Programa
    def visitProg(self, ctx: FINParser.ProgContext):
        self._emit('# Gerado automaticamente pelo transpilador FIN')
        self._emit()
        for decl in ctx.decl():
            self.visitDecl(decl)
        self._emit()
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        return self.get_code()

    # Declarações
    def visitDecl(self, ctx: FINParser.DeclContext):
        tipo    = ctx.tipo().getText()
        default = DEFAULT_VALUE[tipo]
        for id_token in ctx.ID():
            self._emit(f'{id_token.getText()} = {default}')

    # Comandos
    def visitCmd(self, ctx: FINParser.CmdContext):
        self.visit(ctx.getChild(0))

    def visitCmdAtrib(self, ctx: FINParser.CmdAtribContext):
        nome = ctx.ID().getText()
        expr = self.visitExpr(ctx.expr())
        self._emit(f'{nome} = {expr}')

    def visitCmdLeitura(self, ctx: FINParser.CmdLeituraContext):
        nome = ctx.ID().getText()
        tipo = self.symbols.get(nome, 'tek')
        self._emit(f'{nome} = {INPUT_CONV[tipo]}')

    def visitCmdEscrita(self, ctx: FINParser.CmdEscritaContext):
        expr = self.visitExpr(ctx.expr())
        self._emit(f'print({expr})')

    def visitCmdIf(self, ctx: FINParser.CmdIfContext):
        cond = self.visitCond(ctx.cond())
        self._emit(f'if {cond}:')
        self._indent_in()

        # separa cmds do then e do else pelo token MUU
        cmds      = ctx.cmd()
        muu_index = None
        for i, child in enumerate(ctx.children):
            if hasattr(child, 'symbol') and child.symbol.type == FINParser.MUU:
                muu_index = i
                break

        if muu_index is None:
            # sem else
            for cmd in cmds:
                self.visitCmd(cmd)
            self._indent_out()
        else:
            # conta quantos cmds vêm antes do MUU
            then_count = sum(
                1 for c in ctx.children[:muu_index]
                if isinstance(c, FINParser.CmdContext)
            )
            for cmd in cmds[:then_count]:
                self.visitCmd(cmd)
            self._indent_out()
            self._emit('else:')
            self._indent_in()
            for cmd in cmds[then_count:]:
                self.visitCmd(cmd)
            self._indent_out()

    def visitCmdKun(self, ctx: FINParser.CmdKunContext):
        cond = self.visitCond(ctx.cond())
        self._emit(f'while {cond}:')
        self._indent_in()
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        self._indent_out()

    def visitCmdVar(self, ctx: FINParser.CmdVarContext):
        var   = ctx.ID().getText()
        exprs = ctx.expr()
        start = self.visitExpr(exprs[0])
        end   = self.visitExpr(exprs[1])
        self._emit(f'for {var} in range({start}, {end} + 1):')
        self._indent_in()
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        self._indent_out()

    def visitCmdDoKun(self, ctx: FINParser.CmdDoKunContext):
        cond = self.visitCond(ctx.cond())
        self._emit('while True:')
        self._indent_in()
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        self._emit(f'if not ({cond}): break')
        self._indent_out()

    # Condição
    def visitCond(self, ctx: FINParser.CondContext) -> str:
        if isinstance(ctx, FINParser.CondNaoContext):
            expr = self.visitExpr(ctx.expr(0))
            return f'not {expr}'

        exprs = ctx.expr()
        left  = self.visitExpr(exprs[0])
        right = self.visitExpr(exprs[1])

        if isinstance(ctx, FINParser.CondRelContext):
            op = ctx.opRel().getText()
            return f'{left} {op} {right}'

        if isinstance(ctx, FINParser.CondLogContext):
            op = LOGIC_OP.get(ctx.opLog().getText(), ctx.opLog().getText())
            return f'{left} {op} {right}'

        return f'{left} {right}'

    # Expressões
    def visitExpr(self, ctx) -> str:

        if isinstance(ctx, FINParser.ExprNumContext):
            return ctx.NUM().getText()

        if isinstance(ctx, FINParser.ExprStrContext):
            inner = ctx.STR().getText()[1:-1]   # remove aspas duplas
            return f"'{inner}'"

        if isinstance(ctx, FINParser.ExprTottaContext):
            return 'True'

        if isinstance(ctx, FINParser.ExprVaaraContext):
            return 'False'

        if isinstance(ctx, FINParser.ExprIdContext):
            return ctx.ID().getText()

        if isinstance(ctx, FINParser.ExprParenContext):
            inner = self.visitExpr(ctx.expr())
            return f'({inner})'

        if isinstance(ctx, FINParser.ExprMultContext):
            left  = self.visitExpr(ctx.expr(0))
            op    = ctx.op.text
            right = self.visitExpr(ctx.expr(1))
            return f'({left} {op} {right})'

        if isinstance(ctx, FINParser.ExprAddContext):
            left  = self.visitExpr(ctx.expr(0))
            op    = ctx.op.text
            right = self.visitExpr(ctx.expr(1))
            return f'({left} {op} {right})'

        return ctx.getText()


def generate(tree, symbols: dict[str, str]) -> str:
    return CodeGenerator(symbols).visitProg(tree)
