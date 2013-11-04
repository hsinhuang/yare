#!/usr/bin/env python
# coding:utf-8

"""demo for package pyre"""

import yare

regex = yare.compile('(a|b)*a(a|b)')
print regex.match('aa')
# >>> True
print yare.match(regex, 'aab')
# >>> True
