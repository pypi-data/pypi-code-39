#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# Boto3 mock unit tests - execute recipes

from mock import patch
import json
import unittest
import modules


class Case(unittest.TestCase):
    def test_execute_recipes_without_layer(self):
        with patch('boto3.client') as mock_client:
            modules.run_recipes_without_layer('eu-west-1', 'STACKID', 'COOKBOOK')
            self.assertEqual(mock_client.call_count, 2)

    def test_execute_recipes_without_layer_json(self):
        with patch('boto3.client') as mock_client:
            modules.run_recipes_without_layer('eu-west-1', 'STACKID', 'COOKBOOK', 'CUSTOMJSON')
            self.assertEqual(mock_client.call_count, 2)

    def test_execute_recipes_with_layer(self):
        with patch('boto3.client') as mock_client:
            modules.run_recipes_with_layer('eu-west-1', 'STACKID', 'LAYERID', 'COOKBOOK')
            self.assertEqual(mock_client.call_count, 2)

    def test_execute_recipes_with_layer_json(self):
        with patch('boto3.client') as mock_client:
            modules.run_recipes_with_layer('eu-west-1', 'STACKID', 'LAYERID', 'COOKBOOK', 'CUSTOMJSON')
            self.assertEqual(mock_client.call_count, 2)

    def test_execute_recipes_layer(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.create_deployment') as boto_create_deployment:
                with patch('boto3.client.describe_instances') as boto_describe_instances:
                    with open('test/json_data/describe_instances.json') as json_file:
                        data = json.load(json_file)
                        boto_create_deployment.return_value = "{ 'DeploymentId': 'DEPLOYMENTID' }"
                        boto_describe_instances.return_value = data
                        modules.execute_recipes('eu-west-1', 'STACKID', 'COOKBOOK', layer='LAYERID', custom_json='CUSTOMJSON')
                        self.assertEqual(mock_client.call_count, 3)

    def test_execute_recipes(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.create_deployment') as boto_create_deployment:
                with patch('boto3.client.describe_instances') as boto_describe_instances:
                    with open('test/json_data/describe_instances.json') as json_file:
                        data = json.load(json_file)
                        boto_create_deployment.return_value = "{ 'DeploymentId': 'DEPLOYMENTID' }"
                        boto_describe_instances.return_value = data
                        modules.execute_recipes('eu-west-1', 'STACKID', 'COOKBOOK', custom_json='CUSTOMJSON')
                        self.assertEqual(mock_client.call_count, 3)


if __name__ == '__main__':
    unittest.main()
