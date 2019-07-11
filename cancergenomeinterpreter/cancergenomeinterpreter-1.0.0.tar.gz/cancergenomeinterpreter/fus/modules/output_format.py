import logging
import os

import numpy as np
import pandas as pd
import cancergenomeinterpreter.utils.constants as ct
import cancergenomeinterpreter.utils.lib as lib


def add_prescription_required_columns(fus_df, config):
    fus_df[ct.CANCER] = config['tumor_type']
    if ct.SAMPLE not in fus_df.columns:
        logging.debug('Default sample id inserted')
        fus_df[ct.SAMPLE] = ct.DEFAULT_SAMPLE

    # add gene role
    role_df = pd.read_csv(config['gene_role_fp'], sep='\t')
    role_df = role_df.rename(columns={role_df.columns[0]: ct.FUS_EFFECTOR, role_df.columns[-1]: ct.GENE_ROLE})
    fus_df = fus_df.merge(role_df[[ct.FUS_EFFECTOR, ct.GENE_ROLE]], how='left', on=ct.FUS_EFFECTOR)
    fus_df[ct.GENE_ROLE] = np.where(fus_df[ct.GENE_ROLE].isnull(), ct.AMBIGUOUS, fus_df[ct.GENE_ROLE])

    return fus_df


def insert_driver_status(fus_df):
    def get_oncogenic_classification(row):

        # remove 'CANCER' from the known if there are other cancer entries
        def remove_generic(entry):
            if ';' in entry and 'CANCER' in entry:
                entry = entry.replace('CANCER;', '').replace(';CANCER', '')
            return entry

        # print(row)
        if type(row[ct.KNOWN_IN_TUMORS]) == str:
            cat = ct.KNOWN
            statement = 'known in: ' + remove_generic(row[ct.KNOWN_IN_TUMORS])
        else:
            cat = ''
            statement = 'uncertain relevance'

        return pd.Series({ct.ONCOGENIC: cat, ct.ONCOGENIC_CLASSIFICATION: statement})

    fus_df = fus_df.merge(fus_df.apply(lambda row: get_oncogenic_classification(row), axis=1), left_index=True,
                          right_index=True)

    return fus_df


def order_output(fus_df):
    # order rows
    i1 = fus_df[fus_df[ct.ONCOGENIC] == ct.KNOWN].index.tolist()
    i2 = list(set(fus_df.index.tolist()) - set(i1))

    fus_df = fus_df.ix[i1 + i2]

    # order columns
    c1 = [ct.SAMPLE, ct.FUS, ct.FUS_EFFECTOR, ct.GENE_ROLE]
    c3 = [ct.ONCOGENIC, ct.ONCOGENIC_CLASSIFICATION, ct.KNOWN_MATCH]
    c2 = lib.difference_lists([fus_df.columns, c1 + c3])

    fus_df = fus_df[c1 + c2 + c3]

    return fus_df


def run(config: dict):
    logging.info('Formating the output')

    # retrieve the output file
    config['tcgi_fus'] = os.path.join(config['output_folder'], ct.CGI_FUS)

    # if the output file already exists, do not need to run the module if 'force_output' == False
    if not config['force_output'] and os.path.isfile(config['tcgi_fus']):
        logging.debug('Stage skipped: file {0} already exists'.format(config['tcgi_fus']))
        return config

    fus_df = pd.read_csv(config['drivers_fus'], sep='\t')

    # adapt for the in silico drug prescription
    fus_df = add_prescription_required_columns(fus_df, config)

    # create the final output column
    fus_df = insert_driver_status(fus_df)

    # order
    fus_df = order_output(fus_df)

    # output
    fus_df.to_csv(config['tcgi_fus'], sep='\t', index=False)
    logging.debug('File created {0}'.format(config['tcgi_fus']))

    return config
