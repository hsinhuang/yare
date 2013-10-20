#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

from fa import FA, EPSILON

ESCAPE = '\\'
SPECIAL_SYMBOLS = '\\e|*()'

SELECT = 'selection'
CONCAT = 'concatenation'
LOOP   = 'loop'

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

__matched_rparen = {}

def __seeking_rparen(tokens, start_idx):
    """
    return the index of matched right parenthesis in tokens
    of the left parenthesis in `start_idx`
    """
    assert tokens[start_idx] == '('
    tokens_str = ''.join(tokens)
    if tokens_str not in __matched_rparen:
        __matched_rparen.setdefault(tokens_str, {})
    if start_idx not in __matched_rparen[tokens_str]:
        __matched_rparen[tokens_str][start_idx] = \
            __seeking_rparen_noncached(tokens, start_idx)
    return __matched_rparen[tokens_str][start_idx]

def __seeking_rparen_noncached(tokens, start_idx):
    """
    return the index of matched right parenthesis in tokens
    of the left parenthesis in `start_idx`

    this version do not cache
    """
    assert tokens[start_idx] == '('
    start_idx += 1
    while start_idx < len(tokens):
        current = tokens[start_idx]
        if current == ')':
            return start_idx
        if current == '(':
            start_idx = __seeking_rparen(tokens, start_idx)
        start_idx += 1
    return None

def __seeking_vertical_bar(tokens, start_idx):
    """
    return the index of fisrt vertical bar in tokens,
    or None if there is a '(' or ')' before it
    """
    while start_idx < len(tokens):
        current = tokens[start_idx]
        if current == '|':
            return start_idx
        elif current in '()':
            return None
        start_idx += 1
    return None

def __parse(tokens):
    """parse a pattern string to a syntax tree"""
    if not tokens:
        return None
    num_tokens = len(tokens)
    selection = []
    index = 0
    while index < num_tokens:
        current = tokens[index]
        if current == '(':
            rparen_idx = __seeking_rparen(tokens, index)
            if not rparen_idx:
                raise SyntaxError("Parenthesis not matched, ", index)
            if rparen_idx+1 < num_tokens and tokens[rparen_idx+1] == '*':
                rparen_idx += 1
            selection.append(__parse(tokens[index:rparen_idx+1]))
            index = rparen_idx+1
        elif current == ')':
            raise SyntaxError("Parenthesis redundant, ", index)
        elif current == '|':
            raise SyntaxError("Vertical bar not valid, ", index)
        elif current == '*':
            raise SyntaxError("Star not valid, ", index)
        elif current == '\\':
            raise SyntaxError("Backslash not valid, ", index)
        else:
            bar_idx = __seeking_vertical_bar(tokens, index)
            if not bar_idx:


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
