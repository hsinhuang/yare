#!/usr/bin/env python
# coding:utf-8

#pylint: disable=C0103

"""tokenizer for the re implemented in the package"""

import ply.lex as lex

from fa import EPSILON

# List of token names
tokens = (
   'EPSILON',
   'RVBAR',
   'RSTAR',
   'RLPAREN',
   'RRPAREN',
   'RSLASH',
   'VBAR',
   'STAR',
   'LPAREN',
   'RPAREN',
   'NEWLINE',
   'NORMAL'
)

# Regular expression rules for simple tokens
def t_EPSILON(t):
    r'\\e'
    t.value = EPSILON
    return t

def t_RVBAR(t):
    r'\\\|'
    t.value = '|'
    return t

def t_RSTAR(t):
    r'\\\*'
    t.value = '*'
    return t

def t_RLPAREN(t):
    r'\\\('
    t.value = '('
    return t

def t_RRPAREN(t):
    r'\\\)'
    t.value = ')'
    return t

def t_RSLASH(t):
    r'\\\\'
    t.value = '\\'
    return t

t_VBAR         = r'\|'
t_STAR         = r'\*'
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_NEWLINE      = r'\n'
t_NORMAL       = r'.'

# Error handling rule
def t_error(t):
    raise SyntaxError("Illegal character '%s'" % t.value[0])

# Build the lexer
lexer = lex.lex(optimize=1, debug=0, lextab='')
