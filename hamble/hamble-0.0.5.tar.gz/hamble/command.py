'''
    This is a command line tool developed to parse .ini files for parameters 
    to populate into config files used for applications.
'''
import click
from hamble import hamble


@click.command()
@click.version_option(version='0.0.5')
@click.option('--ini', '-i', help='INI file with needed information', required=True)
@click.option('--config', '-c', help='config file needed to populate values from ini file into', required=True)
def cli(ini, config):
    '''This script greets you.'''
    click.echo('The ini file %s was read in.' % ini)
    click.echo('The config file %s was read in.' % config)
    rendered_template = hamble.render_shit(config, ini)
    hamble.write_template(config, rendered_template)
