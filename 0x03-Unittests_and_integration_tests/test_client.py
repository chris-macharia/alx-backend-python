#!/usr/bin/env python3

from unittest import TestCase
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestIntegrationGithubOrgClient(TestCase):
    # Define the necessary variables here
    org_payload = {
        "repos_url": "https://api.github.com/orgs/mock-org/repos",
        "some_other_data": "value"  # Add any additional fields needed
    }

    repos_payload = [
        {"name": "repo1"},
        {"name": "repo2"},
    ]

    expected_repos = ["repo1", "repo2"]

    apache2_repos = ["repo1"]  # Repos with Apache 2.0 license, for example

    @classmethod
    def setUpClass(cls):
        """Set up for integration test."""
        cls.get_patcher = patch("client.get_json")

        # Mocking get_json to return the appropriate payload based on URL
        def get_json_side_effect(url):
            if url == "https://api.github.com/orgs/mock-org":
                return cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                return cls.repos_payload
            raise ValueError(f"Unexpected URL {url}")

        cls.mock_get_json = cls.get_patcher.start()
        cls.mock_get_json.side_effect = get_json_side_effect

    @classmethod
    def tearDownClass(cls):
        """Tear down after integration test."""
        cls.get_patcher.stop()

    @parameterized.expand([
        ("test_public_repos", "repos_url", ["repo1", "repo2"]),
        ("test_public_repos_with_license", "repos_url", ["repo1"]),  # Add license filtering here if needed
    ])
    def test_public_repos(self, name, repos_url, expected_repos):
        """Test the public_repos method."""
        client = GithubOrgClient("mock-org")
        repos = client.public_repos()
        self.assertEqual(repos, expected_repos)
        self.mock_get_json.assert_called()

    def test_public_repos_with_license(self):
        """Test the public_repos method with a license filter."""
        client = GithubOrgClient("mock-org")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
        self.mock_get_json.assert_called()
