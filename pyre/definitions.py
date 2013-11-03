#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

import string
from .utils import selection

# useful regular expression definition
EPSILON = '\\e'
DIGIT = selection(string.digits)
LOWER = selection(string.lowercase)
UPPER = selection(string.uppercase)
WHITESPACE = selection(string.whitespace)
PUNCTUATION = selection(string.punctuation)
WILDCARD = selection(string.printable)
