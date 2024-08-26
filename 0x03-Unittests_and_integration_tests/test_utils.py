#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """implementation of Test class for utils.access_nested_map"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """method tests Access nested map with key path parameters"""
        tested_output = access_nested_map(nested_map, path)
        self.assertEqual(tested_output, expected_result)

    @parameterized.expand([
        ({}, ("a",) 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, error_result):
        """tests if error raised when keys not found"""
        with self.assertRaises(KeyError) as e:
            access_nested_map(nested_map, path)
            self.assertEqual(error_result, e.exception)
