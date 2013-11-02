#!/usr/bin/env python
# coding:utf-8

"""Non-deterministic Finite Automata"""

EPSILON = r'\0'

class FA: #pylint: disable=W0212
    """
    Finite Automata

    EPSILON indicates epsilon
    """
    def __init__(self):
        self.__acceptable = set()
        self.__nodes = set()
        self.__map = {}
        self.__start = None
        self.__finals = set()
        self.__epsilon_clos = {}

    def map(self):
        return self.__map

    def relabel(self):
        """relabel the finite automata"""
        new = FA()
        relabel_map = dict(zip(self.__nodes.difference({ self.__start }),
                               range(1, len(self.__nodes))))
        relabel_map[self.__start] = 0
        new.__acceptable = self.__acceptable.copy()
        new.__nodes = { relabel_map[old] for old in self.__nodes }
        new.__map = { relabel_map[old]:
                        { edge: { relabel_map[node]
                                  for node in self.__map[old][edge]
                                }
                          for edge in self.__map[old]
                        }
                    for old in self.__map
                  }
        new.__start = relabel_map[self.__start]
        new.__finals = { relabel_map[old] for old in self.__finals }
        self.__epsilon_clos = { relabel_map[old]:
                                { relabel_map[e]
                                  for e in self.__epsilon_clos[old]
                                }
                              for old in self.__epsilon_clos
                            }
        return new

    def copy(self):
        """deep copy"""
        new = FA()
        from copy import deepcopy
        new.__acceptable = self.__acceptable.copy()
        new.__nodes = self.__nodes.copy()
        new.__map = deepcopy(self.__map)
        new.__start = self.__start
        new.__finals = self.__finals.copy()
        self.__epsilon_clos = deepcopy(self.__epsilon_clos)
        return new

    def partition(self, group, groups):
        """try to partition group"""
        if len(group) < 2:
            return None
        acceptable_edges = {}
        # partition based on acceptable edges
        for node in group:
            edges = set()
            if node in self.__map:
                for edge in self.__acceptable:
                    if edge in self.__map[node]:
                        edges.add(edge)
            acceptable_edges.setdefault(tuple(edges), set())
            acceptable_edges[tuple(edges)].add(node)
        parti = []
        for edges in acceptable_edges:
            local_parti = {}
            for node in acceptable_edges[edges]:
                edge_next_pair = set()
                for edge in edges:
                    idx = [ list(self.__map[node][edge])[0] in g
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
        groups = [self.__finals, self.__nodes.difference(self.__finals)]
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
        for start in self.__map:
            for edge in self.__map[start]:
                for dst in self.__map[start][edge]:
                    new.connect(divide[start], divide[dst], edge)
        new.set_start(divide[self.__start])
        _ = [new.add_final(divide[f]) for f in self.__finals]
        return new

    def reachable(self, nodes, edge):
        """
        return all the reachable nodes from any of the node in
        `nodes` via `edge`
        """
        if edge not in self.__acceptable:
            return None
        result = set()
        key = set()
        for node in nodes:
            for new_node in self.epsilon_closure(node):
                if new_node in self.__map and edge in self.__map[new_node]:
                    for next_node in self.__map[new_node][edge]:
                        key.add(next_node)
                        result.update(self.epsilon_closure(next_node))
        return (key, result)

    def make_dfa(self):
        """return a NFA corresponding to DFA"""
        new = FA()
        valid_acceptable = self.__acceptable.copy()
        if EPSILON in valid_acceptable:
            valid_acceptable.remove(EPSILON)
        new_nodes_set = { (self.__start,) }
        nodes_unmarked = { (self.__start,) }

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
                for final in self.__finals:
                    if final in e_clos:
                        new.add_final(tuple(key))
                        break

        new.set_start((self.__start,))
        for final in self.__finals:
            if final in self.epsilon_closure(self.__start):
                new.add_final((self.__start,))
                break
        return new

    def is_dfa(self):
        """whether the FA is deterministic """
        if EPSILON in self.__acceptable:
            return False
        for node in self.__map:
            for edge in self.__map[node]:
                if len(self.__map[node][edge]) > 1:
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
        self.__map.setdefault(from_node, {})
        self.__map[from_node].setdefault(edge, set())
        self.__map[from_node][edge].add(to_node)
        self.__acceptable.add(edge)
        self.__nodes.add(from_node)
        self.__nodes.add(to_node)
        return self

    def epsilon_closure(self, node):
        """
        return the epsilon closure of the given node
        """
        if node not in self.__epsilon_clos:
            closure = set()
            if node in self.__map and EPSILON in self.__map[node]:
                closure.update(self.__map[node][EPSILON])
            new_closure = closure.copy()
            if node in new_closure:
                new_closure.remove(node)
            for new_node in closure:
                if self.epsilon_closure(new_node):
                    new_closure.update(self.epsilon_closure(new_node))
            new_closure.add(node)
            self.__epsilon_clos[node] = new_closure
        return self.__epsilon_clos[node]

    def validate(self, edges):
        """
        validate if a string can be accepted by the FA

        `edges` can be a string while all the edges of the FA
        is characters

        return the reachable finals when there are some,
        otherwise return an empty list
        """
        current = self.epsilon_closure(self.__start)
        for edge in edges:
            new_current = set()
            for node in current:
                if node in self.__map and edge in self.__map[node]:
                    for next_node in self.__map[node][edge]:
                        new_current.update(self.epsilon_closure(next_node))
            current = new_current
        terminants = []
        for node in current:
            if node in self.__finals:
                terminants.append(node)
        return terminants

    def start_node(self):
        """getter: start node"""
        return self.__start

    def set_start(self, node):
        """setter: start node"""
        if node in self.__map:
            self.__start = node
        else:
            return None
        return self

    def final_nodes(self):
        """getter: final nodes"""
        return self.__finals

    def add_final(self, node):
        """setter: final nodes"""
        if node in self.__nodes:
            self.__finals.add(node)
        else:
            return None
        return self
