#!/usr/bin/env python
# coding:utf-8

#pylint: disable=C0103

"""parser for the re implemented in the package"""

import ply.yacc as yacc

from pyre.relex import tokens

from pyre.regex import State, StateGraph
from pyre.fa import EPSILON

# Get the token map from the lexer

def p_re_termvre(p):
    're : terms VBAR re'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(p[1].start, EPSILON)
    s0.link(p[3].start, EPSILON)
    p[1].final.link(s1, EPSILON)
    p[3].final.link(s1, EPSILON)

def p_re_terms(p):
    're : terms'
    p[0] = p[1]

def p_re_termre(p):
    'terms : term terms'
    p[1].final.link(p[2].start, EPSILON)
    p[0] = StateGraph(p[1].start, p[2].final)

def p_re_term(p):
    'terms : term'
    p[0] = p[1]

def p_term_res(p):
    'term : LPAREN re RPAREN STAR'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(p[2].start, EPSILON)
    s0.link(s1, EPSILON)
    p[2].final.link(s1, EPSILON)
    p[2].final.link(s0, EPSILON)

def p_term_re(p):
    'term : LPAREN re RPAREN'
    p[0] = p[2]

def p_term_factors(p):
    'term : factor STAR'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(p[1].start, EPSILON)
    s0.link(s1, EPSILON)
    p[1].final.link(s1, EPSILON)
    p[1].final.link(s0, EPSILON)

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_epsilon(p):
    'factor : EPSILON'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(s1, p[1])

def p_factor_rstar(p):
    'factor : RSTAR'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(s1, p[1])

def p_factor_rlparen(p):
    'factor : RLPAREN'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(s1, p[1])

def p_factor_rrparen(p):
    'factor : RRPAREN'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(s1, p[1])

def p_factor_rvbar(p):
    'factor : RVBAR'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(s1, p[1])

def p_factor_normal(p):
    'factor : NORMAL'
    s0 = State()
    s1 = State()
    p[0] = StateGraph(s0, s1)
    s0.link(s1, p[1])

# Error rule for syntax errors
def p_error(p):
    print "Syntax error in input:", p

# Build the parser
parser = yacc.yacc()

def build(pattern):
    """build a state graph based on the pattern"""
    return parser.parse(pattern)
