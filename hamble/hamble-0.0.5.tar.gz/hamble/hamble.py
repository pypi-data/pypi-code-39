'''
    This is the main application code for hamble pip package.
    Reads values from an ini file and parses a config file to populate
    the config file with the correlating values from the ini file.
'''
import boto3
import sys
import logging
import traceback
from configparser import ConfigParser
from jinja2 import FileSystemLoader, Environment


def read_ini_info(ini_file):
    """
    Read the INI file

    Args:
        ini_file - path to the file

    Returns:
        A dictionary of stuff from the INI file

    Exits:
        1 - if problems are encountered
    """
    try:
        config = ConfigParser()
        config.optionxform = lambda option: option
        config.read(ini_file)
        the_stuff = {}
        for section in config.sections():
            the_stuff[section] = {}
            for option in config.options(section):
                the_stuff[section][option] = config.get(section, option)

        return the_stuff

    except Exception as wtf:
        logging.error('Exception caught in read_config_info(): {}'.format(wtf))
        traceback.print_exc(file=sys.stdout)

        return sys.exit(1)


def read_config_file(config):
    '''
    Read the config file:

    Args:
        config - processed from click command line entry

    Returns:
        A list of the config file containing jinja delimiters

    Exits:
        1 - if problems are encountered
    '''
    try:
        config = open(config, 'r')
        f1 = config.readlines()

        return f1

    except Exception as wtf:
        logging.error('Exception caught in read_config_file(): {}'.format(wtf))
        traceback.print_exc(file=sys.stdout)

        return sys.exit(1)


def get_ssm_parameter(param):
    '''
    Goes out to AWS Systems Manager's parameter store and grabs a value

    Args:
        param - parameter name passed here
    Return:
        parameter from parameter store
    '''
    try:
        client = boto3.client('ssm')
        response = client.get_parameter(Name=param, WithDecryption=True)
        return response['Parameter']['Value']
    except Exception as wtf:
        logging.error(wtf, exc_info=False)

    return None


def render_shit(config, ini):
    '''
    Renders the configuration template in question

    Args:
        config - processed from click command line entry
        ini - processed from click command line entry

    Returns:
        Rendered template with values from the ini file
    '''
    dict = read_ini_info(ini)
    template_file = dict.get('parameters', {})
    file_loader = FileSystemLoader('./')
    env = Environment(loader=file_loader)
    template = env.get_template(config)
    for value in template_file.keys():
        if template_file[value].startswith('[ssm:') and template_file[value].endswith(']'):
            parts = (template_file[value]).split(':')
            ssm_key = parts[1].replace(']', '')
            val = get_ssm_parameter(ssm_key)
            if val:
                template_file[value] = val
            else:
                logging.error('SSM parameter {} not found'.format(ssm_key))

    return template.render(template_file)


def write_template(config, rendered_template):
    '''
    Writes newly populated config file over original.

    Args:
        config: config file being processed from click command.py
        rendered_template: rendered config file with populated values from render_shit

    Exits: 1 - if a problem is encounted.
    '''
    with open(config, "w") as f:
        f.write(rendered_template)
        f.close()
