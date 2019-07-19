import configparser


# ------------------------------------------------------------------------------
def parse_config(config_file, section):
    """
    Parses a configuration file into a dictionary.

    :param config_file: a configuration file in [configparser]
    (https://docs.python.org/3/library/configparser.html) compatible format
    :param section: configuration file section to parse
    :return: dictionary of key/value pairs parsed from the configuration file
    """

    # create a parser
    config_parser = configparser.ConfigParser()

    # read the configuration file into a dictionary of parameters
    config_params = {}
    config_parser.read(config_file)
    if config_parser.has_section(section):
        params = config_parser.items(section)
        for param in params:
            config_params[param[0]] = param[1]
    else:
        raise Exception(f"Section '{section}' not found in " +
                        f"the configuration file: {config_file}")

    return config_params


# ------------------------------------------------------------------------------
def config_has_section(config_file: str, section: str):

    # create a configuration parser, read the file,
    # and check for presence of the section
    config_parser = configparser.ConfigParser()
    config_parser.read(config_file)
    return section in config_parser.sections()
