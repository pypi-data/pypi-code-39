"""Test configuration use.
"""

from click.testing import CliRunner

from arbory import arb


def test_show_config():
    runner = CliRunner()
    result = runner.invoke(arb, ['config'])
    assert result.output == 'DEFAULT\n'
