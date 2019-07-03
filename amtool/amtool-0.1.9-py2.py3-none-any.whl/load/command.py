import click
import yaml
from amt import load
from amt import MetaDict
from amt import MetaList


@click.command()
@click.argument('PATH')
def dump(path):
    """
    Read the contents of the artifact tree.
    """
    yaml.add_representer(MetaDict,
                         lambda dumper, data: dumper.represent_mapping(
                             'tag:yaml.org,2002:map', data.items()))
    yaml.add_representer(MetaList,
                         lambda dumper, data: dumper.represent_sequence(
                             'tag:yaml.org,2002:seq', data))
    click.echo(yaml.dump(load(path), default_flow_style=False))
    return 0
