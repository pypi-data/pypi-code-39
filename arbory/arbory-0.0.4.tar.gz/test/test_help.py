"""Test help for all functions.
"""

from click.testing import CliRunner
import pytest

from arbory import arb


@pytest.mark.parametrize('cmd, noop_help', [
    # arbory base command.
    ([], True),
    # tree subcommand.
    (['tree'], False),
    # config subcommand.
    (['config'], False),
])
def test_help(cmd, noop_help):
    """Make sure help is available in both long and short forms."""
    runner = CliRunner()
    cmd.append('--help')
    result = runner.invoke(arb, cmd)
    assert result.exit_code == 0 and 'Usage: ' in result.output
    cmd[-1] = '-h'
    result = runner.invoke(arb, cmd)
    assert result.exit_code == 0 and 'Usage: ' in result.output
    if noop_help:
        del cmd[-1]
        result = runner.invoke(arb, cmd)
        assert result.exit_code == 0 and 'Usage: ' in result.output
