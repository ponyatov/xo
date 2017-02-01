################ Sym tree ################

class Sym:
    tag = 'sym'
    def __init__(self, V): self.val = V ; self.nest = [] ; self.attr = {}
    def __iadd__(self,o): return self.push(o)
    def push(self,o): self.nest.append(o) ; return self
    def __repr__(self): return self.head()
    def head(self): return '<%s:%s>' % (self.tag, self.val)
    def pad(self, n): return '\t'*n
    def dump(self, depth=0):
        S = '\n' + self.pad(depth) + self.head()
        for i in self.nest: S += i.dump(depth + 1)
        return S
class Op(Sym):
    tag = 'op'
class Vector(Sym):
    tag = 'vector'
    def __init__(self): Sym.__init__(self, '')
    def head(self): return '[]'
class Lambda(Sym):
    tag = 'lambda'
    def __init__(self): Sym.__init__(self, '')

################ parser ################

import sys
import ply.lex  as lex
import ply.yacc as yacc

tokens = [ 'SYM' , 'OP' ,
           'LQ' , 'RQ' , 'LC' , 'RC' ,
           'EQ' , 'AT' , 'COLON' ]

t_ignore_comment = r'\#.*'
t_ignore = ' \t\r'
def t_newline(tok):
    r'\n'
    tok.lexer.lineno += 1
    
def t_SYM(tok):
    r'[a-zA-Z0-9_.]+|@gvim|-p'
    tok.value = Sym(tok.value) ; return tok
def t_LQ(tok):
    r'\['
    tok.value = Op(tok.value) ; return tok
def t_RQ(tok):
    r'\]'
    tok.value = Op(tok.value) ; return tok
def t_LC(tok):
    r'\{'
    tok.value = Op(tok.value) ; return tok
def t_RC(tok):
    r'\}'
    tok.value = Op(tok.value) ; return tok
def t_EQ(tok):
    r'\='
    tok.value = Op(tok.value) ; return tok
def t_AT(tok):
    r'\@'
    tok.value = Op(tok.value) ; return tok
def t_COLON(tok):
    r'\:'
    tok.value = Op(tok.value) ; return tok
def t_OP(tok):
    r'[\+\-\*\/\^]'
    tok.value = Op(tok.value) ; return tok
    
def p_REPL_empty(p):
    ' REPL : '
def p_REPL_recur(p):
    ' REPL : REPL ex '
    print p[2].dump()

def p_ex_scalar(p):
    ' ex  : scalar '
    p[0] = p[1]
def p_scalar(p):
    ''' scalar  : SYM
                | OP    '''
    p[0] = p[1]

def p_ex_eq(p):
    ' ex : ex EQ ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]
def p_ex_at(p):
    ' ex : ex AT ex '
    p[0] = p[2] ; p[0] += p[1] ; p[0] += p[3]

def p_ex_vector(p):
    ' ex : LQ vector RQ '
    p[0] = p[2]
def p_vector_new(p):
    ' vector : '
    p[0] = Vector()
def p_vector_item(p):
    ' vector : vector ex '
    p[0] = p[1].push(p[2])

def p_ex_lambda(p):
    ' ex : LC lambda RC '
    p[0] = p[2]
def p_lambda_new(p):
    ' lambda : '
    p[0] = Lambda()
def p_lambda_new(p):
    ' lambda : '
    p[0] = Lambda()
 
def t_error(t): print 'lexer/error', t
def p_error(p): print 'parse/error', p

lexer = lex.lex()
parser = yacc.yacc(debug=False, write_tables=False)
parser.parse(sys.stdin.read())
