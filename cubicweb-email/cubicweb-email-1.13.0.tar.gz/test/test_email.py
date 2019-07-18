"""automatic tests for email views"""

from cubicweb.devtools.testlib import AutomaticWebTest

from cubicweb_email.testutils import EmailValueGenerator  # noqa


class AutomaticWebTest(AutomaticWebTest):

    def to_test_etypes(self):
        return set(('Email', 'EmailPart', 'EmailThread'))

    def list_startup_views(self):
        return ()


if __name__ == '__main__':
    import unittest
    unittest.main()
