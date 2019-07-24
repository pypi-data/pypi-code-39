from importlib import import_module

from django.test import TestCase

from waelstow import capture_stdout

from yaset import import_settings

# ============================================================================

class YasetTests(TestCase):
    def test_working(self):
        # tests a load with a properly configure local_settings directory

        mod = import_module('yaset.tests.fixtures.working')
        import_settings(mod.__dict__)
        self.assertEqual(mod.DEV_ONE, 1)
        self.assertEqual(mod.NESTED_ONE, 1)

    def test_bad_redirect(self):
        # tests a load with an invalid import_redirect entry

        mod = import_module('yaset.tests.fixtures.bad_redirect')
        with capture_stdout() as capture:
            import_settings(mod.__dict__)

        result = capture.getvalue().split('\n')
        self.assertIn('yaset could not load', result[0])
        self.assertIn('yaset could not load', result[1])

    def test_no_redirect(self):
        # tests a load with a missing import_redirect 

        mod = import_module('yaset.tests.fixtures.no_redirect')
        with capture_stdout() as capture:
            import_settings(mod.__dict__)

        self.assertIn('Error', capture.getvalue())

    def test_no_secret(self):
        # tests a load with a missing secrets file

        mod = import_module('yaset.tests.fixtures.no_secret')
        with capture_stdout() as capture:
            import_settings(mod.__dict__)

        # import should still work
        self.assertEqual(mod.DEV_ONE, 1)
        self.assertEqual(mod.NESTED_ONE, 1)

        # stdout should include warning about the secret missing
        result = capture.getvalue()
        self.assertIn('yaset could not load', result)
        self.assertIn('secret', result)
