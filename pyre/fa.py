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
        self.__acceptable__ = set()
        self.__nodes__ = set()
        self.__map__ = {}
        self.__start__ = None
        self.__finals__ = set()
        self.__epsilon_clos__ = {}

    def map(self):
        """getter : __map__"""
        return self.__map__

    def relabel(self):
        """relabel the finite automata"""
        new = FA()
        relabel_map = dict(zip(self.__nodes__.difference({self.__start__}),
                               range(1, len(self.__nodes__))))
        relabel_map[self.__start__] = 0
        new.__acceptable__ = self.__acceptable__.copy()
        new.__nodes__ = { relabel_map[old] for old in self.__nodes__ }
        new.__map__ = { relabel_map[old]:
                        { edge: { relabel_map[node]
                                  for node in self.__map[old][edge]
                                }
                          for edge in self.__map[old]
                        }
                    for old in self.__map__
                  }
        new.__start__ = relabel_map[self.__start__]
        new.__finals__ = { relabel_map[old] for old in self.__finals__ }
        self.__epsilon_clos__ = { relabel_map[old]:
                                { relabel_map[e]
                                  for e in self.__epsilon_clos[old]
                                }
                              for old in self.__epsilon_clos__
                            }
        return new

    def copy(self):
        """deep copy"""
        new = FA()
        from copy import deepcopy
        new.__acceptable__ = self.__acceptable__.copy()
        new.__nodes__ = self.__nodes__.copy()
        new.__map__ = deepcopy(self.__map__)
        new.__start__ = self.__start__
        new.__finals__ = self.__finals__.copy()
        self.__epsilon_clos__ = deepcopy(self.__epsilon_clos__)
        return new

    def partition(self, group, groups):
        """try to partition group"""
        if len(group) < 2:
            return None
        acceptable_edges = {}
        # partition based on acceptable edges
        for node in group:
            edges = set()
            if node in self.__map__:
                for edge in self.__acceptable__:
                    if edge in self.__map__[node]:
                        edges.add(edge)
            acceptable_edges.setdefault(tuple(edges), set())
            acceptable_edges[tuple(edges)].add(node)
        parti = []
        for edges in acceptable_edges:
            local_parti = {}
            for node in acceptable_edges[edges]:
                edge_next_pair = set()
                for edge in edges:
                    idx = [ list(self.__map__[node][edge])[0] in g
                            for g in groups ].index(True)
                    edge_next_pair.add((edge, idx))
                edge_next_t = tuple(edge_next_pair)
                local_parti.setdefault(edge_next_t, set())
                local_parti[edge_next_t].add(node)
            parti += [ list(local_parti[p]) for p in local_parti ]
        if len(parti) > 1:
            return parti
        return None

    def minimize(self):
        """minimize the number of states of the DFA"""
        assert self.is_dfa()
        groups = [self.__finals__,
            self.__nodes__.difference(self.__finals__)]
        from copy import deepcopy
        new_groups = deepcopy(groups)
        parti = True
        while parti:
            delete = None
            for group in groups:
                parti = self.partition(group, groups)
                if parti:
                    delete = group
                    break
            if parti:
                new_groups.remove(delete)
                new_groups += parti
                groups = deepcopy(new_groups)
        new = FA()
        divide = {}
        for group in groups:
            for node in group:
                divide[node] = tuple(group)
        for start in self.__map__:
            for edge in self.__map__[start]:
                for dst in self.__map__[start][edge]:
                    new.connect(divide[start], divide[dst], edge)
        new.set_start(divide[self.__start__])
        for node in self.__finals__:
            new.add_final(divide[node])
        return new

    def reachable(self, nodes, edge):
        """
        return all the reachable nodes from any of the node in
        `nodes` via `edge`
        """
        if edge not in self.__acceptable__:
            return None
        result = set()
        key = set()
        for node in nodes:
            for new_node in self.epsilon_closure(node):
                if new_node in self.__map__ and edge in self.__map__[new_node]:
                    for next_node in self.__map__[new_node][edge]:
                        key.add(next_node)
                        result.update(self.epsilon_closure(next_node))
        return (key, result)

    def make_dfa(self):
        """return a NFA corresponding to DFA"""
        new = FA()
        valid_acceptable = self.__acceptable__.copy()
        if EPSILON in valid_acceptable:
            valid_acceptable.remove(EPSILON)
        new_nodes_set = { (self.__start__,) }
        nodes_unmarked = { (self.__start__,) }

        while nodes_unmarked:
            node = nodes_unmarked.pop()
            for edge in valid_acceptable:
                key, e_clos = self.reachable(node, edge)
                if not key:
                    continue
                if tuple(key) not in new_nodes_set:
                    new_nodes_set.add(tuple(key))
                    nodes_unmarked.add(tuple(key))
                new.connect(node, tuple(key), edge)
                for final in self.__finals__:
                    if final in e_clos:
                        new.add_final(tuple(key))
                        break

        new.set_start((self.__start__,))
        for final in self.__finals__:
            if final in self.epsilon_closure(self.__start__):
                new.add_final((self.__start__,))
                break
        return new

    def is_dfa(self):
        """whether the FA is deterministic """
        if EPSILON in self.__acceptable__:
            return False
        for node in self.__map__:
            for edge in self.__map__[node]:
                if len(self.__map__[node][edge]) > 1:
                    return False
        return True

    def connect(self, from_node, to_node, edge):
        """
        >>> fa = FA()
        >>> fa.connect(0, 1, 'a')
        self.__map = { 0: { 'a': {1} } }
        >>> fa.connect(0, 2, 'a').connect(1, 2, 'b')
        self.__map = { 0: { 'a': {1, 2} },
                     1: { 'b': {2} } }
        """
        self.__map__.setdefault(from_node, {})
        self.__map__[from_node].setdefault(edge, set())
        self.__map__[from_node][edge].add(to_node)
        self.__acceptable__.add(edge)
        self.__nodes__.add(from_node)
        self.__nodes__.add(to_node)
        return self

    def epsilon_closure(self, node):
        """
        return the epsilon closure of the given node
        """
        if node not in self.__epsilon_clos__:
            closure = set()
            if node in self.__map__ and EPSILON in self.__map__[node]:
                closure.update(self.__map__[node][EPSILON])
            new_closure = closure.copy()
            if node in new_closure:
                new_closure.remove(node)
            for new_node in closure:
                if self.epsilon_closure(new_node):
                    new_closure.update(self.epsilon_closure(new_node))
            new_closure.add(node)
            self.__epsilon_clos__[node] = new_closure
        return self.__epsilon_clos__[node]

    def validate(self, edges):
        """
        validate if a string can be accepted by the FA

        `edges` can be a string while all the edges of the FA
        is characters

        return True if any final node is reachable, otherwise False
        """
        current = self.epsilon_closure(self.__start__)
        for edge in edges:
            new_current = set()
            for node in current:
                if node in self.__map__ and edge in self.__map__[node]:
                    for next_node in self.__map__[node][edge]:
                        new_current.update(self.epsilon_closure(next_node))
            current = new_current
        return self.__any_terminant__(current)

    def try_match(self, edges):
        """
        try to match string as long as possible

        return the maximum index that makes self.validate(edges[:index])
        True, if there is no such index, return 0

        `edges` can be a string while all the edges of the FA
        is characters
        """
        idx = 0
        current = self.epsilon_closure(self.__start__)
        for i, edge in enumerate(edges):
            new_current = set()
            for node in current:
                if node in self.__map__ and edge in self.__map__[node]:
                    for next_node in self.__map__[node][edge]:
                        new_current.update(self.epsilon_closure(next_node))
            current = new_current
            if self.__any_terminant__(current):
                idx = i+1
        return idx

    def start_node(self):
        """getter: start node"""
        return self.__start__

    def set_start(self, node):
        """setter: start node"""
        if node in self.__map__:
            self.__start__ = node
        else:
            return None
        return self

    def final_nodes(self):
        """getter: final nodes"""
        return self.__finals__

    def add_final(self, node):
        """setter: final nodes"""
        if node in self.__nodes__:
            self.__finals__.add(node)
        else:
            return None
        return self

    def __any_terminant__(self, nodes):
        """
        whether at least a terminant exists in `nodes`
        """
        for node in nodes:
            if node in self.__finals__:
                return True
        return False
