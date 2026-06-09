# Generated from FIN.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .FINParser import FINParser
else:
    from FINParser import FINParser

class FINListener(ParseTreeListener):

    def enterProg(self, ctx:FINParser.ProgContext):
        pass

    def exitProg(self, ctx:FINParser.ProgContext):
        pass

    def enterDecl(self, ctx:FINParser.DeclContext):
        pass

    def exitDecl(self, ctx:FINParser.DeclContext):
        pass

    def enterTipo(self, ctx:FINParser.TipoContext):
        pass

    def exitTipo(self, ctx:FINParser.TipoContext):
        pass

    def enterCmd(self, ctx:FINParser.CmdContext):
        pass

    def exitCmd(self, ctx:FINParser.CmdContext):
        pass

    def enterCmdAtrib(self, ctx:FINParser.CmdAtribContext):
        pass

    def exitCmdAtrib(self, ctx:FINParser.CmdAtribContext):
        pass

    def enterCmdLeitura(self, ctx:FINParser.CmdLeituraContext):
        pass

    def exitCmdLeitura(self, ctx:FINParser.CmdLeituraContext):
        pass

    def enterCmdEscrita(self, ctx:FINParser.CmdEscritaContext):
        pass

    def exitCmdEscrita(self, ctx:FINParser.CmdEscritaContext):
        pass

    def enterCmdIf(self, ctx:FINParser.CmdIfContext):
        pass

    def exitCmdIf(self, ctx:FINParser.CmdIfContext):
        pass

    def enterCmdKun(self, ctx:FINParser.CmdKunContext):
        pass

    def exitCmdKun(self, ctx:FINParser.CmdKunContext):
        pass

    def enterCmdVar(self, ctx:FINParser.CmdVarContext):
        pass

    def exitCmdVar(self, ctx:FINParser.CmdVarContext):
        pass

    def enterCmdDoKun(self, ctx:FINParser.CmdDoKunContext):
        pass

    def exitCmdDoKun(self, ctx:FINParser.CmdDoKunContext):
        pass

    def enterCondNao(self, ctx:FINParser.CondNaoContext):
        pass

    def exitCondNao(self, ctx:FINParser.CondNaoContext):
        pass

    def enterCondRel(self, ctx:FINParser.CondRelContext):
        pass

    def exitCondRel(self, ctx:FINParser.CondRelContext):
        pass

    def enterCondLog(self, ctx:FINParser.CondLogContext):
        pass

    def exitCondLog(self, ctx:FINParser.CondLogContext):
        pass

    def enterOpRel(self, ctx:FINParser.OpRelContext):
        pass

    def exitOpRel(self, ctx:FINParser.OpRelContext):
        pass

    def enterOpLog(self, ctx:FINParser.OpLogContext):
        pass

    def exitOpLog(self, ctx:FINParser.OpLogContext):
        pass

    def enterExprParen(self, ctx:FINParser.ExprParenContext):
        pass

    def exitExprParen(self, ctx:FINParser.ExprParenContext):
        pass

    def enterExprTotta(self, ctx:FINParser.ExprTottaContext):
        pass

    def exitExprTotta(self, ctx:FINParser.ExprTottaContext):
        pass

    def enterExprStr(self, ctx:FINParser.ExprStrContext):
        pass

    def exitExprStr(self, ctx:FINParser.ExprStrContext):
        pass

    def enterExprAdd(self, ctx:FINParser.ExprAddContext):
        pass

    def exitExprAdd(self, ctx:FINParser.ExprAddContext):
        pass

    def enterExprVaara(self, ctx:FINParser.ExprVaaraContext):
        pass

    def exitExprVaara(self, ctx:FINParser.ExprVaaraContext):
        pass

    def enterExprId(self, ctx:FINParser.ExprIdContext):
        pass

    def exitExprId(self, ctx:FINParser.ExprIdContext):
        pass

    def enterExprMult(self, ctx:FINParser.ExprMultContext):
        pass

    def exitExprMult(self, ctx:FINParser.ExprMultContext):
        pass

    def enterExprNum(self, ctx:FINParser.ExprNumContext):
        pass

    def exitExprNum(self, ctx:FINParser.ExprNumContext):
        pass

del FINParser