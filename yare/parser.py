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
        s0 = State()
        s1 = State()
        s0.link(s1, self.__value__)
        self.graph = StateGraph(s0, s1)
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

__goto_table__ = (
    { 's' : 1, 't' : 2, 'x' : 3 }, # 0
    {}, # 1
    {}, # 2
    { 't' : 7, 'x' : 8 }, # 3
    { 's' : 9, 't' : 10, 'x' : 11 }, # 4
    {}, # 5
    { 's' : 15, 't' : 2, 'x' : 3 }, # 6
    {}, # 7
    { 't' : 7, 'x' : 3 }, # 8
    {}, # 9
    {}, # 10
    { 't' : 18, 'x' : 11 }, # 11
    { 's' : 19, 't' : 10, 'x' : 11 }, # 12
    {}, # 13
    {}, # 14
    {}, # 15
    {}, # 16
    { 's' : 22, 't' : 10, 'x' : 11 }, # 17
    {}, # 18
    {}, # 19
    {}, # 20
    {}, # 21
    {}, # 22
    {}, # 23
    {}, # 24
)

def reduce1(state_stack, parse_stack, input_stack):
    """reduce => s : t"""
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == 't'
    state_stack.append(__goto_table__[state_stack[-1]]['s'])
    p0 = Elem('s', 's', 's', p1.offset())
    p0.graph = p1.graph
    parse_stack.append(p0)

def reduce2(state_stack, parse_stack, input_stack):
    """reduce => s : t | s"""
    state_stack.pop()
    p3 = parse_stack.pop()
    assert p3.lexical_unit() == 's'
    state_stack.pop()
    p2 = parse_stack.pop()
    assert p2.lexical_unit() == '|'
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == 't'
    state_stack.append(__goto_table__[state_stack[-1]]['s'])
    p0 = Elem('s', 's', 's', p1.offset())
    s0 = State()
    s1 = State()
    p0.graph = StateGraph(s0, s1)
    s0.link(p1.graph.start, EPSILON)
    s0.link(p3.graph.start, EPSILON)
    p1.graph.final.link(s1, EPSILON)
    p3.graph.final.link(s1, EPSILON)
    parse_stack.append(p0)

def reduce3(state_stack, parse_stack, input_stack):
    """reduce => t : x"""
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == 'x'
    state_stack.append(__goto_table__[state_stack[-1]]['t'])
    p0 = Elem('t', 't', 't', p1.offset())
    p0.graph = p1.graph
    parse_stack.append(p0)

def reduce4(state_stack, parse_stack, input_stack):
    """reduce => t : x t"""
    state_stack.pop()
    p2 = parse_stack.pop()
    assert p2.lexical_unit() == 't'
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == 'x'
    state_stack.append(__goto_table__[state_stack[-1]]['t'])
    p0 = Elem('t', 't', 't', p1.offset())
    p1.graph.final.link(p2.graph.start, EPSILON)
    p0.graph = StateGraph(p1.graph.start, p2.graph.final)
    parse_stack.append(p0)

def reduce5(state_stack, parse_stack, input_stack):
    """reduce => x : ( s )"""
    state_stack.pop()
    p3 = parse_stack.pop()
    assert p3.lexical_unit() == ')'
    state_stack.pop()
    p2 = parse_stack.pop()
    assert p2.lexical_unit() == 's'
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == '('
    state_stack.append(__goto_table__[state_stack[-1]]['x'])
    p0 = Elem('x', 'x', 'x', p1.offset())
    p0.graph = p2.graph
    parse_stack.append(p0)

def reduce6(state_stack, parse_stack, input_stack):
    """reduce => x : ( s ) *"""
    state_stack.pop()
    p4 = parse_stack.pop()
    assert p4.lexical_unit() == '*'
    state_stack.pop()
    p3 = parse_stack.pop()
    assert p3.lexical_unit() == ')'
    state_stack.pop()
    p2 = parse_stack.pop()
    assert p2.lexical_unit() == 's'
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == '('
    state_stack.append(__goto_table__[state_stack[-1]]['x'])
    p0 = Elem('x', 'x', 'x', p1.offset())
    s0 = State()
    s1 = State()
    p0.graph = StateGraph(s0, s1)
    s0.link(p2.graph.start, EPSILON)
    s0.link(s1, EPSILON)
    p2.graph.final.link(s1, EPSILON)
    p2.graph.final.link(s0, EPSILON)
    parse_stack.append(p0)

def reduce7(state_stack, parse_stack, input_stack):
    """reduce => x : F"""
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == 'F'
    state_stack.append(__goto_table__[state_stack[-1]]['x'])
    p0 = Elem('x', 'x', 'x', p1.offset())
    p0.graph = p1.graph
    parse_stack.append(p0)

def reduce8(state_stack, parse_stack, input_stack):
    """reduce => x : F *"""
    state_stack.pop()
    p2 = parse_stack.pop()
    assert p2.lexical_unit() == '*'
    state_stack.pop()
    p1 = parse_stack.pop()
    assert p1.lexical_unit() == 'F'
    state_stack.append(__goto_table__[state_stack[-1]]['x'])
    p0 = Elem('x', 'x', 'x', p1.offset())
    s0 = State()
    s1 = State()
    p0.graph = StateGraph(s0, s1)
    s0.link(p1.graph.start, EPSILON)
    s0.link(s1, EPSILON)
    p1.graph.final.link(s1, EPSILON)
    p1.graph.final.link(s0, EPSILON)
    parse_stack.append(p0)

def __acc__(state_stack, parse_stack, input_stack):
    """function of accept"""
    assert state_stack == [ 0, 1 ] and len(parse_stack) == 1 and \
        parse_stack[0].lexical_unit() == 's'
    input_stack.pop()

def __s__(state):
    """return a shift function to state"""
    def shift(state_stack, parse_stack, input_stack):
        """shift to state"""
        state_stack.append(state)
        parse_stack.append(input_stack.pop())
    shift.__doc__ = shift.__doc__ + ' %d' % state
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
    { '|' : __s__(6), '$' : __r__(1) }, # 2
    { '(' : __s__(4), 'F' : __s__(5), '$' : __r__(3), '|' : __r__(3) }, # 3
    { '(' : __s__(12), 'F' : __s__(13) }, # 4
    { '*' : __s__(14), '$' : __r__(7), '|' : __r__(7), '(' : __r__(7),
        'F' : __r__(7) }, # 5
    { '(' : __s__(4), 'F' : __s__(5) }, # 6
    { '$' : __r__(4), '|' : __r__(4) }, # 7
    { '(' : __s__(4), 'F' : __s__(5), '$' : __r__(3), '|' : __r__(3) }, # 8
    { ')' : __s__(16) }, # 9
    { '|' : __s__(17), ')' : __r__(1) }, # 10
    { '(' : __s__(12), 'F' : __s__(13), '|' : __r__(3), ')' : __r__(3) }, # 11
    { '(' : __s__(12), 'F' : __s__(13) }, # 12
    { '*' : __s__(20), '|' : __r__(7), '(' : __r__(7), ')' : __r__(7),
        'F' : __r__(7) }, # 13
    { '$' : __r__(8), '|' : __r__(8), '(' : __r__(8), 'F' : __r__(8) }, # 14
    { '$' : __r__(2) }, # 15
    { '*' : __s__(21), '(' : __r__(5), 'F' : __r__(5), '$' : __r__(5),
        '|' : __r__(5) }, # 16
    { '(' : __s__(12), 'F' : __s__(13) }, # 17
    { '|' : __r__(4), ')' : __r__(4) }, # 18
    { ')' : __s__(23) }, # 19
    { '|' : __r__(8), '(' : __r__(8), ')' : __r__(8), 'F' : __r__(8) }, # 20
    { '$' : __r__(6), '|' : __r__(6), '(' : __r__(6), 'F' : __r__(6) }, # 21
    { ')' : __r__(2) }, # 22
    { '*' : __s__(24), '|' : __r__(5), '(' : __r__(5), ')' : __r__(5),
        'F' : __r__(5) }, # 23
    { '|' : __r__(6), '(' : __r__(6), ')' : __r__(6), 'F' : __r__(6) }, # 24
)

def parse(re_str):
    """main function to parse re string"""
    istream = ReStream(re_str)
    tokens = list(istream.next())
    __end__ = Elem(__END__, '', __END__, istream.offset())
    tokens.append(__end__)
    input_stack = list(reversed(tokens))
    state_stack = [ 0 ]
    parse_stack = []
    while input_stack:
        ss_top, is_top = state_stack[-1], input_stack[-1]
        if is_top.lexical_unit() not in __action_table__[ss_top]:
            raise SyntaxError(
                'unexpected %s in column %d' % \
                    (is_top.value() if is_top.value() != __END__
                        else 'line ending',
                        is_top.offset())
            )
        __action_table__[ss_top][is_top.lexical_unit()](
            state_stack, parse_stack, input_stack
        )
    return parse_stack[0].graph

def build(pattern):
    """build a state graph based on the pattern"""
    return parse(pattern)
