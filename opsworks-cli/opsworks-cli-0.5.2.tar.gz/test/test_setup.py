#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# Boto3 mock unit tests - setup

from mock import patch
import json
import unittest
import modules


class Case(unittest.TestCase):
    def test_setup_without_layer(self):
        with patch('boto3.client') as mock_client:
            modules.setup_without_layer('eu-west-1', 'STACKID')
            self.assertEqual(mock_client.call_count, 2)

    def test_setup_with_layer(self):
        with patch('boto3.client') as mock_client:
            modules.setup_with_layer('eu-west-1', 'STACKID', 'LAYERID')
            self.assertEqual(mock_client.call_count, 2)

    def test_setup_layer(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.create_deployment') as boto_create_deployment:
                with patch('boto3.client.describe_instances') as boto_describe_instances:
                    with open('test/json_data/describe_instances.json') as json_file:
                        data = json.load(json_file)
                        boto_create_deployment.return_value = "{ 'DeploymentId': 'DEPLOYMENTID' }"
                        boto_describe_instances.return_value = data
                        modules.setup('eu-west-1', 'STACKID', layer=None)
                        self.assertEqual(mock_client.call_count, 3)

    def test_setup(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.create_deployment') as boto_create_deployment:
                with patch('boto3.client.describe_instances') as boto_describe_instances:
                    with open('test/json_data/describe_instances.json') as json_file:
                        data = json.load(json_file)
                        boto_create_deployment.return_value = "{ 'DeploymentId': 'DEPLOYMENTID' }"
                        boto_describe_instances.return_value = data
                        modules.setup('eu-west-1', 'STACKID', 'LAYERID')
                        self.assertEqual(mock_client.call_count, 3)


if __name__ == '__main__':
    unittest.main()
