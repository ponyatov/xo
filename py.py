################ parser ################

import sys
import ply.lex  as lex
import ply.yacc as yacc

tokens = [ 'SYM' , 'OP' ]

t_ignore_comment = r'\#.*'
t_ignore  = ' \t\r'
def t_newline(tok):
    r'\n'
    tok.lexer.lineno += 1
    
def t_SYM(tok):
    r'[a-zA-Z0-9_.]+|@gvim|-p'
    return tok
def t_OP(tok):
    r'[\=\@\+\-\*\/\^\[\]]'
    return tok    

def t_error(tok): print tok.lexer,'error',tok

lexer = lex.lex()
lexer.input(sys.stdin.read())
for i in iter(lexer.token,None): print i