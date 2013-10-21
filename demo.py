#!/usr/bin/env python
# coding:utf-8

"""demo for package pyre"""

import pyre

regex = pyre.compile('(a|b)*a(a|b)')
print regex.match('aa')
# >>> 'aa'
print pyre.match(regex, 'aab')
# >>> 'aab'
