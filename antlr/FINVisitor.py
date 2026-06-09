# Generated from FIN.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FINParser import FINParser
else:
    from FINParser import FINParser

class FINVisitor(ParseTreeVisitor):

    def visitProg(self, ctx:FINParser.ProgContext):
        return self.visitChildren(ctx)

    def visitDecl(self, ctx:FINParser.DeclContext):
        return self.visitChildren(ctx)

    def visitTipo(self, ctx:FINParser.TipoContext):
        return self.visitChildren(ctx)

    def visitCmd(self, ctx:FINParser.CmdContext):
        return self.visitChildren(ctx)

    def visitCmdAtrib(self, ctx:FINParser.CmdAtribContext):
        return self.visitChildren(ctx)

    def visitCmdLeitura(self, ctx:FINParser.CmdLeituraContext):
        return self.visitChildren(ctx)

    def visitCmdEscrita(self, ctx:FINParser.CmdEscritaContext):
        return self.visitChildren(ctx)

    def visitCmdIf(self, ctx:FINParser.CmdIfContext):
        return self.visitChildren(ctx)

    def visitCmdKun(self, ctx:FINParser.CmdKunContext):
        return self.visitChildren(ctx)

    def visitCmdVar(self, ctx:FINParser.CmdVarContext):
        return self.visitChildren(ctx)

    def visitCmdDoKun(self, ctx:FINParser.CmdDoKunContext):
        return self.visitChildren(ctx)

    def visitCondNao(self, ctx:FINParser.CondNaoContext):
        return self.visitChildren(ctx)

    def visitCondRel(self, ctx:FINParser.CondRelContext):
        return self.visitChildren(ctx)

    def visitCondLog(self, ctx:FINParser.CondLogContext):
        return self.visitChildren(ctx)

    def visitOpRel(self, ctx:FINParser.OpRelContext):
        return self.visitChildren(ctx)

    def visitOpLog(self, ctx:FINParser.OpLogContext):
        return self.visitChildren(ctx)

    def visitExprParen(self, ctx:FINParser.ExprParenContext):
        return self.visitChildren(ctx)

    def visitExprTotta(self, ctx:FINParser.ExprTottaContext):
        return self.visitChildren(ctx)

    def visitExprStr(self, ctx:FINParser.ExprStrContext):
        return self.visitChildren(ctx)

    def visitExprAdd(self, ctx:FINParser.ExprAddContext):
        return self.visitChildren(ctx)

    def visitExprVaara(self, ctx:FINParser.ExprVaaraContext):
        return self.visitChildren(ctx)

    def visitExprId(self, ctx:FINParser.ExprIdContext):
        return self.visitChildren(ctx)

    def visitExprMult(self, ctx:FINParser.ExprMultContext):
        return self.visitChildren(ctx)

    def visitExprNum(self, ctx:FINParser.ExprNumContext):
        return self.visitChildren(ctx)

del FINParser