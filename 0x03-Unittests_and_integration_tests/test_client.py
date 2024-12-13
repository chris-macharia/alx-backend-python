#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test GithubOrgClient.public_repos method.
        """
        # Mocked payloads
        mock_repos_url = "https://api.github.com/orgs/mock-org/repos"
        mock_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]

        # Mock behaviors
        mock_public_repos_url.return_value = mock_repos_url
        mock_get_json.return_value = mock_payload

        # Initialize the client
        client = GithubOrgClient("mock-org")

        # Call the public_repos method
        result = client.public_repos()

        # Assertions
        self.assertEqual(result, ["repo1", "repo2", "repo3"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(mock_repos_url)


if __name__ == "__main__":
    unittest.main()
