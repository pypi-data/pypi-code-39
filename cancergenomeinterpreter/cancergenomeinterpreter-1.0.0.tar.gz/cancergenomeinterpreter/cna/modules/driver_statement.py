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

    # read the pre-compiled cna drivers file (remember the path is in cgi.conf file in .bbglab folder)
    drivers_df = pd.read_csv(config['cna_drivers_fp'], sep='\t')
    drivers_df = drivers_df.rename(columns={drivers_df.columns[0]: ct.GENE, drivers_df.columns[1]: ct.CNA})

    # first ensure that the alteration label is in capital letter
    drivers_df[ct.CNA] = [e.upper() for e in drivers_df[ct.CNA]]

    # and pivot the info
    known_df = drivers_df[drivers_df[drivers_df.columns[-1]] == 'known'][[ct.GENE, ct.CNA, 'cancer_acronym']].groupby(
        [ct.GENE, ct.CNA]) \
        .aggregate(lambda values: ';'.join(values)).reset_index().rename(columns={'cancer_acronym': ct.KNOWN_IN_TUMORS})
    predicted_df = drivers_df[drivers_df[drivers_df.columns[-1]] == 'predicted'][
        [ct.GENE, ct.CNA, 'cancer_acronym']].groupby([ct.GENE, ct.CNA]) \
        .aggregate(lambda values: ';'.join(values)).reset_index().rename(
        columns={'cancer_acronym': ct.PREDICTED_IN_TUMORS})

    # read the sample cnas
    cna_df = pd.read_csv(config['cna_fp'], sep='\t')
    # first ensure that the alteration label is in capital letter
    cna_df[ct.CNA] = [e.upper() for e in cna_df[ct.CNA]]
    # and do the match with the precomplied known and predicted drivers
    out_df = cna_df.merge(known_df, how='left', on=[ct.GENE, ct.CNA]).merge(predicted_df, how='left',
                                                                            on=[ct.GENE, ct.CNA])

    # retrieve tumors offspring
    tumors = get_offspring_tumors(config['tumor_type'])
    config['tumor_offspring'] = tumors
    logging.debug('The tumors of interest are {0}'.format(','.join(tumors)))

    # do the merge only for genes with tumor match
    out_df[ct.KNOWN_MATCH] = out_df.apply(lambda row: tumor_match(row[ct.KNOWN_IN_TUMORS], tumors), axis=1)
    out_df[ct.PREDICTED_MATCH] = out_df.apply(lambda row: tumor_match(row[ct.PREDICTED_IN_TUMORS], tumors), axis=1)

    # output
    out_df.to_csv(config['drivers_cnas'], sep='\t', index=False)
    logging.debug('File created {0}'.format(config['drivers_cnas']))

    return config


def run(config: dict):
    logging.info('Matching with the CNA drivers database')

    # retrieve the output file
    config['drivers_cnas'] = os.path.join(config['tmp_folder'], ct.DRIVERS_CNAS)

    # if the output file already exists, do not need to run the module if 'force_output' == False
    if not config['force_output'] and os.path.isfile(config['drivers_cnas']):
        logging.debug('Stage skipped: file {0} already exists'.format(config['drivers_cnas']))
        return config

    # Match the CNA input with the CNA drivers database
    config = match_drivers(config)

    return config
