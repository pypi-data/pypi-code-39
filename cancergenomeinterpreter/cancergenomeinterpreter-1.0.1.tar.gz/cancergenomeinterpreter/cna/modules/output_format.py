import logging
import os

import numpy as np
import pandas as pd
import cancergenomeinterpreter.utils.constants as ct
import cancergenomeinterpreter.utils.lib as lib


def add_prescription_required_columns(cna_df, config):
    cna_df[ct.CANCER] = config['tumor_type']

    # add gene role
    role_df = pd.read_csv(config['gene_role_fp'], sep='\t')
    role_df = role_df.rename(columns={role_df.columns[0]: ct.GENE, role_df.columns[-1]: ct.GENE_ROLE})
    cna_df = cna_df.merge(role_df[[ct.GENE, ct.GENE_ROLE]], how='left', on=ct.GENE)
    cna_df[ct.GENE_ROLE] = np.where(cna_df[ct.GENE_ROLE].isnull(), ct.AMBIGUOUS, cna_df[ct.GENE_ROLE])

    return cna_df


def insert_driver_status(cna_df):
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
        elif row[ct.PREDICTED_MATCH] == 'match':
            cat = ct.PREDICTED
            statement = 'predicted driver'
        else:
            cat = ''
            statement = 'predicted passenger'

        return pd.Series({ct.ONCOGENIC: cat, ct.ONCOGENIC_CLASSIFICATION: statement})

    cna_df = cna_df.merge(cna_df.apply(lambda row: get_oncogenic_classification(row), axis=1), left_index=True,
                          right_index=True)

    return cna_df


def order_output(cna_df):
    # order rows
    i1 = cna_df[cna_df[ct.ONCOGENIC] == ct.KNOWN].index.tolist()
    i2 = cna_df[cna_df[ct.ONCOGENIC] == ct.PREDICTED].index.tolist()
    i3 = list(set(cna_df.index.tolist()) - set(i1 + i2))

    cna_df = cna_df.ix[i1 + i2 + i3]

    # order columns
    c1 = [ct.SAMPLE, ct.GENE, ct.CNA]
    c3 = [ct.ONCOGENIC, ct.ONCOGENIC_CLASSIFICATION, ct.PREDICTED_MATCH, ct.KNOWN_MATCH]
    c2 = lib.difference_lists([cna_df.columns, c1 + c3])

    cna_df = cna_df[c1 + c2 + c3]

    return cna_df


def run(config: dict):
    logging.info('Formating the output')

    # retrieve the output file
    config['tcgi_cnas'] = os.path.join(config['output_folder'], ct.CGI_CNAS)

    # if the output file already exists, do not need to run the module if 'force_output' == False
    if not config['force_output'] and os.path.isfile(config['tcgi_cnas']):
        logging.debug('Stage skipped: file {0} already exists'.format(config['tcgi_cnas']))
        return config

    cna_df = pd.read_csv(config['drivers_cnas'], sep='\t')

    # adapt for the in silico drug prescription
    cna_df = add_prescription_required_columns(cna_df, config)

    # create the final output column
    cna_df = insert_driver_status(cna_df)

    # order
    cna_df = order_output(cna_df)

    # output
    cna_df.to_csv(config['tcgi_cnas'], sep='\t', index=False)
    logging.debug('File created {0}'.format(config['tcgi_cnas']))

    return config
