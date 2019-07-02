import click
import yaml
from amt import MetaDict
from amt import MetaList
from amt import uid as amtuid


@click.command()
@click.argument('PATH')
def uid(path):
    yaml.add_representer(MetaDict,
                         lambda dumper, data: dumper.represent_mapping(
                             'tag:yaml.org,2002:map', data.items()))
    yaml.add_representer(MetaList,
                         lambda dumper, data: dumper.represent_sequence(
                             'tag:yaml.org,2002:seq', data))
    click.echo(yaml.dump(amtuid(path), default_flow_style=False))
    return 0
