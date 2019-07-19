#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# Boto3 mock unit tests - deploy

from mock import patch
import json
import unittest
import modules


class Case(unittest.TestCase):
    def test_deploy_without_layer(self):
        with patch('boto3.client') as mock_client:
            modules.deploy_without_layer('eu-west-1', 'STACKID', 'APPID')
            self.assertEqual(mock_client.call_count, 2)

    def test_deploy_without_layer_json(self):
        with patch('boto3.client') as mock_client:
            modules.deploy_without_layer('eu-west-1', 'STACKID', 'APPID', 'CUSTOMJSON')
            self.assertEqual(mock_client.call_count, 2)

    def test_deploy_without_layer_json2(self):
        with patch('boto3.client') as mock_client:
            modules.deploy_without_layer('eu-west-1', 'STACKID', 'APPID', custom_json='')
            self.assertEqual(mock_client.call_count, 2)

    def test_deploy_with_layer(self):
        with patch('boto3.client') as mock_client:
            modules.deploy_with_layer('eu-west-1', 'STACKID', 'LAYERID', 'APPID')
            self.assertEqual(mock_client.call_count, 2)

    def test_deploy_with_layer_json(self):
        with patch('boto3.client') as mock_client:
            modules.deploy_with_layer('eu-west-1', 'STACKID', 'LAYERID', 'APPID', 'CUSTOMJSON')
            self.assertEqual(mock_client.call_count, 2)

    def test_deploy_with_layer_json2(self):
        with patch('boto3.client') as mock_client:
            modules.deploy_with_layer('eu-west-1', 'STACKID', 'LAYERID', 'APPID', custom_json='')
            self.assertEqual(mock_client.call_count, 2)

    def test_deploy_layer(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.create_deployment') as boto_create_deployment:
                with patch('boto3.client.describe_instances') as boto_describe_instances:
                    with open('test/json_data/describe_instances.json') as json_file:
                        data = json.load(json_file)
                        boto_create_deployment.return_value = "{ 'DeploymentId': 'DEPLOYMENTID' }"
                        boto_describe_instances.return_value = data
                        modules.deploy('eu-west-1', 'STACKID', 'APPID', layer=None)
                        self.assertEqual(mock_client.call_count, 3)

    def test_deploy(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.create_deployment') as boto_create_deployment:
                with patch('boto3.client.describe_instances') as boto_describe_instances:
                    with open('test/json_data/describe_instances.json') as json_file:
                        data = json.load(json_file)
                        boto_create_deployment.return_value = "{ 'DeploymentId': 'DEPLOYMENTID' }"
                        boto_describe_instances.return_value = data
                        modules.deploy('eu-west-1', 'STACKID', 'LAYERID', 'APPID')
                        self.assertEqual(mock_client.call_count, 3)


if __name__ == '__main__':
    unittest.main()
