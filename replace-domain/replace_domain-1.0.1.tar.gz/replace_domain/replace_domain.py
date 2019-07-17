from looptools import Timer
from argparse import ArgumentParser
import os


@Timer.decorator
def replace_domain(domain, conf_file, placeholder="$DOMAIN_NAME"):
    """
    Parse a nginx.conf template that contains $DOMAIN_NAME placeholders.

    Replace all occurrences of $DOMAIN_NAME with the correct domain name.

    :param domain: Domain url
    :param conf_file: File path of config file
    :param placeholder: String to replace within the config file
    :return:
    """
    # Read in the file
    with open(os.path.abspath(conf_file), 'r') as cf:
        data = cf.read()

    # Replace the target string
    new_data = data.replace(placeholder, domain)

    # Write the file out again
    with open(conf_file, 'w') as cf:
        cf.write(new_data)


def main():
    # Declare argparse argument descriptions
    usage = 'Nginx config string replacement utility.'
    description = 'Replace $DOMAIN_NAME place holder with real domain name value.'
    helpers = {
        'domain': 'Domain name to replace the placeholder',
        'conf-file': 'Path to your .conf template file.',
        'placeholder': 'String to replace to replace with domain value.'
    }

    # construct the argument parse and parse the arguments
    ap = ArgumentParser(usage=usage, description=description)
    ap.add_argument('--domain', help=helpers['domain'], type=str)
    ap.add_argument('--conf-file', help=helpers['conf-file'], type=str)
    ap.add_argument('--placeholder', help=helpers['placeholder'], type=str)
    args = vars(ap.parse_args())

    replace_domain(args['domain'], args['conf_file'])


if __name__ == '__main__':
    main()
