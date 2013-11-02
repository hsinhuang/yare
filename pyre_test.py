#!/usr/bin/env python
# coding:utf-8
#pylint: disable=C0103
#pylint: disable=R0904

"""unit test cases for the package"""

import random
import unittest
import pyre

class TestCaseSimpleSelection(unittest.TestCase):
    """simple test case: selection"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a|b')
    def test_match(self):
        """test method `match`"""
        positive = [ 'a', 'b' ]
        negative = [ '', '\\', '\\e', 'ab', 'a|b', 'c' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCaseSimpleConcatenation(unittest.TestCase):
    """simple test case: concatenation"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('ab')
    def test_match(self):
        """test method `match`"""
        positive = [ 'ab' ]
        negative = [ '', '\\', '\\e', 'a', 'b' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCaseSimpleLoop(unittest.TestCase):
    """simple test case: loop"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a*')
    def test_match(self):
        """test method `match`"""
        negative = [ ' ', '\\', '\\e', 'b' ]
        for case in negative:
            self.assertFalse(self.__regex__.match(case))
        for dup in xrange(0, 1000):
            self.assertTrue(self.__regex__.match('a' * dup))

if __name__ == '__main__':
    unittest.main()
