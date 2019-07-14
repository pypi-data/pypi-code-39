import os
import unittest
import uuid

from cavy import testing


class MixinTestCase(testing.EnvironmentMixin, unittest.TestCase):
    pass


class EnvironmentMixinTests(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.env_vars = {
            'one': str(uuid.uuid4()),
            'two': str(uuid.uuid4()),
            'three': None,
        }
        self._saved_env = {}
        for name, value in self.env_vars.items():
            self._saved_env[name] = os.environ.pop(name, None)
            if value is not None:
                os.environ[name] = value

    def tearDown(self):
        super().tearDown()
        for name, value in self._saved_env.items():
            os.environ.pop(name, None)
            if value is not None:
                os.environ[name] = value

    def test_that_environment_variables_are_saved(self):
        test = MixinTestCase()
        test.setUp()
        test.setenv('one', '1234')
        test.unsetenv('two')
        test.setenv('three', 'whatever')
        test.tearDown()

        self.assertEqual(self.env_vars['one'], os.environ.get('one'))
        self.assertEqual(self.env_vars['two'], os.environ.get('two'))
        self.assertIsNone(os.environ.get('three'))
