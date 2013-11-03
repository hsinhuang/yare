#!/usr/bin/env python
# coding:utf-8

"""init file of the package"""

import string
from .utils import select

# useful regular expression definition
EPSILON = '\\e'
DIGIT = select(list(string.digits))
LOWERCASE = select(list(string.lowercase))
UPPERCASE = select(list(string.uppercase))
WHITESPACE = select(list(string.whitespace))
PUNCTUATION = select(list(string.punctuation))
WILDCARD = select(list(string.printable))
