#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

from fa import FA

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
        print type(edge)
        self.move.setdefault(edge, [])
        if state not in self.move[edge]:
            self.move[edge].append(state)
        return state

class StateGraph:
    """state graph"""
    def __init__(self, start=None, final=None):
        self.start = start
        self.final = final
    def all_states(self, from_state):
        """all states in the graph from the from_state"""
        alls = [ from_state ]
        for edge in from_state.move:
            for node in from_state.move[edge]:
                if node not in alls:
                    alls.append(node)
            for next_state in from_state.move[edge]:
                for node in self.all_states(next_state):
                    if node not in alls:
                        alls.append(node)
        return alls
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
