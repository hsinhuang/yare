#!/usr/bin/env python
# coding:utf-8

"""a LR(1) Parser of regular expression string"""

from fa import EPSILON

from regex import State, StateGraph

__END__ = '$'

class Elem:
    """an element in regular expression"""
    def __init__(self, lexical, raw_str, value, offset):
        self.__lexical__ = lexical
        self.__raw_str__ = raw_str
        self.__value__ = value
        self.__offset__ = offset
    def __str__(self):
        return '`%s`, at column %d, of type %s' % \
            (self.__value__, self.__offset__, self.__lexical__)
    def lexical_unit(self):
        """get the lexical unit of this element"""
        return self.__lexical__
    def offset(self):
        """get the offset of this element in the re string"""
        return self.__offset__
    def value(self):
        """get the value of this elem"""
        return self.__value__

class ReStream:
    """input stream of re string"""
    SPEC_SYM = { '|', '*', '(', ')', }
    ESCAPE_SYM = { '\\e' : EPSILON, '\|' : '|', '\*' : '*',
        '\(' : '(', '\)' : ')', '\\\\' : '\\', }
    def __init__(self, string):
        self.__string__ = string
        self.__offset__ = 0
    def __iter__(self):
        return self
    def next(self):
        """get next element"""
        while self.__string__:
            next_elem = self.__string__[0]
            lexical = 'F'
            if next_elem != '\\':
                self.__string__ = self.__string__[1:]
                if next_elem in ReStream.SPEC_SYM:
                    lexical = next_elem
                elem_value = next_elem
            else:
                next_elem = self.__string__[:2]
                self.__string__ = self.__string__[2:]
                if next_elem not in ReStream.ESCAPE_SYM:
                    raise SyntaxWarning(
                        '`%s` escaped invalid character' % next_elem
                        )
                elem_value = ReStream.ESCAPE_SYM[next_elem]
            yield Elem(lexical, next_elem, elem_value, self.__offset__)
            self.__offset__ += 1
    def has_next(self):
        """whether the stream has any string remaining"""
        return self.__string__
    def offset(self):
        """getter : offset in total"""
        return self.__offset__

def reduce1(state_stack, parse_stack, input_stack):
    """reduce => s : t"""
    pass

def reduce2(state_stack, parse_stack, input_stack):
    """reduce => t OR s"""
    pass

def parse(re_str):
    """main function to parse re string"""
    istream = ReStream(re_str)
    tokens = list(istream.next())
    __end__ = Elem(__END__, '', __END__, istream.offset())
    tokens.append(__end__)
    input_stack = list(reversed(tokens))
    for elem in input_stack:
        print elem
    state_stack = [ 0 ]
    parse_stack = []
    # while True:
    #     pass

def build(pattern):
    """build a state graph based on the pattern"""
    return parse(pattern)
