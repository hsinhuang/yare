#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

from fa import FA, EPSILON

ESCAPE = '\\'
SPECIAL_SYMBOLS = '\\e|*()'

class RegEx:
    """Regular Expression based on minimal DFA"""
    def __init__(self, nfa, pattern):
        dfa = nfa.relabel().make_dfa().relabel()
        self.__dfa = dfa.minimize().relabel()
        self.__pattern = pattern

    def match(self, string):
        """
        If `string` matches the regex, then return the string,
        otherwise return None
        """
        if self.__dfa.validate(string):
            return string
        return None

    def pattern(self):
        """getter: pattern"""
        return self.__pattern


def match(regex, string):
    """whether the `string` matches `regex`"""
    return regex.match(string)

def __split(pattern):
    """split pattern string to token list"""
    tokens = []
    in_escape = False

    for char in pattern:
        if in_escape:
            if char in SPECIAL_SYMBOLS:
                tokens.append(ESCAPE+char if char != 'e' else EPSILON)
            else:
                raise SyntaxWarning('escape symbol followed '
                    'by a non-special symbol')
            in_escape = False
        else:
            if char == ESCAPE:
                in_escape = True
            else:
                tokens.append(char)
    return tokens

def __grow_nfa(nfa, tokens, start_index=0):
    """
    grow the given nfa

    params: nfa         - the one should be grew
            tokens      - grow based on the tokens
            start_index - the new part of nfa start from it

    return: (new_nfa, start_node, end_node)
            new_nfa    - new nfa
            start_node - start node of the new nfa
            end_node   - end node of the new nfa
    """
    return nfa, tokens, start_index

def compile(pattern):
    """Compile a regular expression to minimal DFA"""
    tokens = __split(pattern)
    nfa, start, final = __grow_nfa(FA(), tokens, 0)
    nfa.set_start(start).add_final(final)
    return RegEx(nfa, pattern)
