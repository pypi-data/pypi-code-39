import logging
import os
import sys

import pandas as pd
import cancergenomeinterpreter.utils.constants as ct
import cancergenomeinterpreter.utils.lib as lib
from itab.files import open_file


def is_fus_file(input_file):
    with open_file(input_file) as fd:
        header = fd.readline().lower()
        return ct.FUS in header


def reformat_input(config):
    def order_partners(e):

        try:
            p1, p2 = e.split(ct.FUS_SEP)
            if p1 > p2:
                p1, p2 = p2, p1
            return p1 + ct.FUS_SEP + p2
        except Exception:
            return 'n/a'

    df = pd.read_csv(config['input_fp'], sep='\t')

    # pass to lower case
    df.columns = [c.lower() for c in df.columns]

    for c in [ct.FUS]:
        if c not in df.columns:
            logging.error('The column {0} is not found in the fusion drivers file {1}'.format(c, config['input_fp']))
            sys.exit(-1)

    df[ct.FUS] = df.apply(lambda row: order_partners(row[ct.FUS]), axis=1)

    # output
    df.to_csv(config['fus_fp'], sep='\t', index=False)
    logging.debug('File created in temp folder: {0}'.format(config['fus_fp']))

    return df


def run(config: dict):
    logging.info('Processing the Fusions input file')

    # fusion has a single format so far, so there is no format detection step
    config['input_format'] = ct.FUS_FORMAT

    # retrieve the paths of the outputs of the module
    config['input_fp'] = os.path.join(config['output_folder'], ct.INPUT_FUS)
    config['fus_fp'] = os.path.join(config['tmp_folder'], ct.REFORMATED_FUS)

    # if the output file already exists, do not need to run the module if 'force_output' == False
    if not config['force_output'] and os.path.isfile(config['fus_fp']):
        logging.debug('Stage skipped: file {0} already exists'.format(config['fus_fp']))
        return config

    # first, it copies the input file as it is
    lib.copy_input_file(config, ct.INTERNAL_ID)

    # then reformat the input
    config = reformat_input(config)

    return config
