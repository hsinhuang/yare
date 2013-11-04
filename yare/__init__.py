#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

from .regex import compile, match
from .utils import escape, group, select, concat, loop, \
    loop_, diff, optional, range
from .definitions import EPSILON, DIGIT, LOWERCASE, UPPERCASE, \
    WHITESPACE, PUNCTUATION, WILDCARD
