#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""

import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """implementation of Test class for utils.access_nested_map"""
    @parameterized.expand([
        ("case1", {"a": 1}, ("a",), 1),
        ("case2", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("case3", {"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map, path, expected_result):
        """method tests Access nested map with key path.
        Parameters
        ---------
        nested_map: Mapping
        A nested map
        path: Sequence
        a sequence of key representing a path to the value
        result: right expected results values according to input parameters
        """
        tested_output = access_nested_map(nested_map, path)
        self.assertEqual(tested_output, expected_result)


if__name__ == '__main__':
    unittest.main()
