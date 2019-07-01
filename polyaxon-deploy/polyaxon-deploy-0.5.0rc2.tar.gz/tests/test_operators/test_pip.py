# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from unittest import TestCase

import mock

from polyaxon_deploy.operators.exceptions import OperatorException
from polyaxon_deploy.operators.pip import PipOperator

DUMMY_RETURN_VALUE = object()


class TestPipOperator(TestCase):

    def setUp(self):
        self.pip = PipOperator()

    @staticmethod
    def mock_popen(return_code, out_msg, err_msg=None):
        def popen(*args, **kwargs):
            stdout = kwargs.pop('stdout')
            stdout.write(out_msg)
            if err_msg:
                stderr = kwargs.pop('stderr')
                stderr.write(err_msg)
            return mock.Mock(wait=mock.Mock(return_value=return_code))

        return mock.Mock(side_effect=popen)

    @mock.patch('polyaxon_deploy.operators.cmd_operator.subprocess')
    def test_pip(self, mock_subprocess):
        mock_subprocess.Popen = self.mock_popen(0, 'bar')
        assert self.pip.execute(['install']) == 'bar'
        assert mock_subprocess.Popen.call_args[0][0] == ['pip', 'install']

    @mock.patch('polyaxon_deploy.operators.cmd_operator.subprocess')
    def test_pip_error(self, mock_subprocess):
        return_code = 1
        stdout = "output"
        stderr = "error"
        mock_subprocess.Popen = self.mock_popen(return_code, stdout, stderr)
        with self.assertRaises(OperatorException) as exception:
            self.pip.execute(['run'])

        self.assertEqual(
            exception.exception.message,
            "`pip` command ('pip', 'run') "
            "failed with exit status {}\nstdout:\n{}\nstderr:\n{}".format(
                return_code,
                stdout,
                stderr)
        )
