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
    """reduce => s : t OR s"""
    pass

def reduce3(state_stack, parse_stack, input_stack):
    """reduce => t : x"""
    pass

def reduce4(state_stack, parse_stack, input_stack):
    """reduce => t : x t"""
    pass

def reduce5(state_stack, parse_stack, input_stack):
    """reduce => x : ( s )"""
    pass

def reduce6(state_stack, parse_stack, input_stack):
    """reduce => x : ( s ) *"""
    pass

def reduce7(state_stack, parse_stack, input_stack):
    """reduce => x : F"""
    pass

def reduce8(state_stack, parse_stack, input_stack):
    """reduce => x : F *"""
    pass

def __acc__(state_stack, parse_stack, input_stack):
    """function of accept"""
    assert state_stack == [ 0, 1 ] and parse_stack == [ 's' ]

def __s__(state):
    """return a shift function to state"""
    def shift(state_stack, parse_stack, input_stack):
        """"shift to state"""
        state_stack.append(state)
        parse_stack.append(input_stack.pop())
    return shift

def __r__(num):
    """return a reduce function of number num"""
    assert 1 <= num <= 8
    reduces = [ None, reduce1, reduce2, reduce3, reduce4, reduce5,
        reduce6, reduce7, reduce8 ]
    return reduces[num]

__action_table__ = (
    { '(' : __s__(4), 'F' : __s__(5), }, # 0
    { '$' : __acc__ }, # 1
    { '|' : __s__(7), '$' : __r__(1) }, # 2
    { '|' : __r__(3), '(' : __s__(4), 'F' : __s__(5), '$' : __r__(3), }, # 3
    { '(' : __s__(4), 'F' : __s__(5) }, # 4
    { '|' : __r__(7), '(' : __r__(7), '*' : __s__(6), 'F' : __r__(7),
        '$' : __r__(7), }, # 5
    { '|' : __r__(8), '(' : __r__(8), 'F' : __r__(8), '$' : __r__(8), }, # 6
    { '(' : __s__(4), 'F' : __s__(5), }, # 7
    { '$' : __r__(2) }, # 8
    { '|' : __r__(4), '$' : __r__(4) }, # 9
    { '|' : __r__(3), '(' : __s__(4), 'F' : __s__(5), '$' : __r__(3), }, # 10
    { ')' : __s__(12) }, # 11
    { '|' : __r__(5), '(' : __r__(5), '*' : __s__(13), 'F' : __r__(5),
        '$' : __r__(5), }, # 12
    { '|' : __r__(6), '(' : __r__(6), 'F' : __r__(6), '$' : __r__(6), }, # 13
    { '|' : __s__(15), ')' : __r__(1) }, # 14
    { '(' : __s__(4), 'F' : __s__(5), }, # 15
    { ')' : __r__(2) }, # 16
    { '|' : __r__(3), '(' : __s__(4), ')' : __r__(3), 'F' : __s__(5), }, # 17
    { '|' : __r__(4), ')' : __r__(4), }, # 18
)

__goto_table__ = (
    { 's' : 1, 't' : 2, 'x' : 3 }, # 0
    {}, # 1
    {}, # 2
    { 't' : 9, 'x' : 10 }, # 3
    { 's' : 11, 't' : 14, 'x' : 17 }, # 4
    {}, # 5
    {}, # 6
    { 's' : 8, 't' : 2, 'x' : 3 }, # 7
    {}, # 8
    {}, # 9
    { 't' : 9, 'x' : 10 }, # 10
    {}, # 11
    {}, # 12
    {}, # 13
    {}, # 14
    { 's' : 16, 't' : 14, 'x' : 17 }, # 15
    {}, # 16
    { 't' : 18, 'x' : 17 }, # 17
    {}, # 18
)

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
    while input_stack:
        __action_table__[state_stack[-1]][input_stack[-1]](
            state_stack, parse_stack, input_stack
        )

def build(pattern):
    """build a state graph based on the pattern"""
    return parse(pattern)
