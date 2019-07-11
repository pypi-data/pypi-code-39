import logging
import os

import pandas as pd
import cancergenomeinterpreter.utils.constants as ct
from cancergenomeinterpreter.utils.tumor import Tumor


def match_drivers(config):
    def get_offspring_tumors(tumor_type):
        Tumor.load_family(config['cancer_types'])
        tumor_family = [tumor_type] + Tumor(tumor_type).get_offspring()
        logging.debug('The driver genes are looked for cancers: {0}'.format(','.join(tumor_family)))

        return list(set(tumor_family))

    def tumor_match(driver_tumors, sample_tumors):
        if type(driver_tumors) != str:
            return ''

        driver_tumors = driver_tumors.split(';') if ';' in driver_tumors else [driver_tumors]
        common = list(set(driver_tumors) & set(sample_tumors))
        match = ct.KNOWN_MATCH if len(common) > 0 else ''

        return match

    # read the cancer-fus drivers db (remember that this entry is contained in the cgi.conf in the .bbglab folder)
    known_df = pd.read_csv(config['fus_drivers_fp'], sep='\t')
    known_df = known_df.rename(columns={known_df.columns[0]: ct.FUS, known_df.columns[1]: ct.FUS_EFFECTOR,
                                        known_df.columns[2]: ct.KNOWN_IN_TUMORS})

    # read the input and merge
    fus_df = pd.read_csv(config['fus_fp'], sep='\t')
    out_df = fus_df.merge(known_df[[ct.FUS, ct.FUS_EFFECTOR, ct.KNOWN_IN_TUMORS]], how='left', on=ct.FUS)

    # retrieve tumors offspring
    tumors = get_offspring_tumors(config['tumor_type'])
    config['tumor_offspring'] = tumors
    logging.debug('The tumors of interest are {0}'.format(','.join(tumors)))

    # do the merge only for genes with tumor match
    out_df[ct.KNOWN_MATCH] = out_df.apply(lambda row: tumor_match(row[ct.KNOWN_IN_TUMORS], tumors), axis=1)

    # output
    out_df.to_csv(config['drivers_fus'], index=False, sep='\t')
    logging.debug('File created {0}'.format(config['drivers_fus']))

    return config


def run(config: dict):
    logging.info('Matching with the FUS drivers database')

    # retrieve the output file of the module
    config['drivers_fus'] = os.path.join(config['tmp_folder'], ct.DRIVER_FUS)

    # if the output file already exists, do not need to run the module if 'force_output' == False
    if not config['force_output'] and os.path.isfile(config['drivers_fus']):
        logging.debug('Stage skipped: file {0} already exists'.format(config['drivers_fus']))
        return config

    # Match the CNA input with the CNA drivers database
    config = match_drivers(config)

    return config
