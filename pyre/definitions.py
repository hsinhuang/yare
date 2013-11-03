#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

import string
from .utils import selection

# useful regular expression definition
EPSILON = '\\e'
DIGIT = selection(list(string.digits))
LOWERCASE = selection(list(string.lowercase))
UPPERCASE = selection(list(string.uppercase))
WHITESPACE = selection(list(string.whitespace))
PUNCTUATION = selection(list(string.punctuation))
WILDCARD = selection(list(string.printable))
