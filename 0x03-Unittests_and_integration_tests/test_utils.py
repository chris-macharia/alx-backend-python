#!/usr/bin/env python3

import unittest
from unittest.mock import patch, Mock
from utils import get_json

class TestGetJson(unittest.TestCase):
    
    @patch("utils.requests.get")
    def test_get_json(self, mock_get):
        """
        Test the utils.get_json function to ensure it returns the expected result.
        Uses unittest.mock.patch decorator to mock external HTTP calls.
        """
        # Define test cases
        test_cases = [
            {"test_url": "http://example.com", "test_payload": {"payload": True}},
            {"test_url": "http://holberton.io", "test_payload": {"payload": False}}
        ]

        for case in test_cases:
            test_url = case["test_url"]
            test_payload = case["test_payload"]

            # Reset the mock to clear any previous calls
            mock_get.reset_mock()

            # Create a Mock response object with a json method
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            # Call the function under test
            result = get_json(test_url)

            # Assert the mocked get was called once with the correct URL
            mock_get.assert_called_once_with(test_url)

            # Assert the function returns the expected payload
            self.assertEqual(result, test_payload)

# End of TestGetJson class

