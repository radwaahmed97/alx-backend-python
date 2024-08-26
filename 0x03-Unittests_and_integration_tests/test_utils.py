#!/usr/bin/env python3
"""unit test for utils.access_nested_map"""

import unittest
from unittests.mock import patch, Mock
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
        ({}, ("a",), 'a'),
        ({"a": 1}, ("a", "b"), 'b')
    ])
    def test_access_nested_map_exception(self, nested_map, path, error_result):
        """tests if error raised when keys not found"""
        with self.assertRaises(KeyError) as err:
            access_nested_map(nested_map, path)
            self.assertEqual(error_result, err.exception)


class TestGetJson(unittest.TestCase):
    """Implementation of test class for utils.get_json"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """method tests of get_json returns expected results"""
        Mocked_output = Mock()
        Mocked_output.json.return_value = test_payload
        with patch('requests.get', return_value=Mocked_output):
            tested_output = get_json(test_url)
            self.asserEqual(tested_output, test_payload)
            Mocked_output.json.assert_called_once()
