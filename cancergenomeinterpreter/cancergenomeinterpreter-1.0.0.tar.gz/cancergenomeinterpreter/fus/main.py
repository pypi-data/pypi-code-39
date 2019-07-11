import argparse
import logging
import os

import cancergenomeinterpreter.fus.modules.driver_statement as driver_statement
import cancergenomeinterpreter.fus.modules.input_preprocessing as input_preprocessing
import cancergenomeinterpreter.fus.modules.output_format as output_format
import cancergenomeinterpreter.utils.constants as ct
import cancergenomeinterpreter.utils.lib as lib


def run(input_file, tumor_type, output_folder, force_output=False):
    # Load config file
    config = lib.load_configuration()

    # Initialize configuration
    config['source_fp'] = os.path.abspath(input_file)
    config['output_folder'] = lib.create_folder(output_folder)
    config['tumor_type'] = tumor_type
    config['tmp_folder'] = lib.create_folder(os.path.join(config['output_folder'], 'tmp'))
    config['force_output'] = force_output

    # Read and format input file
    input_preprocessing.run(config)

    # Match with pre compiled known/predicted CNA drivers
    driver_statement.run(config)

    # Format the output
    output_format.run(config)

    return config


def cmdline():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument('-i', '--input', dest='input_file', required=True, help='Variants file')

    # Optional arguments
    parser.add_argument('-o', '--output', dest='output_folder', default="output",
                        help="Output folder. Default to regions file name without extensions.")
    parser.add_argument('-t', '--tumor', dest='tumor_type', default=ct.PANCANCER,
                        help="Specify the tumor type of the sample(s) under analysis")
    parser.add_argument('--force', dest='force_output', default=False, action='store_true',
                        help="Run the commands and overwrite results although output files already exist")
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help="Show more progress details")

    # Parse arguments
    args = parser.parse_args()

    # Configure the logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S')
    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.debug(args)

    run(args.input_file, args.tumor_type, args.output_folder, force_output=args.force_output)


if __name__ == "__main__":
    cmdline()
