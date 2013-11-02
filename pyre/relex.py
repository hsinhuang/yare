#!/usr/bin/env python
# coding:utf-8

#pylint: disable=C0103

"""tokenizer for the re implemented in the package"""

import ply.lex as lex

from pyre.fa import EPSILON

# List of token names
tokens = (
   'EPSILON',
   'RVBAR',
   'RSTAR',
   'RLPAREN',
   'RRPAREN',
   'VBAR',
   'STAR',
   'LPAREN',
   'RPAREN',
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

t_VBAR         = r'\|'
t_STAR         = r'\*'
t_LPAREN       = r'\('
t_RPAREN       = r'\)'
t_NORMAL       = r'.'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
