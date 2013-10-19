#!/usr/bin/env python
# coding:utf-8

"""Non-deterministic Finite Automata"""

EPSILON = r'\0'

class NFA:
    """
    Non-deterministic Finite Automata

    EPSILON indicates epsilon
    """
    def __init__(self):
        self.acceptable = set()
        self.nodes = set()
        self.map = {}
        self.start = None
        self.finals = []

    def connect(self, from_node, to_node, edge):
        """
        >>> fa = FA()
        >>> fa.connect(0, 1, 'a')
        self.map = { 0: { 'a': [1] } }
        >>> fa.connect(0, 2, 'a').connect(1, 2, 'b')
        self.map = { 0: { 'a': [1, 2] },
                     1: { 'b': [2] } }
        """
        self.map.setdefault(from_node, {})
        self.map[from_node].setdefault(edge, [])
        self.map[from_node][edge].append(to_node)
        self.acceptable.add(edge)
        self.nodes.add(from_node)
        self.nodes.add(to_node)
        return self

    def epsilon_closure(self, node):
        """
        return the epsilon closure of the given node
        """
        if node not in self.nodes:
            return None
        closure = []
        if EPSILON in self.map[node]:
            closure += self.map[node][EPSILON]
        new_closure = closure
        for clos in closure:
            if self.epsilon_closure(clos):
                new_closure += self.epsilon_closure(clos)
        return new_closure

    def validate(self, edges):
        """
        validate if a string can be accepted by the NFA

        `edges` can be a string while all the edges of the NFA
        is characters

        return the reachable finals when there are some,
        otherwise return an empty list
        """
        current = {self.start}
        for edge in edges:
            new_current = set()
            for node in current:
                if node in self.map and edge in self.map[node]:
                    new_current.update(self.map[node][edge])
            current = new_current
        terminants = []
        for node in current:
            if node in self.finals:
                terminants.append(node)
        return terminants

    def start_node(self):
        """getter: start node"""
        return self.start

    def set_start(self, node):
        """setter: start node"""
        if node in self.map:
            self.start = node
        else:
            return None
        return self

    def final_nodes(self):
        """getter: final nodes"""
        return self.finals

    def add_final(self, node):
        """setter: final nodes"""
        if node in self.nodes:
            self.finals.append(node)
        else:
            return None
        return self
