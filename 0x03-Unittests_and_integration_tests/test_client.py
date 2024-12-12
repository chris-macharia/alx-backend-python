#!/usr/bin/env python3

"""A GitHub org client."""
from typing import (
    List,
    Dict,
)

from utils import (
    get_json,
    access_nested_map,
    memoize,
)

import requests

def get_json(url: str) -> Dict:
    """Fetch JSON data from a given URL.

    Args:
        url (str): The URL to fetch data from.

    Returns:
        Dict: The JSON response as a dictionary.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

class GithubOrgClient:
    """A GitHub organization client."""

    ORG_URL = "https://api.github.com/orgs"

    def __init__(self, org_name: str) -> None:
        """Initialize the GitHubOrgClient instance.

        Args:
            org_name (str): The name of the GitHub organization.
        """
        self._org_name = org_name

    @memoize
    def org(self) -> Dict:
        """Fetch and memoize the organization details.

        Returns:
            Dict: The organization details.
        """
        return get_json(self.ORG_URL.format(org=self._org_name))

    @property
    def _public_repos_url(self) -> str:
        """Retrieve the public repositories URL.

        Returns:
            str: The URL for the organization's public repositories.
        """
        return self.org["repos_url"]

    @memoize
    def repos_payload(self) -> Dict:
        """Fetch and memoize the repositories payload.

        Returns:
            Dict: The repositories payload.
        """
        return get_json(self._public_repos_url)

    def public_repos(self, license: str = None) -> List[str]:
        """Retrieve the list of public repositories.

        Args:
            license (str, optional): Filter repositories by license key. Defaults to None.

        Returns:
            List[str]: A list of repository names.
        """
        json_payload = self.repos_payload
        public_repos = [
            repo["name"] for repo in json_payload
            if license is None or self.has_license(repo, license)
        ]

        return public_repos

    @staticmethod
    def has_license(repo: Dict[str, Dict], license_key: str) -> bool:
        """Check if a repository has a specific license.

        Args:
            repo (Dict[str, Dict]): The repository data.
            license_key (str): The license key to check for.

        Returns:
            bool: True if the repository has the license, False otherwise.
        """
        assert license_key is not None, "license_key cannot be None"
        try:
            has_license = access_nested_map(repo, ("license", "key")) == license_key
        except KeyError:
            return False
        return has_license

    def get_org(self) -> Dict:
        """Fetch the details of the organization.

        Returns:
            Dict: The organization details.
        """
        url = f"{self.ORG_URL}/{self._org_name}"
        return get_json(url)
