#!/usr/bin/env python
# coding:utf-8

"""
useful helper functions

all function only accept normal letter as parameter, i.e., you should
*NOT* escape the letter before you passed it to the functions

all return values are escaped except `group`
"""

import string

ESCAPE_TABLE = {
    '\\' : '\\\\',
    '|' : '\|',
    '*' : '\*',
    '(' : '\(',
    ')' : '\)',
}

def escape(patterns):
    """
    escape the letter in `patterns`

    return a list
    """
    assert hasattr(patterns, '__iter__') or type(patterns) == str
    escaped = []
    for pattern in patterns:
        if pattern in ESCAPE_TABLE:
            escaped.append(ESCAPE_TABLE[pattern])
        else:
            escaped.append(pattern)
    return escaped

def group(pattern):
    """
    return a regex string which contains pattern in a group
    """
    return '(' + ''.join(escape[pattern]) + ')'

def selection(patterns):
    """
    return a regex string which means a selection between `patterns`
    """
    assert hasattr(patterns, '__iter__') or type(patterns) == str
    return group('|'.join(escape(patterns)))

def concatenation(patterns):
    """
    return a regex string which means a concatenation of `patterns`
    """
    assert hasattr(patterns, '__iter__') or type(patterns) == str
    return group(''.join(escape(patterns)))

def loop(pattern):
    """
    return a regex string which means a loop of `pattern`
    """
    assert not hasattr(pattern, '__iter__')
    return group(group(''.join(escape([pattern]))) + '*')

def diff(patterns):
    """
    return a regex string which stands for a regex with no letter
     in `patterns`

    similiar to `(^patterns)` in other regular expression language
    """
    assert hasattr(patterns, '__iter__') or type(patterns) == str
    all_letters = set(string.printable)
    valid_letters = all_letters.difference(set(patterns))
    return selection(valid_letters)

def nonempty_loop(pattern):
    """
    return a regex string which means a loop of `pattern`

    similiar to `((pattern)+)` in other regular expression language
    """
    assert not hasattr(pattern, '__iter__')
    return group(group(''.join(escape([pattern]))) + loop(pattern))

def optional(pattern):
    """
    return a regex string which means `pattern` is optional

    similiar to `((pattern)?)` in other regular expression language
    """
    assert not hasattr(pattern, '__iter__')
    return selection([pattern, '\\e'])

def range(start, end):
    """
    return a regex string which means all letters from `start` to `end`,
    both included

    similiar to `[start-end]` in other regular expression language
    """
    assert start < end
    all_letters = string.printable
    return selection(
        all_letters[all_letters.index(start):all_letters.index((end))]
    )
