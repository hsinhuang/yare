#!/usr/bin/env python
# coding:utf-8

"""a LR(1) Parser of regular expression string"""

from fa import EPSILON

from regex import State, StateGraph

class ReStream:
    """input stream of re string"""
    SPEC_SYM = { '|' : 0, '*' : 1, '(' : 2, ')' : 3, }
    ESCAPE_SYM = { '\\e' : EPSILON, '\|' : '|', '\*' : '*',
        '\(' : '(', '\)' : ')', '\\\\' : '\\', }
    def __init__(self, string):
        self.__string__ = string
    def __iter__(self):
        return self
    def next(self):
        """get next element"""
        while self.__string__:
            next_elem = self.__string__[0]
            if next_elem != '\\':
                self.__string__ = self.__string__[1:]
                if next_elem in ReStream.SPEC_SYM:
                    next_elem = ReStream.SPEC_SYM[next_elem]
            else:
                next_elem = self.__string__[:2]
                self.__string__ = self.__string__[2:]
                if next_elem not in ReStream.ESCAPE_SYM:
                    raise SyntaxWarning(
                        '`%s` escaped invalid character' % next_elem
                        )
                next_elem = ReStream.ESCAPE_SYM[next_elem]
            yield next_elem
    def has_next(self):
        """whether the stream has any string remaining"""
        return self.__string__

def parse(re_str):
    """main function to parse re string"""
    istream = ReStream(re_str)
    tokens = list(istream.next())
    return tokens

def build(pattern):
    """build a state graph based on the pattern"""
    return parse(pattern)
