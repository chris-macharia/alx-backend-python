#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch, PropertyMock
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test class for GithubOrgClient."""

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test GithubOrgClient._public_repos_url method.
        """
        # Mocked payload for the org property
        mock_payload = {
            "repos_url": "https://api.github.com/orgs/mock-org/repos"
        }
        mock_org.return_value = mock_payload

        # Initialize the client
        client = GithubOrgClient("mock-org")

        # Call the _public_repos_url method
        result = client._public_repos_url

        # Assertions
        self.assertEqual(result, mock_payload["repos_url"])
        mock_org.assert_called_once()  # Ensure org method was called exactly once


if __name__ == "__main__":
    unittest.main()
