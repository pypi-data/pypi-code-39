import logging
import unittest
import uuid
import warnings

from cavy import testing


class MixinTestCase(testing.PEP8NamingMixin, unittest.TestCase):
    pass


class PEP8MixinTests(unittest.TestCase):
    def verify_assertion(self, method_name, *args, **kwargs):
        msg = str(uuid.uuid4())

        test = MixinTestCase()
        method = getattr(test, method_name)
        with self.assertRaises(AssertionError):
            method(*args, **kwargs)

        with self.assertRaises(AssertionError) as context:
            method(*args, msg=msg, **kwargs)
        self.assertIn(msg, str(context.exception))

    def test_simple_assertions(self):
        self.verify_assertion('assert_false', True)
        self.verify_assertion('assert_true', False)
        self.verify_assertion('assert_equal', 1, 2)
        self.verify_assertion('assert_not_equal', 1, 1)
        self.verify_assertion('assert_almost_equal', 1, 2)
        self.verify_assertion('assert_not_almost_equal', 0.1, 0.11, places=1)
        self.verify_assertion('assert_in', 'foo', 'hello world')
        self.verify_assertion('assert_not_in', 'foo', 'foobar')
        self.verify_assertion('assert_is', object(), object())
        self.verify_assertion('assert_is_not', None, None)
        self.verify_assertion('assert_less', 2, 1)
        self.verify_assertion('assert_less_equal', 2, 1)
        self.verify_assertion('assert_greater', 1, 2)
        self.verify_assertion('assert_greater_equal', 1, 2)
        self.verify_assertion('assert_is_none', 'NotNone')
        self.verify_assertion('assert_is_not_none', None)
        self.verify_assertion('assert_is_instance', 1, str)
        self.verify_assertion('assert_not_is_instance', 1, int)
        self.verify_assertion('assert_regex', 'foo', r'foo[bB]ar')
        self.verify_assertion('assert_not_regex', 'foobar', r'foo[bB]ar')

    def test_datatype_assertions(self):
        self.verify_assertion('assert_sequence_equal', [1, 2], (2, 3))
        self.verify_assertion('assert_list_equal', [1, 2], [2, 3])
        self.verify_assertion('assert_tuple_equal', (1, 2), (2, 3))
        self.verify_assertion('assert_dict_equal', {'one': 1}, {'one': 2})
        self.verify_assertion('assert_count_equal', [1, 3], (1, 2))
        self.verify_assertion('assert_multi_line_equal', '1\n2', '1\n2\n')
        self.verify_assertion('assert_set_equal', {1, 2}, {1, 2, 3})

    def test_context_manager_assertions(self):
        test = MixinTestCase()
        with test.assert_raises(TypeError):
            1 / '2'
        with test.assert_raises_regex(TypeError, r'unsupported operand'):
            1 / '2'
        with test.assert_warns(UserWarning):
            warnings.warn('foo')
        with test.assert_warns_regex(UserWarning, 'foo'):
            warnings.warn('foo')
        with test.assert_logs('some.logger'):
            logging.getLogger('some.logger').info('hi there')
