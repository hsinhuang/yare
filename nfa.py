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
        self.epsilon_clos = {}

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
        if node not in self.epsilon_clos:
            if node not in self.nodes:
                return None
            closure = set()
            if node in self.map and EPSILON in self.map[node]:
                closure.update(self.map[node][EPSILON])
            new_closure = closure.copy()
            for new_node in closure:
                if self.epsilon_closure(new_node):
                    new_closure.update(self.epsilon_closure(new_node))
            new_closure.add(node)
            self.epsilon_clos[node] = new_closure
        return self.epsilon_clos[node]

    def validate(self, edges):
        """
        validate if a string can be accepted by the NFA

        `edges` can be a string while all the edges of the NFA
        is characters

        return the reachable finals when there are some,
        otherwise return an empty list
        """
        current = self.epsilon_closure(self.start)
        for edge in edges:
            new_current = set()
            for node in current:
                if node in self.map and edge in self.map[node]:
                    for next_node in self.map[node][edge]:
                        new_current.update(self.epsilon_closure(next_node))
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

test1 = NFA()
test1\
.connect(0, 1, EPSILON)\
.connect(1, 2, EPSILON)\
.connect(1, 3, EPSILON)\
.connect(1, 7, EPSILON)\
.connect(2, 4, 'a')\
.connect(3, 5, 'b')\
.connect(4, 6, EPSILON)\
.connect(5, 6, EPSILON)\
.connect(6, 1, EPSILON)\
.connect(6, 7, EPSILON)\
.connect(7, 8, EPSILON)\
.connect(8, 9, 'a')\
.connect(9, 10, EPSILON)\
.connect(10, 11, EPSILON)\
.connect(10, 12, EPSILON)\
.connect(11, 13, 'a')\
.connect(12, 14, 'b')\
.connect(13, 15, EPSILON)\
.connect(14, 15, EPSILON)\
.set_start(0)\
.add_final(15)
