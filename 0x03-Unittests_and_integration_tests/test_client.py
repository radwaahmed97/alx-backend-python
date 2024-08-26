#!/usr/bin/env python3
"""contains TestGithubOrgClient testclass"""

import unittest
from unittest.mock import (
    MagicMock,
    Mock,
    PropertyMock,
    patch,
)
from parameterized import parameterized, parameterized_class
from client import (
    GithubOrgClient
)
from fixtures import TEST_PAYLOAD
from typing import Dict


class TestGithubOrgClient(unittest.TestCase):
    """TestGithubOrgClient test class"""
    @patch(
        "client.get_json",
    )
    @parameterized.expand([
        ("google", {'login': "google"}),
        ("abc", {'login': "abc"}),
    ])
    def test_org(self, org: str, expected_result: Dict,
                 Mocked_func: MagicMock) -> None:
        """method tests GithubOrgClient.org returns the correct value"""
        Mocked_func.return_value = MagicMock(
            return_value=expected_result)
        goclientobj = GithubOrgClient(org)
        self.assertEqual(goclientobj.org(), expected_result)
        Mocked_func.assert_called_once_with(
            "https://api.github.com/orgs/{}".format(org)
        )

    def test_public_repos_url(self) -> None:
        """method tests unit-test GithubOrgClient._public_repos_url"""
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {
                'repos_url': "https://api.github.com/users/google/repos",
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                "https://api.github.com/users/google/repos",
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """
        method testing list of repos as expected and
        mocked property called once
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 7776515,
                    "name": "cpp-netlib",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": True,
                    "url": "https://api.github.com/repos/google/cpp-netlib",
                    "created_at": "2013-01-23T14:45:32Z",
                    "updated_at": "2019-11-15T02:26:31Z",
                    "has_issues": False,
                    "forks": 59,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "cpp-netlib",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "apache-2.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests the `has_license` method."""
        gh_org_client = GithubOrgClient("google")
        client_has_licence = gh_org_client.has_license(repo, key)
        self.assertEqual(client_has_licence, expected)


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """_summary_

    Args:
            unittest (_type_): _description_

    Returns:
            _type_: _description_
    """
    @classmethod
    def setUpClass(cls) -> None:
        """_summary_

        Returns:
                _type_: _description_
        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """_summary_
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """_summary_
        """
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """_summary_
        """
        cls.get_patcher.stop()
