#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

from pyre.fa import FA

class State:
    """state"""
    count = 0
    def __init__(self):
        self.name = State.count
        self.move = {}
        State.count += 1
    def __eq__(self, state):
        assert state.__class__ == State
        return self.name == state.name
    def link(self, state, edge):
        """link to state via edge"""
        self.move.setdefault(edge, [])
        if state not in self.move[edge]:
            self.move[edge].append(state)
        return state

class StateGraph:
    """state graph"""
    def __init__(self, start=None, final=None):
        self.start = start
        self.final = final
        self.__all_states = []
    def all_states(self, start):
        """return all states in the graph from the start state"""
        if start in self.__all_states:
            return self.__all_states
        self.__all_states.append(start)
        for edge in start.move:
            for next_state in start.move[edge]:
                self.all_states(next_state)
        return self.__all_states
    def make_nfa(self):
        """make NFA from the state graph"""
        nfa = FA()
        for current in self.all_states(self.start):
            for edge in current.move:
                for next_node in current.move[edge]:
                    nfa.connect(current.name, next_node.name, edge)
        nfa.set_start(self.start.name)
        nfa.add_final(self.final.name)
        return nfa

class RegEx:
    """Regular Expression based on minimal DFA"""
    def __init__(self, nfa, pattern, dfa=False):
        self.__fa = nfa.make_dfa().minimize().relabel() if dfa else nfa
        self.__pattern = pattern

    def match(self, string):
        """
        If `string` matches the regex, then return the string,
        otherwise return None
        """
        if self.__fa.validate(string):
            return True
        return False

    def pattern(self):
        """getter: pattern"""
        return self.__pattern

    def match_prefix(self, string):
        """
        return the maximum index that makes self.match(string[:index])
        True
        """
        pass

def compile(pattern, dfa=True):
    """compile a pattern to RegEx"""
    from pyre.reyacc import build
    try:
        graph = build(pattern)
        if not graph:
            raise SyntaxError()
    except SyntaxError, error:
        if not error.args:
            raise SyntaxError("pattern `%s` cannot be parsed" % pattern)
        else:
            raise error
    nfa = graph.make_nfa()
    return RegEx(nfa, pattern, dfa)

def match(regex, string):
    """
    If `string` matches the regex, then return the string,
    otherwise return None
    """
    return regex.match(string)
