import unittest

from cavy import testing


class MixinTestCase(testing.AdditionalAssertionsMixin, unittest.TestCase):
    pass


class AdditionalAssertsTests(unittest.TestCase):
    def test_assert_between(self):
        test = MixinTestCase()
        with self.assertRaisesRegex(AssertionError,
                                    r'1 is not between 2 and 3'):
            test.assert_between(1, 2, 3)

        with self.assertRaisesRegex(AssertionError, 'foo'):
            test.assert_between(4, 2, 3, msg='foo')

    def test_assert_startswith(self):
        test = MixinTestCase()
        test.assert_startswith([1, 2, 3], (1, 2))
        test.assert_startswith('prefixed string', 'prefix')

        with self.assertRaisesRegex(
                AssertionError,
                r"'prefixed string' does not start with 'suffix'"):
            test.assert_startswith('prefixed string', 'suffix')
        with self.assertRaisesRegex(
                AssertionError,
                r'\[1, 2, 3, 4\] does not start with \[1, 1\]'):
            test.assert_startswith([1, 2, 3, 4], [1, 1])
        with self.assertRaisesRegex(
                AssertionError, r'\[1, 2\] does not start with \(1, 2, 3\)'):
            test.assert_startswith([1, 2], (1, 2, 3))
        with self.assertRaisesRegex(AssertionError, r'foo'):
            test.assert_startswith([1, 2], [1, 2, 3], msg='foo')

    def test_assert_endswith(self):
        test = MixinTestCase()
        test.assert_endswith([1, 2, 3], (2, 3))
        test.assert_endswith('string with suffix', 'suffix')

        with self.assertRaisesRegex(
                AssertionError,
                r"'string with suffix' does not end with 'not suffix'"):
            test.assert_endswith('string with suffix', 'not suffix')
        with self.assertRaisesRegex(
                AssertionError, r'\[1, 2, 3, 4\] does not end with \[1, 1\]'):
            test.assert_endswith([1, 2, 3, 4], [1, 1])
        with self.assertRaisesRegex(AssertionError,
                                    r'\[1, 2\] does not end with \(1, 2, 3\)'):
            test.assert_endswith([1, 2], (1, 2, 3))
        with self.assertRaisesRegex(AssertionError, r'foo'):
            test.assert_endswith({1: '1', 2: '2'}, [1, 2, 3], msg='foo')
