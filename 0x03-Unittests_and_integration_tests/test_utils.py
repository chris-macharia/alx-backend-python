#!/usr/bin/env python3

"""
Unit tests for the `access_nested_map` function.
- Tests the correct functionality for valid paths.
- Tests exception handling for invalid paths.
"""

import unittest
from parameterized import parameterized

# Function to retrieve a value from a nested map using a given path
def access_nested_map(nested_map, path):
    """
    Access a value from a nested dictionary using a sequence of keys.

    Args:
        nested_map (dict): The nested dictionary to traverse.
        path (tuple): A sequence of keys to follow in the nested dictionary.

    Returns:
        The value found at the end of the path.

    Raises:
        KeyError: If a key in the path is not found in the dictionary.
    """
    for key in path:
        if not isinstance(nested_map, dict):
            raise KeyError(f"Key {key} not found")
        if key not in nested_map:
            raise KeyError(f"Key {key} not found")
        nested_map = nested_map[key]
    return nested_map

class TestAccessNestedMap(unittest.TestCase):
    """Unit test class for the `access_nested_map` function."""

    @parameterized.expand([
        # Test cases for valid paths
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test that `access_nested_map` returns the correct value for valid paths.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        # Test cases for invalid paths
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test that `access_nested_map` raises a KeyError for invalid paths.
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)
        self.assertEqual(context.exception.args[0], f"Key {path[len(path)-1]} not found")

if __name__ == '__main__':
    unittest.main()
