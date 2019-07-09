from click.testing import CliRunner

from auger.cli.cli import cli


class TestCliTableOfContents(object):

    def test_index(self):
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0
        assert 'project' in result.output
        assert 'dataset' in result.output
        assert 'experiment' in result.output
        assert 'model' in result.output
        assert 'new' in result.output
