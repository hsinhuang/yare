#!/usr/bin/env python
# coding:utf-8
#pylint: disable=C0103
#pylint: disable=R0904

"""unit test cases for the package"""

import unittest
import pyre

class TestUtils(unittest.TestCase):
    """test utils.py"""
    def test_escape(self):
        """test : escape"""
        cases = [
            ('abcde', list('abcde')),
            ('()|*\\ea', ['\(', '\)', '\|', '\*', '\\\\', 'e', 'a']),
        ]
        for case in cases:
            self.assertEqual(pyre.escape(case[0]), case[1])

    def test_group(self):
        """test : group"""
        cases = [
            ('abcde', '(abcde)'),
        ]
        for case in cases:
            self.assertEqual(pyre.group(case[0]), case[1])

    def test_selection(self):
        """test : selection"""
        cases = [
            ('a', '(a)'),
            ('ab', '(a|b)'),
            (['ab', '\\e'], '(ab|\\e)'),
            (['a|b'], '(a|b)'),
            (['a|b', 'c'], '(a|b|c)'),
            (['a|b', 'c|a'], '(a|b|c|a)'),
        ]
        for case in cases:
            self.assertEqual(pyre.selection(case[0]), case[1])

    def test_concatenation(self):
        """test : concatenation"""
        cases = [
            ('abcde', '(abcde)'),
            ('(abcde)', '(\(abcde\))'),
            (['a', 'b'], '(ab)'),
            (['a'], '(a)'),
        ]
        for case in cases:
            self.assertEqual(pyre.concatenation(case[0]), case[1])

    def test_loop(self):
        """test : loop"""
        cases = [
            ('abcde', '((abcde)*)'),
            ('(abcde)', '((\(abcde\))*)'),
        ]
        for case in cases:
            self.assertEqual(pyre.loop(case[0]), case[1])

    def test_diff(self):
        """test : diff"""
        import string
        cases = [
            (string.printable, '()'),
        ]
        for case in cases:
            self.assertEqual(pyre.diff(case[0]), case[1])

    def test_nonempty_loop(self):
        """test : nonempty_loop"""
        cases = [
            ('abcde', '((abcde)((abcde)*))'),
            ('(abcde)', '((\(abcde\))((\(abcde\))*))'),
        ]
        for case in cases:
            self.assertEqual(pyre.nonempty_loop(case[0]), case[1])

    def test_optional(self):
        """test : optional"""
        cases = [
            ('a', '(a|\\e)'),
            ('ab', '(ab|\\e)'),
            ('ab|\\e', '(ab|\\e|\\e)'),
            ('a|b', '(a|b|\\e)'),
        ]
        for case in cases:
            self.assertEqual(pyre.optional(case[0]), case[1])


if __name__ == '__main__':
    unittest.main()
