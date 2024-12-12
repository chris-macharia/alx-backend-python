#!/usr/bin/env python3
"""
Unit test for GithubOrgClient.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        Uses @patch to mock get_json and @parameterized.expand for test cases.
        """
        # Mock response for the get_json function
        mock_response = {"login": org_name, "id": 12345, "description": f"{org_name} details"}
        mock_get_json.return_value = mock_response

        # Initialize the client and call the org method
        client = GithubOrgClient(org_name)
        org = client.get_org()

        # Assertions
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(org, mock_response)


if __name__ == "__main__":
    unittest.main()
