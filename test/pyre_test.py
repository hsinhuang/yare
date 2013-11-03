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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'a', '' ]
        negative = [ ' ', '\\', '\\e' ]
        partial = [
            ('a|\\e', 1),
            ('a\\e', 1),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'a', 'b' ]
        negative = [ '', ' ', '\\', '\\e', 'c' ]
        partial = [
            ('ab', 1),
            ('a|b', 1),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'ab' ]
        negative = [ '', ' ', '\\', '\\e', 'a', 'b' ]
        partial = [
            ('aba', 2),
            ('abab', 2),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        negative = [ ' ', '\\', '\\e', 'b' ]
        partial = [
            ('ab', 1),
            ('aaabababab', 3),
        ]
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for dup in xrange(0, 1000, 7):
            self.assertEqual(self.__regex__.match_prefix('a' * dup), dup)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'b', 'ab', 'aab', 'cd' ]
        negative = [ '', ' ', '\\', '\\e', 'd', 'ad', 'acd', 'a*b|cd' ]
        partial = [
            ('bcd', 1),
            ('aabcd', 3),
            ('cdaab', 2),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'bd', 'abd', 'acd', 'cd' ]
        negative = [ '', ' ', '\\', '\\e', 'bcd', 'abcd', 'bc', 'd',
            'a*(b|c)d' ]
        partial = [
            ('bda', 2),
            ('cdcd', 2),
            ('acdabcd', 3),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'bd', 'abd', 'ac)d', 'c)d' ]
        negative = [ '', ' ', '\\', '\\e', 'acd', 'ac\)d', 'c\)d',
            'a*(b|c\))d' ]
        partial = [
            ('bda', 2),
            ('c)dcd', 3),
            ('ac)dabcd', 4),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'a*bd', 'acd' ]
        negative = [ '', ' ', '\\', '\\e', 'abd', 'a\*bd', 'a(\*b|c)d' ]
        partial = [
            ('a*bda', 4),
            ('acdcd', 3),
            ('acdabcd', 3),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

class TestCase5(unittest.TestCase):
    """complex test case 5"""
    def setUp(self):
        """compile a regex"""
        self.__regex__ = pyre.compile('a*b\|cd')
    def test_match(self):
        """test method `match`"""
        positive = [ 'b|cd', 'ab|cd', 'aaab|cd' ]
        negative = [ '', ' ', '\\', '\\e', 'ab', 'cd', 'a*b\|cd' ]
        for case in positive:
            self.assertTrue(self.__regex__.match(case))
        for case in negative:
            self.assertFalse(self.__regex__.match(case))
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'b|cd', 'ab|cd', 'aaab|cd' ]
        negative = [ '', ' ', '\\', '\\e', 'ab', 'cd', 'a*b\|cd' ]
        partial = [
            ('aaab|cdd', 7),
            ('aaab|cdab|cd', 7),
        ]
        for case in positive:
            self.assertEqual(self.__regex__.match_prefix(case), len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

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
    def test_match_prefix(self):
        """test method `match_prefix`"""
        positive = [ 'aaaa', 'abbb', 'abab', 'abba', 'aabb', 'aaab',
            'aaba', 'abaa' ]
        negative = [ '', ' ', '\\', '\\e', '(a|b)*a(a|b)(a|b)(a|b)' ]
        partial = [
            ('aaaac', 4),
            ('abbab', 4),
            ('bbababa', 6),
        ]
        for case in positive:
            for dup in xrange(0, 100, 7):
                self.assertEqual(self.__regex__.match_prefix('a'*dup + case),
                    dup+len(case))
        for case in negative:
            self.assertEqual(self.__regex__.match_prefix(case), 0)
        for case in partial:
            self.assertEqual(self.__regex__.match_prefix(case[0]), case[1])

class TestException(unittest.TestCase):
    """test case : exception"""
    def test_compile(self):
        """test method `compile`"""
        raisable = [ 'a(b', ')a', 'a\(b|c)a*b' ]
        for case in raisable:
            self.assertRaises(SyntaxError, pyre.compile, case)

if __name__ == '__main__':
    unittest.main()
