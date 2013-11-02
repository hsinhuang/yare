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
        self.__regex__ = pyre.compile(r'a|b')
    def test_match(self):
        """test method `match`"""
        positive = []
        negative = []
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCaseSimpleConcatenation(unittest.TestCase):
    """simple test case: concatenation"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile(r'ab')
    def test_match(self):
        """test method `match`"""
        positive = []
        negative = []
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCaseSimpleLoop(unittest.TestCase):
    """simple test case: loop"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile(r'a*')
    def test_match(self):
        """test method `match`"""
        positive = []
        negative = []
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

if __name__ == '__main__':
    unittest.main()
