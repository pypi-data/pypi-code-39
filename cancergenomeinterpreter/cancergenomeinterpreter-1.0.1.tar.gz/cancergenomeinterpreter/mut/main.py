import argparse
import logging
import os
import sys

import cancergenomeinterpreter.mut.modules.call_fiscore as call_fiscore
import cancergenomeinterpreter.mut.modules.dna_mutation_annotation as dna_mutation_annotation
import cancergenomeinterpreter.mut.modules.driver_prediction as driver_prediction
import cancergenomeinterpreter.mut.modules.input_preprocessing as input_format
import cancergenomeinterpreter.mut.modules.lib as lib
import cancergenomeinterpreter.mut.modules.match_metadata as match_metadata
import cancergenomeinterpreter.mut.modules.output_format as output_format
import cancergenomeinterpreter.mut.utils.constants as ct
from cancergenomeinterpreter.utils.lib import load_configuration
from cancergenomeinterpreter.mut.utils.faidx import init_refgenome

# FIXME Fix the warnings instead of ignoring them
import pandas as pd
pd.options.mode.chained_assignment = None


def run(config: dict):
    # 1. Processing the mutations input file
    config = input_format.run(config)

    # 2. Annotating the nucleotide mutations to protein coordinates per transcript
    config = dna_mutation_annotation.run(config)

    # 3. Retrieving Functional Impact scores
    config = call_fiscore.run(config)

    # 4. Matching with several metadata files
    config = match_metadata.run(config)

    # 5. Running the driver prediction
    config = driver_prediction.run(config)

    # 6. Arranging the output
    output_format.run(config)


def cmdline():
    parser = argparse.ArgumentParser()

    # Required arguments
    parser.add_argument('-i', '--input', dest='input_file', required=True, help='Variants file')

    # Optional arguments
    parser.add_argument('-o', '--output', dest='output_folder', default="output",
                        help="Output folder. Default to regions file name without extensions.")
    parser.add_argument('-t', '--tumor', dest='tumor_type', default=ct.PANCANCER,
                        help="Specify the tumor type of the sample(s) under analysis")
    parser.add_argument('-s', '--sample', dest='sample', default=ct.INTERNAL_ID,
                        help="Default identifier of the sample")
    parser.add_argument('--force', dest='force_output', default=False, action='store_true',
                        help="Run the commands and overwrite results although output files already exist")
    parser.add_argument('--debug', dest='debug', default=False, action='store_true', help="Show more progress details")
    parser.add_argument('--extended', dest='extended', default=False, action='store_true',
                        help="Computational expensive metrics are also calculated for non coding mutations")

    # Parse arguments
    args = parser.parse_args()
    output_folder = lib.create_folder(args.output_folder)

    # Configure the logging
    handler_stdout = logging.StreamHandler(stream=sys.stdout)
    handler_file = logging.FileHandler(os.path.join(output_folder, 'oncodriveMUT.log'))
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', datefmt='%H:%M:%S',
                        handlers=[handler_stdout, handler_file])
    logging.getLogger().setLevel(logging.DEBUG if args.debug else logging.INFO)
    logging.debug(args)

    # from the utils/config.py it uses the config file (that can be passed as an argument,
    # or in .bbglab as default otherwise) to retrieve the file paths of the file of interest
    # (known oncogenic mutations etc)
    config = load_configuration()

    # Initialize configuration
    config['source_fp'] = os.path.abspath(args.input_file)
    config['output_folder'] = output_folder
    config['tumor_type'] = args.tumor_type
    config['tmp_folder'] = lib.create_folder(os.path.join(config['output_folder'], 'tmp'))
    config['force_output'] = args.force_output
    config['extended'] = args.extended
    config['sample'] = args.sample
    # the following one is only used if the input is protein format; to move it elsewhere
    config['recoverable_fs'] = 0
    init_refgenome(config['genomeref'])

    run(config)


if __name__ == "__main__":
    cmdline()
