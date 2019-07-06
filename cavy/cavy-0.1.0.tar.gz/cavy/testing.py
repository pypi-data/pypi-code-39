import logging
import os
import unittest


class EnvironmentMixin(unittest.TestCase):
    """Adds safe environment variable manipulation.

    Use this instead of manipulating :data:`os.environ` or calling
    :meth:`os.setenv` directly.  Failing to do so may cause strange
    test failures when environment variables leak between test
    cases.

    """

    def setUp(self):
        super().setUp()
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__saved_vars = {}

    def tearDown(self):
        """Automatically reset the environment during test clenaup."""
        super().tearDown()
        self.reset_environment()

    def reset_environment(self):
        """Undo changes to the environment."""
        for name, value in self.__saved_vars.items():
            os.environ.pop(name, None)
            if value is not None:
                os.environ[name] = value
        self.__saved_vars.clear()

    def setenv(self, name, value):
        """Set an environment variable.

        :param str name: names the environment variable to set
        :param str value: value to store in the environment

        """
        self.__logger.getChild('setenv').info('setting %s=%s', name, value)
        self.__saved_vars.setdefault(name, os.environ.get(name))
        os.environ[name] = value

    def unsetenv(self, name):
        """Clear an environment variable.

        :param str name: names the environment variable to clear

        """
        self.__logger.getChild('unsetenv').info('clearing %s', name)
        self.__saved_vars.setdefault(name, os.environ.get(name))
        os.environ.pop(name, None)


class PEP8NamingMixin(unittest.TestCase):
    """PEP8 compliant names for assertions.

    Mix this class in over :class:`unittest.TestCase` to provide
    :pep:`8` compliant names for the assertions.  This makes it possible
    to write tests that look like::

        class MyTest(PEP8AssertionsMixin, unittest.TestCase):
            def test_something(self):
                self.assert_equal(1, 2)

    instead of::

        class MyTest(PEP8AssertionsMixin, unittest.TestCase):
            def test_something(self):
                self.assertEqual(1, 2)

    It is a small thing but the non-PEP8 names in unittest have
    always bothered me.

    """

    def assert_false(self, expr, msg=None):
        self.assertFalse(expr, msg)

    def assert_true(self, expr, msg=None):
        self.assertTrue(expr, msg)

    def assert_raises(self, expected_exception, *args, **kwargs):
        return self.assertRaises(expected_exception, *args, **kwargs)

    def assert_warns(self, expected_warning, *args, **kwargs):
        return self.assertWarns(expected_warning, *args, **kwargs)

    def assert_logs(self, logger=None, level=None):
        return self.assertLogs(logger, level)

    def assert_equal(self, first, second, msg=None):
        self.assertEqual(first, second, msg)

    def assert_not_equal(self, first, second, msg=None):
        self.assertNotEqual(first, second, msg)

    def assert_almost_equal(self,
                            first,
                            second,
                            places=None,
                            msg=None,
                            delta=None):
        self.assertAlmostEqual(first, second, places, msg, delta)

    def assert_not_almost_equal(self,
                                first,
                                second,
                                places=None,
                                msg=None,
                                delta=None):
        self.assertNotAlmostEqual(first, second, places, msg, delta)

    def assert_sequence_equal(self, seq1, seq2, msg=None, seq_type=None):
        self.assertSequenceEqual(seq1, seq2, msg, seq_type)

    def assert_list_equal(self, list1, list2, msg=None):
        self.assertListEqual(list1, list2, msg)

    def assert_tuple_equal(self, tuple1, tuple2, msg=None):
        self.assertTupleEqual(tuple1, tuple2, msg)

    def assert_set_equal(self, set1, set2, msg=None):
        self.assertSetEqual(set1, set2, msg)

    def assert_in(self, member, container, msg=None):
        self.assertIn(member, container, msg)

    def assert_not_in(self, member, container, msg=None):
        self.assertNotIn(member, container, msg)

    def assert_is(self, expr1, expr2, msg=None):
        self.assertIs(expr1, expr2, msg)

    def assert_is_not(self, expr1, expr2, msg=None):
        self.assertIsNot(expr1, expr2, msg)

    def assert_dict_equal(self, d1, d2, msg=None):
        self.assertDictEqual(d1, d2, msg)

    def assert_count_equal(self, first, second, msg=None):
        self.assertCountEqual(first, second, msg)

    def assert_multi_line_equal(self, first, second, msg=None):
        self.assertMultiLineEqual(first, second, msg)

    def assert_less(self, a, b, msg=None):
        self.assertLess(a, b, msg)

    def assert_less_equal(self, a, b, msg=None):
        self.assertLessEqual(a, b, msg)

    def assert_greater(self, a, b, msg=None):
        self.assertGreater(a, b, msg)

    def assert_greater_equal(self, a, b, msg=None):
        self.assertGreaterEqual(a, b, msg)

    def assert_is_none(self, obj, msg=None):
        self.assertIsNone(obj, msg)

    def assert_is_not_none(self, obj, msg=None):
        self.assertIsNotNone(obj, msg)

    def assert_is_instance(self, obj, cls, msg=None):
        self.assertIsInstance(obj, cls, msg)

    def assert_not_is_instance(self, obj, cls, msg=None):
        self.assertNotIsInstance(obj, cls, msg)

    def assert_raises_regex(self, expected_exception, expected_regex, *args,
                            **kwargs):
        return self.assertRaisesRegex(expected_exception, expected_regex,
                                      *args, **kwargs)

    def assert_warns_regex(self, expected_warning, expected_regex, *args,
                           **kwargs):
        return self.assertWarnsRegex(expected_warning, expected_regex, *args,
                                     **kwargs)

    def assert_regex(self, text, expected_regex, msg=None):
        self.assertRegex(text, expected_regex, msg)

    def assert_not_regex(self, text, unexpected_regex, msg=None):
        self.assertNotRegex(text, unexpected_regex, msg)


class AdditionalAssertionsMixin(unittest.TestCase):
    """Useful assertions that aren't in the Standard Library.

    This mix-in includes some assertions that I've found myself
    wishing were part of the Standard Library from time to time.

    """

    def assert_between(self, value, low, high, msg=None):
        """Assert that `value` is between `low` and `high`.

        :param value: value to compare
        :param low: inclusive low range endpoint
        :param high: inclusive high range endpoint
        :param str msg: optional message to use on failure

        """
        if msg is None:
            self.longMessage = False
            msg = '{!r} is not between {!r} and {!r}'.format(value, low, high)
        self.assertGreaterEqual(value, low, msg=msg)
        self.assertLessEqual(value, high, msg=msg)

    def assert_startswith(self, value, prefix, msg=None):
        """Assert that `prefix` is a prefix of `value`.

        :param value: value to check
        :param prefix: sequence of values that `value` should start with.
        :param str msg: optional message to use on failure

        Note that `value` and `prefix` ARE NOT required to be of the
        same type.  The only requirement is that they are ordered
        sequences of the same underlying type.

        """
        if msg is None:
            msg = '{!r} does not start with {!r}'.format(value, prefix)
        if len(prefix) > len(value):
            self.fail(msg)
        for a, b in zip(value, prefix):
            if a != b:
                self.fail(msg)

    def assert_endswith(self, value, suffix, msg=None):
        """Assert that `suffix` is a suffix of `value`.

        :param value: value to check
        :param suffix: sequence of values that `value` should end with
        :param str msg: optional message to use on failure

        Note that `value` and `suffix` ARE NOT required to be of the
        same type.  They are required to be reversible sequences of the
        same underlying type.

        """
        if msg is None:
            msg = '{!r} does not end with {!r}'.format(value, suffix)
        if len(suffix) > len(value):
            raise AssertionError(msg)
        for a, b in zip(reversed(value), reversed(suffix)):
            if a != b:
                raise AssertionError(msg)
