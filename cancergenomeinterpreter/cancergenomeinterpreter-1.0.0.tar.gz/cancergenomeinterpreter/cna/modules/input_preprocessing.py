import logging
import os
import sys

import numpy as np
import pandas as pd
import cancergenomeinterpreter.utils.constants as ct
import cancergenomeinterpreter.utils.lib as lib
from itab.files import open_file


def detect_malformed_cna(df, config):
    df['alteration_malformed'] = np.where(df[ct.CNA].isin(ct.CNA_ALTERATIONS), 'ok', 'malformed')

    malformed_df = df[df['alteration_malformed'] == 'malformed']
    df = df[df['alteration_malformed'] != 'malformed']

    df = df.drop('alteration_malformed', 1)
    malformed_df = malformed_df.drop('alteration_malformed', 1)

    if len(malformed_df) > 0:
        logging.warning('There are {0} entries not considered since cna is not stated as {1}'
                        .format(len(malformed_df), ' or '.join(ct.CNA_ALTERATIONS)))
        malformed_df.to_csv(config['malformed_fp'], index=False, sep='\t')
        logging.debug('File created {0}'.format(config['malformed_fp']))

    return df


def free2cna(config):
    df = pd.read_csv(config['input_fp'], sep='\t')

    for c in [ct.GENE, ct.CNA]:
        if c not in df.columns:
            logging.error('The column {0} is not found in the cna drivers file {1}'.format(c, config['cna_drivers_fp']))
            sys.exit(-1)

    # Change CNA to uppercase
    df[ct.CNA] = df[ct.CNA].str.upper()

    if ct.SAMPLE not in df.columns:
        logging.debug('Default sample id inserted')
        df[ct.SAMPLE] = ct.DEFAULT_SAMPLE

    # check that the CNA entries follow the required syntax
    df = detect_malformed_cna(df, config)

    # if ok, i put it in the tmp folder
    df.to_csv(config['cna_fp'], sep='\t', index=False)
    logging.debug('File created in temp folder: {0}'.format(config['cna_fp']))

    return config


def mat2cna(config):
    df = pd.read_csv(config['input_fp'], sep='\t')
    logging.debug('The AMP/DEL values to be parsed are {0}/{1}'.format(config['amp_value'], config['del_value']))

    # convert a matrix to a tdm with only the significant AMP/DEL
    out_df = pd.DataFrame()
    for s in df.columns[3:]:
        tmp_df = pd.DataFrame({ct.GENE: df[df.columns[0]], ct.SAMPLE: [s] * len(df), ct.CNA: df[s].astype(float)},
                              index=range(len(df)))
        tmp_df = tmp_df[tmp_df[ct.CNA].isin([config['amp_value'], config['del_value']])]
        out_df = out_df.append(tmp_df, ignore_index=True)

    # recode to 'AMP', 'DEL'
    out_df[ct.CNA] = np.where(out_df[ct.CNA] == config['amp_value'], 'AMP', 'DEL')

    # output
    out_df.to_csv(config['cna_fp'], sep='\t', columns=[ct.SAMPLE, ct.GENE, ct.CNA], index=False)
    logging.debug('File created in temp folder: {0}'.format(config['cna_fp']))

    return config


def which_cna_file(input_file):
    with open_file(input_file) as fd:
        header = fd.readline().lower()

        if ct.LOCUS.lower() in header and ct.CYTOBAND.lower() in header:
            return ct.CNA_MAT_FORMAT

        if ct.CNA.lower() in header and ct.GENE.lower() in header:
            return ct.CNA_FREE_FORMAT

        return None


def detect_original_format(original_fp):
    """
    The detection of the format of the original input file; based on the extension of the file

    :param original_fp: Input file path
    :return: The format type
    """

    # is_cna_file return the format of the cna file if it is one, None otherwise
    cna_format = which_cna_file(original_fp)

    if cna_format is None:
        logging.error('Format of the input file not recognized {0}'.format(original_fp))
        sys.exit(-1)

    return cna_format


def reformat_input(config):
    """
    Takes the input copied in the output root and reformat it depending on the input format
    """

    if config['input_format'] == ct.CNA_FREE_FORMAT:
        free2cna(config)
    elif config['input_format'] == ct.CNA_MAT_FORMAT:
        mat2cna(config)
    else:
        logging.error('The format {0} has not format function implemented'.format(config['input_format']))
        sys.exit(-1)

    return config


def run(config: dict):
    logging.info('Processing the Copy Number Alterations input file')

    # detect original format here, since i need to use it for the rest of the pipeline
    original_format = detect_original_format(config['source_fp'])

    config['input_format'] = original_format
    logging.info('The detected format is {0}'.format(original_format))

    # retrieve the paths of the outputs of the module
    config['input_fp'] = os.path.join(config['output_folder'], ct.INPUT_CNAS)
    config['malformed_fp'] = os.path.join(config['output_folder'], ct.MALFORMED_CNAS)
    config['cna_fp'] = os.path.join(config['tmp_folder'], ct.REFORMATED_CNAS)

    # if the output file already exists, do not need to run the module if 'force_output' == False
    if not config['force_output'] and os.path.isfile(config['cna_fp']):
        logging.debug('Stage skipped: file {0} already exists'.format(config['cna_fp']))
        return config

    # first, it copies the input file as it is
    lib.copy_input_file(config, ct.INTERNAL_ID)

    # then reformat the input
    config = reformat_input(config)

    return config
