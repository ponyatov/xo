################ Sym tree ################

class Sym:
    tag = 'sym'
    def __init__(self, V): self.val = V
    def __repr__(self): return self.head()
    def head(self): return '<%s:%s>' % (self.tag, self.val)
class Op(Sym):
    tag = 'op'

################ parser ################

import sys
import ply.lex  as lex
import ply.yacc as yacc

tokens = [ 'SYM' , 'OP' ]

t_ignore_comment = r'\#.*'
t_ignore = ' \t\r'
def t_newline(tok):
    r'\n'
    tok.lexer.lineno += 1
    
def t_SYM(tok):
    r'[a-zA-Z0-9_.]+|@gvim|-p'
    tok.value = Sym(tok.value) ; return tok
def t_OP(tok):
    r'[\=\@\+\-\*\/\^\[\]]'
    tok.value = Op(tok.value) ; return tok

def t_error(tok): print tok.lexer, 'error', tok

lexer = lex.lex()
lexer.input(sys.stdin.read())
for i in iter(lexer.token, None): print i
