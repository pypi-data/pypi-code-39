import unittest

from cavy import testing

state = {}


def f(*args, **kwargs):
    state['called'] = True


class MixinTestCase(testing.PatchingMixin, unittest.TestCase):
    def call_function(self, *args, **kwargs):
        f(*args, **kwargs)


class PatchingMixinTests(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.test = MixinTestCase()
        self.test.setUp()

    def tearDown(self):
        super().tearDown()
        self.test.tearDown()

    def test_that_patches_are_started(self):
        state['called'] = False
        self.test.patch('tests.test_patching_mixin.f')
        self.test.call_function()
        self.assertFalse(state['called'])

    def test_that_patcher_instance_is_returned(self):
        patched = self.test.patch('tests.test_patching_mixin.f')
        self.test.call_function()
        patched.assert_called_once_with()

    def test_that_teardown_stops_patch(self):
        self.test.patch('tests.test_patching_mixin.f')
        self.test.tearDown()
        self.test.call_function()
        self.assertTrue(state['called'])
