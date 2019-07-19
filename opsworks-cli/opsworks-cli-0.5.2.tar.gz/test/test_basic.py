#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# AWS OpsWorks deployment cli - Unittest for python34 and up
# Ref - https://stackoverflow.com/questions/4219717/how-to-assert-output-with-nosetest-unittest-in-python
# Unit testing basic fuctions of the modules

import sys
import unittest
import contextlib
from io import StringIO
import modules

region = 'eu-west-1'
stack = '2e7f6dd5-e4a3-4389-bc95-b4bacc234df0'
layer = 'ac0df176-104b-46ae-946e-7cf7367b816e'
app = '2da891ea-1809-480d-a799-cb2c08746115'
cookbook = 'apache2::default'
custom_json = '{"default": "version"}'
instances = 2
deploymentid = '2e7f6dd5e4a34389bc95b4bacc234df0'
name = 'setup'
name2 = 'update_custom_cookbooks'


class Case(unittest.TestCase):
    if sys.version_info >= (3, 4):
        def test_execute_recipes1(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.execute_recipes(region=region, stack=stack, cookbook=cookbook)
            output = usage_stdout.getvalue().strip()
            self.assertIn('execute_recipes main function testing', output)

        def test_execute_recipes2(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.execute_recipes(region=region, stack=stack, cookbook=cookbook, layer=layer)
            output = usage_stdout.getvalue().strip()
            self.assertIn('execute_recipes main function testing', output)

        def test_execute_recipes3(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.execute_recipes(region=region, stack=stack, cookbook=cookbook, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('execute_recipes main function testing', output)

        def test_execute_recipes4(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.execute_recipes(region=region, stack=stack, cookbook=cookbook, layer=layer, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('execute_recipes main function testing', output)

        def test_run_recipes_without_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.run_recipes_without_layer(region=region, stack=stack, cookbook=cookbook, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('run_recipes_without_layer sub function', output)

        def test_run_recipes_without_layer2(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.run_recipes_without_layer(region=region, stack=stack, cookbook=cookbook)
            output = usage_stdout.getvalue().strip()
            self.assertIn('run_recipes_without_layer sub function', output)

        def test_run_recipes_with_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.run_recipes_with_layer(region=region, stack=stack, layer=layer, cookbook=cookbook, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('run_recipes_with_layer sub function', output)

        def test_run_recipes_with_layer2(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.run_recipes_with_layer(region=region, stack=stack, layer=layer, cookbook=cookbook)
            output = usage_stdout.getvalue().strip()
            self.assertIn('run_recipes_with_layer sub function', output)

        def test_run_update_custom_cookbook(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.update_custom_cookbooks(region=region, stack=stack, layer=layer)
            output = usage_stdout.getvalue().strip()
            self.assertIn('update_custom_cookbooks main function testing', output)

        def test_run_update_custom_cookbooks_with_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.update_custom_cookbooks_with_layer(region=region, stack=stack, layer=layer)
            output = usage_stdout.getvalue().strip()
            self.assertIn('update_custom_cookbooks_with_layer sub function testing', output)

        def test_run_update_custom_cookbooks_without_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.update_custom_cookbooks_without_layer(region=region, stack=stack)
            output = usage_stdout.getvalue().strip()
            self.assertIn('update_custom_cookbooks_without_layer sub function testing', output)

        def test_run_setup(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.setup(region=region, stack=stack, layer=layer)
            output = usage_stdout.getvalue().strip()
            self.assertIn('setup main function testing', output)

        def test_run_setup_with_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.setup_with_layer(region=region, stack=stack, layer=layer)
            output = usage_stdout.getvalue().strip()
            self.assertIn('setup_with_layer sub function testing', output)

        def test_run_setup_without_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.setup_without_layer(region=region, stack=stack)
            output = usage_stdout.getvalue().strip()
            self.assertIn('setup_without_layer sub function testing', output)

        def test_run_deploy(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.deploy(region=region, stack=stack, layer=layer, app=app, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('deploy main function', output)

        def test_run_deploy_json(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.deploy(region=region, stack=stack, layer=layer, app=app)
            output = usage_stdout.getvalue().strip()
            self.assertIn('deploy main function', output)

        def test_run_deploy_json2(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.deploy(region=region, stack=stack, app=app, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('deploy main function', output)

        def test_run_deploy_with_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.deploy_with_layer(region=region, stack=stack, layer=layer, app=app, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('deploy_with_layer sub function', output)

        def test_run_deploy_with_layer2(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.deploy_with_layer(region=region, stack=stack, layer=layer, app=app)
            output = usage_stdout.getvalue().strip()
            self.assertIn('deploy_with_layer sub function', output)

        def test_run_deploy_without_layer(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.deploy_without_layer(region=region, stack=stack, app=app, custom_json=custom_json)
            output = usage_stdout.getvalue().strip()
            self.assertIn('deploy_without_layer sub function', output)

        def test_run_deploy_without_layer2(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.deploy_without_layer(region=region, stack=stack, app=app)
            output = usage_stdout.getvalue().strip()
            self.assertIn('deploy_without_layer sub function', output)

        def test_run_getnames(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.common_functions.get_names(stack=stack, layer=layer, region=region, name=name)
            output = usage_stdout.getvalue().strip()
            self.assertIn('setup', output)

        def test_run_getnames2(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.common_functions.get_names(stack=stack, layer=layer, region=region, name=name2)
            output = usage_stdout.getvalue().strip()
            self.assertIn('update_custom_cookbook', output)

        def test_run_getstatus(self):
            usage_stdout = StringIO()
            with contextlib.redirect_stdout(usage_stdout):
                modules.common_functions.get_status(deploymentid=deploymentid, region=region, instances=instances)
            output = usage_stdout.getvalue().strip()
            self.assertIn('2e7f6dd5e4a34389bc95b4bacc234df0', output)

        def test_summary(self):
            summary_stdout = StringIO()
            with contextlib.redirect_stdout(summary_stdout):
                modules.common_functions.summary(100, 50, 10)
            output = summary_stdout.getvalue().strip()
            self.assertIn('Success', output)

        def test_summary_fail_skipped(self):
            summary_stdout = StringIO()
            with contextlib.redirect_stdout(summary_stdout):
                modules.common_functions.summary_fail_skipped(100, 50, 10)
            output = summary_stdout.getvalue().strip()
            self.assertIn('Success', output)

        def test_get_status_instances_main(self):
            summary_stdout = StringIO()
            with contextlib.redirect_stdout(summary_stdout):
                modules.common_functions.get_status_instances_main(region=region, deploymentid=deploymentid, instances=instances, success_count=2, failed_count=1, skipped_count=0)
            output = summary_stdout.getvalue().strip()
            self.assertIn('get_status_instances_main', output)

        def test_get_status_instances_sub(self):
            summary_stdout = StringIO()
            with contextlib.redirect_stdout(summary_stdout):
                modules.common_functions.get_status_instances_sub(region=region, deploymentid=deploymentid, instances=instances, success_count=5, fail_skip_count=2, success_fail_count=0)
            output = summary_stdout.getvalue().strip()
            self.assertIn('get_status_instances_sub', output)

        def test_deploy_test_output_summary(self):
            summary_stdout = StringIO()
            with contextlib.redirect_stdout(summary_stdout):
                modules.test_output_summary(region=region, stack=stack, layer=layer, app=app, custom_json=None)
            output = summary_stdout.getvalue().strip()
            self.assertIn(stack, output)

    else:
        print('python version lowerthan 3.4')


if __name__ == '__main__':
    unittest.main()
