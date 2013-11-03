#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

from .regex import compile, match
from .utils import escape, group, selection, concatenation, loop, \
    diff, nonempty_loop, optional
from .definitions import EPSILON, DIGIT, LOWER, UPPER, \
    WHITESPACE, PUNCTUATION, WILDCARD
