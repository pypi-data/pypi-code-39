# coding: utf-8

"""
    Pulp 3 API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: v3
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest

import pulpcore.client.pulpcore
from pulpcore.client.pulpcore.api.repositories_api import RepositoriesApi  # noqa: E501
from pulpcore.client.pulpcore.rest import ApiException


class TestRepositoriesApi(unittest.TestCase):
    """RepositoriesApi unit test stubs"""

    def setUp(self):
        self.api = pulpcore.client.pulpcore.api.repositories_api.RepositoriesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create(self):
        """Test case for create

        Create a repository  # noqa: E501
        """
        pass

    def test_delete(self):
        """Test case for delete

        Delete a repository  # noqa: E501
        """
        pass

    def test_list(self):
        """Test case for list

        List repositories  # noqa: E501
        """
        pass

    def test_partial_update(self):
        """Test case for partial_update

        Partially update a repository  # noqa: E501
        """
        pass

    def test_read(self):
        """Test case for read

        Inspect a repository  # noqa: E501
        """
        pass

    def test_update(self):
        """Test case for update

        Update a repository  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
