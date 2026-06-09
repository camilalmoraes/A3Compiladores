# ============================================================
#  semantic.py  —  Análise Semântica usando Visitor do ANTLR
# ============================================================

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'antlr'))

from FINVisitor import FINVisitor
from FINParser  import FINParser


class SemanticError(Exception):
    pass


class SemanticAnalyzer(FINVisitor):

    def __init__(self):
        # tabela de símbolos: nome → tipo ('kok','des','tek','tot')
        self.symbols: dict[str, str] = {}

    # Programa
    def visitProg(self, ctx: FINParser.ProgContext):
        # visita declarações primeiro, depois comandos
        for decl in ctx.decl():
            self.visitDecl(decl)
        for cmd in ctx.cmd():
            self.visitCmd(cmd)

    # Declarações
    def visitDecl(self, ctx: FINParser.DeclContext):
        tipo = ctx.tipo().getText()
        for id_token in ctx.ID():
            nome = id_token.getText()
            if nome in self.symbols:
                raise SemanticError(f'Variável "{nome}" já foi declarada.')
            self.symbols[nome] = tipo

    # Comandos
    def visitCmd(self, ctx: FINParser.CmdContext):
        return self.visit(ctx.getChild(0))

    def visitCmdAtrib(self, ctx: FINParser.CmdAtribContext):
        nome = ctx.ID().getText()
        linha = ctx.ID().getSymbol().line
        self._check_declared(nome, linha)
        self.visitExpr(ctx.expr())
        self._check_assign_type(nome, ctx.expr(), linha)

    def visitCmdLeitura(self, ctx: FINParser.CmdLeituraContext):
        nome = ctx.ID().getText()
        linha = ctx.ID().getSymbol().line
        self._check_declared(nome, linha)

    def visitCmdEscrita(self, ctx: FINParser.CmdEscritaContext):
        self.visitExpr(ctx.expr())

    def visitCmdIf(self, ctx: FINParser.CmdIfContext):
        self.visitCond(ctx.cond())
        for cmd in ctx.cmd():
            self.visitCmd(cmd)

    def visitCmdKun(self, ctx: FINParser.CmdKunContext):
        self.visitCond(ctx.cond())
        for cmd in ctx.cmd():
            self.visitCmd(cmd)

    def visitCmdVar(self, ctx: FINParser.CmdVarContext):
        nome = ctx.ID().getText()
        linha = ctx.ID().getSymbol().line
        self._check_declared(nome, linha)
        if self.symbols.get(nome) != 'kok':
            raise SemanticError(
                f'Linha {linha}: variável de controle "{nome}" deve ser do tipo kok (inteiro).'
            )
        for expr in ctx.expr():
            self.visitExpr(expr)
        for cmd in ctx.cmd():
            self.visitCmd(cmd)

    def visitCmdDoKun(self, ctx: FINParser.CmdDoKunContext):
        for cmd in ctx.cmd():
            self.visitCmd(cmd)
        self.visitCond(ctx.cond())

    # Condição
    def visitCond(self, ctx: FINParser.CondContext):
        for expr in ctx.expr():
            self.visitExpr(expr)

    # Expressões
    def visitExpr(self, ctx):
        # ExprId — verifica se variável foi declarada
        if isinstance(ctx, FINParser.ExprIdContext):
            nome = ctx.ID().getText()
            linha = ctx.ID().getSymbol().line
            self._check_declared(nome, linha)
            return

        # Desce nos filhos recursivamente
        for i in range(ctx.getChildCount()):
            child = ctx.getChild(i)
            if isinstance(child, FINParser.ExprContext.__mro__[0]):
                self.visitExpr(child)
            elif hasattr(child, 'expr'):
                for e in child.expr():
                    self.visitExpr(e)

    # Helpers
    def _check_declared(self, nome: str, linha: int):
        if nome not in self.symbols:
            raise SemanticError(
                f'Linha {linha}: variável "{nome}" não foi declarada.'
            )

    def _check_assign_type(self, nome: str, expr_ctx, linha: int):
        tipo = self.symbols[nome]
        texto = expr_ctx.getText()

        if isinstance(expr_ctx, FINParser.ExprStrContext) and tipo != 'tek':
            raise SemanticError(
                f'Linha {linha}: não é possível atribuir texto à variável "{nome}" do tipo {tipo}.'
            )
        if isinstance(expr_ctx, (FINParser.ExprTottaContext, FINParser.ExprVaaraContext)) and tipo != 'tot':
            raise SemanticError(
                f'Linha {linha}: não é possível atribuir booleano à variável "{nome}" do tipo {tipo}.'
            )


def analyze(tree, parser):
    sa = SemanticAnalyzer()
    sa.visitProg(tree)
    return sa.symbols
