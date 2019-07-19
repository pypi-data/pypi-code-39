#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# Boto3 mock unit tests - common functions

from mock import patch
import json
import unittest
import modules


class Case(unittest.TestCase):
    def test_get_status_success(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_success.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status('DEPLOYMENTID', 'REGION', '0')
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_skipped(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_skipped.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status('DEPLOYMENTID', 'REGION', '0')
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_failed(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_failed.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status('DEPLOYMENTID', 'REGION', '0')
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_success_skip(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_success_skiped.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status('DEPLOYMENTID', 'REGION', '0')
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_success_failed(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_success_failed.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status('DEPLOYMENTID', 'REGION', '0')
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_failed_skipped(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_failed_skipped.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status('DEPLOYMENTID', 'REGION', '0')
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_instances_sub_fail_skip_count(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_failed_skipped.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status_instances_sub('REGION', 'DEPLOYMENTID', 2, 0, 2, 1)
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_instances_sub_success_fail_count(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_success_failed.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status_instances_sub('REGION', 'DEPLOYMENTID', 2, 1, 1, 1)
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_instances_main_success_count(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_success.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status_instances_main('REGION', 'DEPLOYMENTID', 1, 1, 0, 0)
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_instances_main_skipped_count(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_skipped.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status_instances_main('REGION', 'DEPLOYMENTID', 1, 0, 1, 0)
                    self.assertEqual(mock_client.call_count, 1)

    def test_get_status_instances_main_failed_count(self):
        with patch('boto3.client') as mock_client:
            with patch('boto3.client.describe_commands') as boto_describe_commands:
                with open('test/json_data/describe_commands_failed.json') as json_file:
                    data = json.load(json_file)
                    boto_describe_commands.return_value = data
                    modules.get_status_instances_main('REGION', 'DEPLOYMENTID', 1, 0, 0, 1)
                    self.assertEqual(mock_client.call_count, 1)


if __name__ == '__main__':
    unittest.main()
