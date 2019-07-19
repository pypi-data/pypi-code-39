#!/usr/bin/env python
# Copyright 2018 Chathuranga Abeyrathna. All Rights Reserved.
# AWS OpsWorks deployment cli - Unittest for python2
# Unit testing basic fuctions of the modules - Python2

import unittest
import logging
import sys
import modules.execute_recipes

if sys.version_info < (3, 3):
    import StringIO

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


class Case2(unittest.TestCase):
    if sys.version_info < (3, 3):
        def test_execute_recipes1(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.execute_recipes(region=region, stack=stack, cookbook=cookbook)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('execute_recipes main function testing', s.read())

        def test_execute_recipes2(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.execute_recipes(region=region, stack=stack, cookbook=cookbook, layer=layer)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('execute_recipes main function testing', s.read())

        def test_execute_recipes3(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.execute_recipes(region=region, stack=stack, cookbook=cookbook, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('execute_recipes main function testing', s.read())

        def test_execute_recipes4(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.execute_recipes(region=region, stack=stack, cookbook=cookbook, layer=layer, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('execute_recipes main function testing', s.read())

        def test_run_recipes_without_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.run_recipes_without_layer(region=region, stack=stack, cookbook=cookbook, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('run_recipes_without_layer sub function', s.read())

        def test_run_recipes_without_layer2(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.run_recipes_without_layer(region=region, stack=stack, cookbook=cookbook)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('run_recipes_without_layer sub function', s.read())

        def run_recipes_with_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.run_recipes_with_layer(region=region, stack=stack, layer=layer, cookbook=cookbook, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('run_recipes_with_layer sub function', s.read())

        def run_recipes_with_layer2(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.run_recipes_with_layer(region=region, stack=stack, layer=layer, cookbook=cookbook)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('run_recipes_with_layer sub function', s.read())

        def test_run_update_custom_cookbook(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.update_custom_cookbooks(region=region, stack=stack, layer=layer)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('update_custom_cookbooks main function testing', s.read())

        def test_run_update_custom_cookbooks_with_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.update_custom_cookbooks_with_layer(region=region, stack=stack, layer=layer)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('update_custom_cookbooks_with_layer sub function testing', s.read())

        def test_run_update_custom_cookbooks_without_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.update_custom_cookbooks_without_layer(region=region, stack=stack)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('update_custom_cookbooks_without_layer sub function testing', s.read())

        def test_run_setup(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.setup(region=region, stack=stack, layer=layer)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('setup main function testing', s.read())

        def test_run_setup_with_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.setup_with_layer(region=region, stack=stack, layer=layer)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('setup_with_layer sub function testing', s.read())

        def test_run_setup_without_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.setup_without_layer(region=region, stack=stack)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('setup_without_layer sub function testing', s.read())

        def test_run_deploy(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.deploy(region=region, stack=stack, layer=layer, app=app, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('deploy main function', s.read())

        def test_run_deploy_json(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.deploy(region=region, stack=stack, layer=layer, app=app)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('deploy main function', s.read())

        def test_run_deploy_json2(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.deploy(region=region, stack=stack, app=app, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('deploy main function', s.read())

        def test_run_deploy_with_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.deploy_with_layer(region=region, stack=stack, layer=layer, app=app, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('deploy_with_layer sub function', s.read())

        def test_run_deploy_with_layer2(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.deploy_with_layer(region=region, stack=stack, layer=layer, app=app)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('deploy_with_layer sub function', s.read())

        def test_run_deploy_without_layer(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.deploy_without_layer(region=region, stack=stack, app=app, custom_json=custom_json)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('deploy_without_layer sub function', s.read())

        def test_run_deploy_without_layer2(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.deploy_without_layer(region=region, stack=stack, app=app)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('deploy_without_layer sub function', s.read())

        def test_run_getnames(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.common_functions.get_names(stack=stack, layer=layer, region=region, name=name)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('setup', s.read())

        def test_run_getnames2(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.common_functions.get_names(stack=stack, layer=layer, region=region, name=name2)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('update_custom_cookbook', s.read())

        def test_run_getstatus(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.common_functions.get_status(deploymentid=deploymentid, region=region, instances=instances)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('2e7f6dd5e4a34389bc95b4bacc234df0', s.read())

        def test_summary(self):
            stdout = sys.stdout
            s = StringIO.StringIO()
            sys.stdout = s
            modules.common_functions.summary(100, 50, 10)
            sys.stdout = stdout
            s.seek(0)
            self.assertIn('Success', s.read())
    else:
        print('python version is higher than 3.4')


if __name__ == '__main__':
    unittest.main()
