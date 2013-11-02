#!/usr/bin/env python
# coding:utf-8
#pylint: disable=C0103
#pylint: disable=R0904

"""unit test cases for the package"""

import unittest
import pyre

class TestSimpleEpsilon(unittest.TestCase):
    """simple test case: epsilon"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a|\\e')
    def test_match(self):
        """test method `match`"""
        positive = [ 'a', '' ]
        negative = [ ' ', '\\', '\\e', 'a|\\e', 'a\\e' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestSimpleSelection(unittest.TestCase):
    """simple test case: selection"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a|b')
    def test_match(self):
        """test method `match`"""
        positive = [ 'a', 'b' ]
        negative = [ '', ' ', '\\', '\\e', 'ab', 'a|b', 'c' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestSimpleConcatenation(unittest.TestCase):
    """simple test case: concatenation"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('ab')
    def test_match(self):
        """test method `match`"""
        positive = [ 'ab' ]
        negative = [ '', ' ', '\\', '\\e', 'a', 'b' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestSimpleLoop(unittest.TestCase):
    """simple test case: loop"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a*')
    def test_match(self):
        """test method `match`"""
        negative = [ ' ', '\\', '\\e', 'b' ]
        for case in negative:
            self.assertFalse(self.__regex__.match(case))
        for dup in xrange(0, 1000, 7):
            self.assertTrue(self.__regex__.match('a' * dup))

class TestCase1(unittest.TestCase):
    """complex test case 1"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a*b|cd')
    def test_match(self):
        """test method `match`"""
        positive = [ 'b', 'ab', 'aab', 'cd' ]
        negative = [ '', ' ', '\\', '\\e', 'bcd', 'acd', 'ad', 'd', 'a*b|cd' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCase2(unittest.TestCase):
    """complex test case 2"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a*(b|c)d')
    def test_match(self):
        """test method `match`"""
        positive = [ 'bd', 'abd', 'acd', 'cd' ]
        negative = [ '', ' ', '\\', '\\e', 'bcd', 'abcd', 'bc', 'd',
            'a*(b|c)d' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCase3(unittest.TestCase):
    """complex test case 3"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a*(b|c\))d')
    def test_match(self):
        """test method `match`"""
        positive = [ 'bd', 'abd', 'ac)d', 'c)d' ]
        negative = [ '', ' ', '\\', '\\e', 'acd', 'ac\)d', 'c\)d',
            'a*(b|c\))d' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCase4(unittest.TestCase):
    """complex test case 4"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a(\*b|c)d')
    def test_match(self):
        """test method `match`"""
        positive = [ 'a*bd', 'acd' ]
        negative = [ '', ' ', '\\', '\\e', 'abd', 'a\*bd', 'a(\*b|c)d' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCase5(unittest.TestCase):
    """complex test case 5"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a*b\|cd')
    def test_match(self):
        """test method `match`"""
        positive = [ 'b|cd', 'ab|cd' ]
        negative = [ '', ' ', '\\', '\\e', 'ab', 'cd', 'a*b\|cd' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestCase6(unittest.TestCase):
    """complex test case 6"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('(a|b)*a(a|b)(a|b)(a|b)')
    def test_match(self):
        """test method `match`"""
        positive = [ 'aaaa', 'abbb', 'abab', 'abba', 'aabb', 'aaab',
            'aaba', 'abaa' ]
        negative = [ '', ' ', '\\', '\\e', '(a|b)*a(a|b)(a|b)(a|b)' ]
        for case in positive:
            for dup in xrange(0, 100, 7):
                self.assertTrue(self.__regex__.match('a'*dup + case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))

class TestException(unittest.TestCase):
    """test case : exception"""
    def test_compile(self):
        """test method `compile`"""
        raisable = [ 'a(b', ')a', 'a\(b|c)a*b' ]
        for case in raisable:
            self.assertRaises(SyntaxError, pyre.compile, case)

if __name__ == '__main__':
    unittest.main()
