#!/usr/bin/env python
# coding:utf-8

"""Non-deterministic Finite Automata"""

EPSILON = r'\0'

class FA:
    """
    Finite Automata

    EPSILON indicates epsilon
    """
    def __init__(self):
        self.acceptable = set()
        self.nodes = set()
        self.map = {}
        self.start = None
        self.finals = set()
        self.epsilon_clos = {}

    def relabel(self):
        """relabel the finite automata"""
        new = FA()
        relabel_map = dict(zip(self.nodes.difference({ self.start }),
                               range(1, len(self.nodes))))
        relabel_map[self.start] = 0
        new.acceptable = self.acceptable.copy()
        new.nodes = { relabel_map[old] for old in self.nodes }
        new.map = { relabel_map[old]:
                        { edge: { relabel_map[node]
                                  for node in self.map[old][edge]
                                }
                          for edge in self.map[old]
                        }
                    for old in self.map
                  }
        new.start = relabel_map[self.start]
        new.finals = { relabel_map[old] for old in self.finals }
        self.epsilon_clos = { relabel_map[old]:
                                { relabel_map[e]
                                  for e in self.epsilon_clos[old]
                                }
                              for old in self.epsilon_clos
                            }
        return new

    def copy(self):
        """deep copy"""
        new = FA()
        from copy import deepcopy
        new.acceptable = self.acceptable.copy()
        new.nodes = self.nodes.copy()
        new.map = deepcopy(self.map)
        new.start = self.start
        new.finals = self.finals.copy()
        self.epsilon_clos = deepcopy(self.epsilon_clos)
        return new

    def minimize(self):
        """minimize the number of states of the DFA"""
        assert self.is_dfa()

    def reachable(self, nodes, edge):
        """
        return all the reachable nodes from any of the node in
        `nodes` via `edge`
        """
        if edge not in self.acceptable:
            return None
        result = set()
        key = set()
        for node in nodes:
            for new_node in self.epsilon_closure(node):
                if new_node in self.map and edge in self.map[new_node]:
                    for next_node in self.map[new_node][edge]:
                        key.add(next_node)
                        result.update(self.epsilon_closure(next_node))
        return (key, result)

    def make_dfa(self):
        """return a NFA corresponding to DFA"""
        new = FA()
        valid_acceptable = self.acceptable.copy()
        valid_acceptable.remove(EPSILON)
        new_nodes_set = { (self.start,) }
        nodes_unmarked = { (self.start,) }

        while nodes_unmarked:
            node = nodes_unmarked.pop()
            for edge in valid_acceptable:
                key, e_clos = self.reachable(node, edge)
                if tuple(key) not in new_nodes_set:
                    new_nodes_set.add(tuple(key))
                    nodes_unmarked.add(tuple(key))
                new.connect(node, tuple(key), edge)
                for final in self.finals:
                    if final in e_clos:
                        new.add_final(tuple(key))

        new.set_start((self.start,))
        return new

    def is_dfa(self):
        """whether the FA is deterministic """
        if EPSILON in self.acceptable:
            return False
        for node in self.map:
            for edge in self.map[node]:
                if len(self.map[node][edge]) > 1:
                    return False
        return True

    def connect(self, from_node, to_node, edge):
        """
        >>> fa = FA()
        >>> fa.connect(0, 1, 'a')
        self.map = { 0: { 'a': {1} } }
        >>> fa.connect(0, 2, 'a').connect(1, 2, 'b')
        self.map = { 0: { 'a': {1, 2} },
                     1: { 'b': {2} } }
        """
        self.map.setdefault(from_node, {})
        self.map[from_node].setdefault(edge, set())
        self.map[from_node][edge].add(to_node)
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
            if node in new_closure:
                new_closure.remove(node)
            for new_node in closure:
                if self.epsilon_closure(new_node):
                    new_closure.update(self.epsilon_closure(new_node))
            new_closure.add(node)
            self.epsilon_clos[node] = new_closure
        return self.epsilon_clos[node]

    def validate(self, edges):
        """
        validate if a string can be accepted by the FA

        `edges` can be a string while all the edges of the FA
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
            self.finals.add(node)
        else:
            return None
        return self

test1 = FA()
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
