# Copyright 2018-2019 Cyril Roelandt
#
# Licensed under the 3-clause BSD license. See the LICENSE file.
import datetime
import unittest
from unittest import mock

import upt

from upt_fedora.upt_fedora import FedoraPackage


class TestFedoraPackage(unittest.TestCase):
    def setUp(self):
        self.upt_pkg = upt.Package('foo', '42', summary='summary',
                                   homepage='homepage')
        FedoraPackage.folder_name = 'frontend-foo'
        self.fedora_pkg = FedoraPackage(self.upt_pkg, None)

    def test_attributes(self):
        self.assertEqual(self.upt_pkg.version, self.fedora_pkg.version)
        self.assertEqual(self.upt_pkg.summary, self.fedora_pkg.summary)
        self.assertEqual(self.upt_pkg.homepage, self.fedora_pkg.homepage)

    def test_licenses(self):
        # No licenses
        self.upt_pkg.licenses = []
        self.assertEqual(self.fedora_pkg.licenses, '')

        # A single good license
        self.upt_pkg.licenses = [upt.licenses.ApacheLicenseTwoDotZero()]
        self.assertEqual(self.fedora_pkg.licenses, 'ASL 2.0')

        # A single bad license
        self.upt_pkg.licenses = [upt.licenses.AdaptivePublicLicense()]
        self.assertEqual(self.fedora_pkg.licenses, 'BAD LICENSE (APL-1.0)')

        # A mix of good and bad licenses
        self.upt_pkg.licenses = [
            upt.licenses.ApacheLicenseTwoDotZero(),
            upt.licenses.AdaptivePublicLicense()
        ]
        self.assertEqual(self.fedora_pkg.licenses,
                         'BAD LICENSE (Apache-2.0 APL-1.0)')

    def test_today(self):
        # We cannot mock datetime.datetime.today, because built-in types are
        # immutable. We subclass datetime.datetime and redefine "today"
        # instead.
        class MockDatetime(datetime.datetime):
            def today():
                return datetime.datetime(1989, 5, 26)

        datetime.datetime = MockDatetime
        self.assertEqual(self.fedora_pkg.today(), 'Fri May 26 1989')

    def test_depends(self):
        self.assertListEqual(self.fedora_pkg.build_depends, [])
        self.assertListEqual(self.fedora_pkg.run_depends, [])
        self.assertListEqual(self.fedora_pkg.test_depends, [])

        requirements = {
            'build': [upt.PackageRequirement('foo')],
            'run': [upt.PackageRequirement('bar')],
            'test': [upt.PackageRequirement('baz')],
        }
        self.upt_pkg.requirements = requirements
        self.assertListEqual(self.fedora_pkg.build_depends,
                             requirements['build'])
        self.assertListEqual(self.fedora_pkg.run_depends,
                             requirements['run'])
        self.assertListEqual(self.fedora_pkg.test_depends,
                             requirements['test'])


class TestOutputDirectory(unittest.TestCase):
    def setUp(self):
        self.upt_pkg = upt.Package('foo', 42)
        FedoraPackage.folder_name = 'frontend-foo'

    @mock.patch('os.makedirs', side_effect=PermissionError)
    def test_create_output_directory_permission_denied(self, mkdir):
        self.fedora_pkg = FedoraPackage(self.upt_pkg, None)
        with self.assertRaises(SystemExit):
            self.fedora_pkg._create_output_directory()

    @mock.patch('os.getcwd', return_value='/cwd')
    def test_output_directory_no_output(self, getcwd):
        self.fedora_pkg = FedoraPackage(self.upt_pkg, None)
        self.assertEqual(self.fedora_pkg.output_dir, '/cwd/frontend-foo')

    def test_output_directory_output(self):
        self.fedora_pkg = FedoraPackage(self.upt_pkg, '/path/')
        self.assertEqual(self.fedora_pkg.output_dir, '/path/frontend-foo')


class TestFileCreation(unittest.TestCase):
    def setUp(self):
        self.upt_pkg = upt.Package('foo', 42)
        FedoraPackage.folder_name = 'frontend-foo'
        FedoraPackage.archive_type = 'archive_type'
        self.fedora_pkg = FedoraPackage(self.upt_pkg, None)

    @mock.patch('builtins.open', side_effect=FileExistsError)
    def test_create_specfile_already_exists(self, m_open):
        with self.assertRaises(SystemExit):
            self.fedora_pkg._create_specfile()

    @mock.patch('builtins.open', side_effect=PermissionError)
    def test_create_specfile_permission_denied(self, m_open):
        with self.assertRaises(SystemExit):
            self.fedora_pkg._create_specfile()

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    @mock.patch.object(FedoraPackage, '_render_specfile_template',
                       return_value='Specfile content')
    def test_create_specfile(self, m_specfile, m_open):
        self.fedora_pkg._create_specfile()
        m_open.assert_called()
        m_open().write.assert_called_once_with('Specfile content')

    @mock.patch('builtins.open')
    def test_create_sources_no_archive(self, m_open):
        self.upt_pkg.get_archive = mock.Mock(
            side_effect=upt.ArchiveUnavailable)
        self.fedora_pkg._create_sources()
        m_open.assert_not_called()

    @mock.patch('builtins.open', side_effect=PermissionError)
    def test_create_sources_permission_denied(self, m_open):
        self.upt_pkg.get_archive = mock.Mock()
        with self.assertRaises(SystemExit):
            self.fedora_pkg._create_sources()

    @mock.patch('builtins.open', side_effect=FileExistsError)
    def test_create_sources_already_exists(self, m_open):
        self.upt_pkg.get_archive = mock.Mock()
        with self.assertRaises(SystemExit):
            self.fedora_pkg._create_sources()

    @mock.patch('builtins.open', new_callable=mock.mock_open)
    def test_create_sources(self, m_open):
        fake_archive = upt.Archive('http://example.com/foo.tar.gz',
                                   sha512='sha512')
        self.upt_pkg.get_archive = mock.Mock(return_value=fake_archive)
        self.fedora_pkg._create_sources()
        content = 'SHA512 (foo.tar.gz) = sha512'
        m_open().write.assert_called_once_with(content)


if __name__ == '__main__':
    unittest.main()
