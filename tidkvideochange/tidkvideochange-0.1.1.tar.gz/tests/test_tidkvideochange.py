#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `tidkvideochange` package."""


import unittest
from click.testing import CliRunner

from tidkvideochange import tidkvideochange
from tidkvideochange import cli


class TestTidkvideochange(unittest.TestCase):
    """Tests for `tidkvideochange` package."""

    def test_import(self):
        """Test something."""
        try:
            from tidkvideochange.VideoChange import VideoChangeVideoText
        except:
            assert False

    def test_prepare_detection(self):
        try:
            from tidkvideochange import detection_batch as detection
            detection.prepare_model()
        except:
            assert False

    def test_prepare_recognition(self):
        try:
            from tidkvideochange import recognition_batch as recognition
            recognition.prepare_model()
        except:
            assert False

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'tidkvideochange.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output


if __name__ == '__main__':
    unittest.main()