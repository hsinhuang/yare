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

def escape(pattern):
    """
    escape the `pattern`
    """
    if type(pattern) != str:
        raise TypeError('require type `str`, but get `%s`' % pattern)
    if pattern in ESCAPE_TABLE:
        return ESCAPE_TABLE[pattern]
    else:
        return pattern

def group(pattern):
    """
    return a regex string which contains pattern in a group
    """
    if type(pattern) != str:
        raise TypeError('require type `str`, but get `%s`' % pattern)
    return '(' + ''.join(escape(pattern)) + ')'

def selection(patterns):
    """
    return a regex string which means a selection between `patterns`
    """
    if not hasattr(patterns, '__iter__'):
        raise TypeError('require iterable, but get `%s`' % patterns)
    return group('|'.join([escape(pattern) for pattern in patterns]))

def concatenation(patterns):
    """
    return a regex string which means a concatenation of `patterns`
    """
    if not hasattr(patterns, '__iter__'):
        raise TypeError('require iterable, but get `%s`' % patterns)
    return group(''.join([escape(pattern) for pattern in patterns]))

def loop(pattern):
    """
    return a regex string which means a loop of `pattern`
    """
    if type(pattern) != str:
        raise TypeError('require type `str`, but get `%s`' % pattern)
    return group(group(''.join(escape(pattern))) + '*')

def nonempty_loop(pattern):
    """
    return a regex string which means a loop of `pattern`

    similiar to `((pattern)+)` in other regular expression language
    """
    if type(pattern) != str:
        raise TypeError('require type `str`, but get `%s`' % pattern)
    return group(group(''.join(escape(pattern))) + loop(pattern))

def diff(patterns):
    """
    return a regex string which stands for a regex with no letter
     in `patterns`

    similiar to `(^patterns)` in other regular expression language
    """
    if not hasattr(patterns, '__iter__'):
        raise TypeError('require iterable, but get `%s`' % patterns)
    all_letters = set(string.printable)
    valid_letters = all_letters.difference(set(patterns))
    return selection(valid_letters)

def optional(pattern):
    """
    return a regex string which means `pattern` is optional

    similiar to `((pattern)?)` in other regular expression language
    """
    if type(pattern) != str:
        raise TypeError('require type `str`, but get `%s`' % pattern)
    return selection([pattern, '\\e'])

def range(start, end):
    """
    return a regex string which means all letters from `start` to `end`,
    both included

    similiar to `[start-end]` in other regular expression language
    """
    if type(start) != str:
        raise TypeError('require type `str`, but get `%s`' % start)
    if type(end) != str:
        raise TypeError('require type `str`, but get `%s`' % end)
    assert start < end and len(start) == len(end) == 1
    all_letters = string.printable
    return selection(
        all_letters[all_letters.index(start):all_letters.index((end))]
    )
