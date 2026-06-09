// ============================================================
//  FIN.g4 Gramática ANTLR4 da Linguagem FIN
//  Transpilador Finlandês → Python
// ============================================================

grammar FIN;

// ── Regra inicial ────────────────────────────────────────────
prog
    : OHJ decl+ cmd+ LOP EOF
    ;

// ── Declarações ──────────────────────────────────────────────
decl
    : tipo ID (',' ID)* '.'
    ;

tipo
    : KOK
    | DES
    | TEK
    | TOT
    ;

// ── Comandos ─────────────────────────────────────────────────
cmd
    : cmdAtrib
    | cmdLeitura
    | cmdEscrita
    | cmdIf
    | cmdKun
    | cmdVar
    | cmdDoKun
    ;

cmdAtrib
    : ID ASSIGN expr '.'
    ;

cmdLeitura
    : LUE '(' ID ')'  '.'
    ;

cmdEscrita
    : KIR '(' expr ')' '.'
    ;

cmdIf
    : JOS '(' cond ')' '{' cmd+ '}' (MUU '{' cmd+ '}')?
    ;

cmdKun
    : KUN '(' cond ')' '{' cmd+ '}'
    ;

cmdVar
    : VAR ID DE expr ATE expr '{' cmd+ '}'
    ;

cmdDoKun
    : DO '{' cmd+ '}' KUN '(' cond ')' '.'
    ;

// ── Condição ─────────────────────────────────────────────────
cond
    : EI expr                   # condNao
    | expr opRel expr           # condRel
    | expr opLog expr           # condLog
    ;

opRel : LT | GT | LE | GE | EQ | NEQ ;
opLog : JA | TAI ;

// ── Expressões (com precedência) ─────────────────────────────
expr
    : expr op=('*' | '/' | '%') expr   # exprMult
    | expr op=('+' | '-') expr         # exprAdd
    | '(' expr ')'                     # exprParen
    | NUM                              # exprNum
    | STR                              # exprStr
    | TOTTA                            # exprTotta
    | VAARA                            # exprVaara
    | ID                               # exprId
    ;

// ══════════════════════════════════════════════════════════════
//  TOKENS — Palavras Reservadas
// ══════════════════════════════════════════════════════════════
OHJ   : 'ohj' ;
LOP   : 'lop' ;
KOK   : 'kok' ;
DES   : 'des' ;
TEK   : 'tek' ;
TOT   : 'tot' ;
JOS   : 'jos' ;
MUU   : 'muu' ;
KUN   : 'kun' ;
VAR   : 'var' ;
DO    : 'do'  ;
LUE   : 'lue' ;
KIR   : 'kir' ;
TOTTA : 'totta' ;
VAARA : 'vaara' ;
JA    : 'ja'  ;
TAI   : 'tai' ;
EI    : 'ei'  ;
DE    : 'de'  ;
ATE   : 'ate' ;

// ── Operadores ───────────────────────────────────────────────
ASSIGN : ':=' ;
LE     : '<=' ;
GE     : '>=' ;
EQ     : '==' ;
NEQ    : '!=' ;
LT     : '<'  ;
GT     : '>'  ;

// ── Literais ─────────────────────────────────────────────────
NUM : [0-9]+ ('.' [0-9]+)? ;
STR : '"' (~["\r\n])* '"' ;
ID  : [a-zA-Z_][a-zA-Z0-9_]* ;

// ── Ignorados ────────────────────────────────────────────────
WS      : [ \t\r\n]+  -> skip ;
COMMENT : '#' ~[\r\n]* -> skip ;
