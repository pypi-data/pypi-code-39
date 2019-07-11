import logging
import os

import numpy as np
import pandas as pd

import cancergenomeinterpreter.mut.modules.lib as lib
import cancergenomeinterpreter.mut.utils.constants as ct


def do_report(config: dict):
    report_d = {
        'cancer_type': [0, 'cancer', config['tumor_type']],
        # number of drivers found for the tumor and its offspring ('generic' = pancancer analysis, 'none' = any found)
        'cancer_offspring': [1, 'cancer offspring',
                             ','.join([e for e in config['tumor_offspring'] if e != config['tumor_type']])],
        'samples': [2, 'samples', '-'],
        'entries': [3, 'entries', '-'],
        'analysed_mutations': [4, 'analysed mutations', '-'],
        'drivers': [5, 'driver mutations', '-'],
        'known': [6, 'known oncogenic mutations', '-'],
        'predicted': [7, 'predicted driver mutations', '-'],
        'mutations_per_sample': [8, 'median mutations per sample', '-'],
        'drivers_per_sample': [9, 'median driver mutations per sample', '-'],
        'samples_without_drivers': [10, 'samples without any driver event', '-']
    }

    input_df = pd.read_csv(os.path.join(config['output_folder'], ct.INPUT_MUTS), sep='\t', comment='#')
    final_df = pd.read_csv(os.path.join(config['output_folder'], ct.FINAL_MUTS), sep='\t')

    drivers_df = final_df[final_df[ct.DRIVER_MUT_BOOL].isin([ct.KNOWN, ct.PREDICTED])]

    report_d['entries'][-1] = len(input_df)
    report_d['analysed_mutations'][-1] = len(final_df)
    report_d['drivers'][-1] = len(drivers_df)
    report_d['known'][-1] = len(final_df[final_df[ct.DRIVER_MUT_BOOL].isin([ct.KNOWN])])
    report_d['predicted'][-1] = len(final_df[final_df[ct.DRIVER_MUT_BOOL].isin([ct.PREDICTED])])
    report_d['samples'][-1] = len(final_df[ct.SAMPLE].unique())
    report_d['mutations_per_sample'][-1] = final_df.groupby(ct.SAMPLE).size().median()
    report_d['drivers_per_sample'][-1] = drivers_df.groupby(ct.SAMPLE).size().median() if len(drivers_df) > 0 else 0
    report_d['samples_without_drivers'][-1] = report_d['samples'][-1] - len(drivers_df[ct.SAMPLE].unique())

    if 'sample_drivers' in config:
        report_d['sample_drivers_number'] = [1, 'number of driver genes of the sample tumor (and offspring)',
                                             config['sample_drivers']]

    report_df = pd.DataFrame({'var': list(report_d.keys()), 'order': [e[0] for e in report_d.values()],
                              'description': [e[1] for e in report_d.values()],
                              'value': [e[-1] for e in report_d.values()]})

    # output
    report_fp = os.path.join(config['output_folder'], ct.REPORT)
    report_df.sort_values(by='order', ascending=True).to_csv(report_fp, sep='\t',
                                                             columns=['var', 'description', 'value'], index=False)
    logging.info('Summary of the results created {0}'.format(os.path.basename(report_fp)))

    return config


def order_output_rows(mutations_df: pd.DataFrame):
    logging.debug('Ordering rows..')

    i1 = mutations_df[mutations_df[ct.DRIVER_MUT_BOOL] == ct.KNOWN].index.tolist()
    i2 = mutations_df[mutations_df[ct.DRIVER_MUT_BOOL] == ct.PREDICTED].index.tolist()
    i3 = lib.difference_lists([mutations_df.index.tolist(), i1 + i2])

    mutations_df = mutations_df.ix[i1 + i2 + i3]

    return mutations_df


def add_prescription_required_columns(mutations_df: pd.DataFrame, config: dict):
    logging.debug('Adding extra columns required by in silico prescription..')

    mutations_df[ct.CANCER] = config['tumor_type']
    mutations_df[ct.ALT_TYPE] = 'MUT'

    if ct.SAMPLE not in mutations_df.columns.tolist():
        logging.debug('Default sample identifier inserted')
        mutations_df[ct.SAMPLE] = config['sample']

    return mutations_df


def recover_original_columns(mutations_df: pd.DataFrame, config: dict):
    logging.debug('Recovering original columns..')

    input_df = pd.read_csv(config['input_fp'], sep='\t')

    if ct.INTERNAL_ID not in mutations_df.columns.tolist() or ct.INTERNAL_ID not in input_df.columns.tolist():
        logging.warning('The internal id can not be found, so recovery of original columns can not be attempted')
        return mutations_df

    # those original columns already existing in the output file, i rename them
    for c in input_df.columns:
        if c != ct.INTERNAL_ID and c in mutations_df:
            input_df = input_df.rename(columns={c: c + ct.ORIGINAL_COLUMNS_SUFFIX})

    # keep the columns of each source to order them before returning the resulting merged dataframe
    original_cols = input_df.columns.tolist()
    extra_cols = mutations_df.columns.tolist()
    extra_cols.remove(ct.INTERNAL_ID)  # to avoid ask to output the ct.INTERNAL_ID column twice

    # merge
    mutations_df = mutations_df.merge(input_df, how='left', on=ct.INTERNAL_ID)

    # reorder columns
    mutations_df = mutations_df[original_cols + extra_cols]

    return mutations_df


def recover_input_prot_info(mutations_df: pd.DataFrame, config: dict):
    logging.debug('Recovering original info from the reverse protein mapping..')

    def get_coi_rev_prot(row):
        return pd.Series({ct.INTERNAL_ID: row['input'].split('|')[1],
                          ct.GDNA: row['coordinates(gDNA/cDNA/protein)'].split('/')[0],
                          ct.REV_TRANSCRIPT: row[ct.TRANSCRIPT].split(' ')[0]})

    # first, i need to read the original reverse protein results
    rev_prot_df = pd.read_csv(config['transvar_revprot_output'], sep='\t')

    # i create the columns i need in that rev prot file
    rev_prot_df = rev_prot_df.merge(rev_prot_df.apply(lambda row: get_coi_rev_prot(row), axis=1),
                                    left_index=True, right_index=True)

    # i collapse the transcripts used for reveresely mapping each protein change to each
    # gDNA (since the same mutation id can have actually several gdna
    transcripts_in_rev_mapping_df = rev_prot_df[[ct.INTERNAL_ID, ct.GDNA, ct.REV_TRANSCRIPT]] \
        .groupby([ct.INTERNAL_ID, ct.GDNA], axis=0, as_index=False).aggregate(lambda e: ','.join(e))

    # and merge to obtain the transcripts used to map each protein to each gDNA
    mutations_df[ct.INTERNAL_ID] = mutations_df[ct.INTERNAL_ID].astype(int)
    transcripts_in_rev_mapping_df[ct.INTERNAL_ID] = transcripts_in_rev_mapping_df[ct.INTERNAL_ID].astype(int)

    mutations_df = mutations_df.merge(transcripts_in_rev_mapping_df, how='left', on=[ct.INTERNAL_ID, ct.GDNA])

    # order just to put it nicer
    coi = [ct.PROT + ct.ORIGINAL_COLUMNS_SUFFIX, ct.INTERNAL_ID, ct.REV_TRANSCRIPT, ct.GDNA, ct.PROT, ct.TRANSCRIPT]
    mutations_df = mutations_df.reindex(columns=pd.Index(coi).append(mutations_df.columns.difference(coi)))

    return mutations_df


def deal_rev_mapping_issues(mutations_df: pd.DataFrame):
    """
    remove the duplicated entries due to rev mapping in which one of the
    possibilities is the sampe positons than the input
    """

    def get_diff_prot(row):

        tmp = row['protein_orig'].split(':')
        input_gene, input_prot = tmp[0], tmp[1]
        if row[ct.GENE] == input_gene and not lib.match_protein_pos(row[ct.PROT], input_prot):
            return '{0} reannotated in {1}'.format(row['protein_orig'], row[ct.TRANSCRIPT])

        return ''

    # annotation in the selected transcript is different than the one of the input
    mutations_df[ct.REV_MAP_ISSUE] = mutations_df.apply(lambda row: get_diff_prot(row), axis=1)

    # get the mutation ids that are repeated due to rev mapping
    counts = mutations_df.groupby([ct.INTERNAL_ID, ct.GENE]).size().reset_index()
    rep_ids = counts[counts[0] > 1][ct.INTERNAL_ID].unique()
    if len(rep_ids) > 0:
        text = 'There are {0} mutations duplicated due to reverse protein mapping'.format(len(rep_ids))
        # if one of the duplicated mutations match with the input, remove the others
        rep_ids_with_a_match = \
            mutations_df[(mutations_df[ct.INTERNAL_ID].isin(rep_ids)) & (mutations_df[ct.REV_MAP_ISSUE] == '')][
                ct.INTERNAL_ID].unique()

        if len(rep_ids_with_a_match) > 0:
            text += '; in {0} of them, one of the reannotated options matches with ' \
                    'the input so the rest is filtered out'.format(len(rep_ids_with_a_match))

            mutations_df = mutations_df[np.invert(
                (mutations_df[ct.INTERNAL_ID].isin(rep_ids_with_a_match)) & (mutations_df[ct.REV_MAP_ISSUE] != ''))]

        logging.debug(text)

    if len(mutations_df[mutations_df[ct.REV_MAP_ISSUE] != '']) > 0:
        logging.debug('Overall, there are {0} protein changes reannotated'.format(
            len(mutations_df[mutations_df[ct.REV_MAP_ISSUE] != ''])))

    return mutations_df


def remove_non_coding_duplicated(mutations_df):
    # get the internal_id of the mutations that are duplicated
    tmp = mutations_df.groupby(ct.INTERNAL_ID).size()
    dup_ids = tmp[tmp > 1].index.unique()

    # remove the entries with internal id duplicated and not coding
    i_to_remove = mutations_df[(mutations_df[ct.INTERNAL_ID].isin(dup_ids)) & (
        np.invert(mutations_df[ct.CONSEQUENCE_TYPE].isin(ct.PAM_CT)))].index
    size = len(mutations_df)
    mutations_df = mutations_df.ix[np.invert(mutations_df.index.isin(i_to_remove))]

    if len(mutations_df) < size:
        logging.debug('There is {0} duplicated non coding mutations removed'.format(size - len(mutations_df)))

    return mutations_df


def get_drivermut_statement(mutations_df: pd.DataFrame):
    logging.debug('Creating the driver mutation final category..')

    # the final label of oncodriveMUT
    def state_drivermut(row):

        # a) return the tumor types of a known mutation
        known = []
        if type(row[ct.KNOWN_ONCOGENIC]) == str:
            # if it s known oncogenic and neutral, that should be an error!
            if type(row[ct.KNOWN_NEUTRAL]) == str:
                logging.warning(
                    'The variant {0} is known to be neutral and oncogenic!!'.format(row[ct.GENE] + '-' + row[ct.PROT]))
            # if 'cancer' is included among other tumors, i remove it
            known.append(
                row[ct.KNOWN_ONCOGENIC].replace(ct.TUMORS_SEP + 'CANCER', '').replace('CANCER' + ct.TUMORS_SEP, ''))

        if type(row[ct.KNOWN_PREDISPOSING]) == str:
            # if it s known predisposing and neutral, that should be an error!
            if type(row[ct.KNOWN_NEUTRAL]) == str:
                logging.warning(
                    'The variant {0} is known to be neutral and oncogenic!!'.format(row[ct.GENE] + '-' + row[ct.PROT]))
            known.append(row[ct.KNOWN_PREDISPOSING])

        if len(known) > 0:
            return 'known in: ' + ';'.join(list(set([j for i in [k.split(ct.TUMORS_SEP) for k in known] for j in i])))

        # b) it is a known neutral mutation (at this moment, it comes from oncokb, o no cancer type is specified)
        if type(row[ct.KNOWN_NEUTRAL]) == str:
            return 'likely neutral for oncogenesis'

        # c) if it is a polymorphism
        if row[ct.EXAC_AF] >= ct.POLYM_AF:
            return ct.POLYM

        # d) else, return the label of the OncodriveMUT prediction
        prediction = row[ct.DRIVER_MUT_PREDICTION]
        if prediction == ct.PASSENGER:
            prediction = "predicted passenger"
        elif prediction in [ct.TIER_1, ct.TIER_2]:
            prediction = "predicted driver: " + prediction.lower()

        return prediction

    # whether the mutation is known, predicted or None
    def drivermut_bool(row):

        if 'known' in row[ct.DRIVER_MUT_STATEMENT]:
            return ct.KNOWN
        if 'driver' in row[ct.DRIVER_MUT_STATEMENT]:
            return ct.PREDICTED
        return ct.OTHER

    # the final label of oncodriveMUT
    mutations_df[ct.DRIVER_MUT_STATEMENT] = mutations_df.apply(lambda row: state_drivermut(row), axis=1)

    # a boolean saying if a mutation is driver (known/predicted) or no (empty)
    mutations_df[ct.DRIVER_MUT_BOOL] = mutations_df.apply(lambda row: drivermut_bool(row), axis=1)

    return mutations_df


def get_known_match(mutations_df: pd.DataFrame, config: dict):
    def is_match(row):

        if row[ct.DRIVER_MUT_BOOL] == ct.KNOWN:
            known_tumors = row[ct.DRIVER_MUT_STATEMENT].replace(' ', '').split(':')[1].split(ct.TUMORS_SEP)

            # i want an exact match here; therefore, i do not check the offspring of the known mutation;
            # in other words, known in lung does not match with LUSC
            if len(lib.intersect_lists([known_tumors, config['tumor_offspring']])) > 0:
                return ct.KNOWN_MATCH

        return ''

    mutations_df[ct.KNOWN_MATCH] = mutations_df.apply(lambda row: is_match(row), axis=1)

    return mutations_df


def concat_known_sources(mutations_df):
    def join_columns(df, labelin_1, labelin_2, labelin_3, labelout):
        def concat(e1, e2, e3):
            return pd.Series([e1, e2, e3]).str.cat(sep=ct.SEPARATOR)

        tmp_df = mutations_df.dropna(subset=[labelin_1, labelin_2, labelin_3],
                                     how='all')  # remember to put how='all' so you remove when both are empty

        # there is at least one emtry with known content
        if len(tmp_df) > 0:
            tmp_df.loc[:, labelout] = tmp_df.apply(lambda row: concat(row[labelin_1], row[labelin_2], row[labelin_3]),
                                                   axis=1)
            return tmp_df.append(df.ix[np.invert(df.index.isin(tmp_df.index))], sort=True)

        # no entry with known content
        df.loc[:, labelout] = np.nan
        return df

    mutations_df = join_columns(mutations_df, 'known_predisposing_source', 'known_oncogenic_source',
                                'known_neutral_source', ct.KNOWN_VARIANT_SOURCE)
    mutations_df = join_columns(mutations_df, 'known_predisposing_reference', 'known_oncogenic_reference',
                                'known_neutral_reference', ct.KNOWN_VARIANT_REFERENCE)

    return mutations_df


def report_lost_mutations(mutations_df, config):
    in_ids = pd.read_csv(config['input_fp'], sep='\t')[ct.INTERNAL_ID]
    out_ids = mutations_df[ct.INTERNAL_ID]

    not_mapped_ids = lib.difference_lists([in_ids, out_ids])
    if len(not_mapped_ids) > 0:
        logging.warning(
            'There are {0} input mutations that have been not processed due to format/mapping problems'.format(
                len(not_mapped_ids)))

    if config['input_format'] == ct.PROT_FORMAT:
        counts = mutations_df.groupby(ct.INTERNAL_ID).size().reset_index().rename(columns={0: 'counts'})
        counts = counts[counts['counts'] > 1]
        if len(counts) > 0:
            logging.info(
                'There are {0} input aminoacid changes that created multiple output rows due to '
                'not-unequivocal reverse mapping to DNA'.format(
                    len(counts)))

    return


def run(config: dict):
    logging.info('Arranging the output')

    # retrieve the paths of the outputed files
    out_fp = os.path.join(config['output_folder'], ct.FINAL_MUTS)
    config['oncodrivemut_output_fp'] = out_fp

    # assess if i need to run this stage by checking whether the *final* outputed file already exists
    if not config['force_output'] and os.path.isfile(out_fp):
        logging.debug('Stage skipped: file {0} already exists'.format(out_fp))
        return config

    mutations_df = pd.read_csv(config['driver_prediction_fp'], sep='\t')

    # Recover the original columns of the input file unless the input file was a vcf (then all the columns has been
    # kept during the whole pipeline and we do not need to recover them in the last step)
    if config['input_format'] != ct.VCF_FORMAT:
        mutations_df = recover_original_columns(mutations_df, config)

    # In case the input is in protein format, this step also recover the original protein input and the transcripts
    # used for each protein <-> dna mapping
    if config['input_format'] == ct.PROT_FORMAT:
        mutations_df = recover_input_prot_info(mutations_df, config)

    # In case the input is in protein format, create a column stating (a) if a mutation is not unequivocal;
    # (b) if a mutation has a different aminoacid change
    if config['input_format'] == ct.PROT_FORMAT:
        mutations_df = deal_rev_mapping_issues(mutations_df)

    # if a mutation is duplicated due to mapping, remove the one non-coding
    mutations_df = remove_non_coding_duplicated(mutations_df)

    # adapt for the in silico drug prescription
    mutations_df = add_prescription_required_columns(mutations_df, config)

    # create the final oncodriveMUT column
    mutations_df = get_drivermut_statement(mutations_df)

    # only for known mutations, whether the tumor type match with the sample tumor
    mutations_df = get_known_match(mutations_df, config)

    # only for known mutations, create a final column merging sources and references
    mutations_df = concat_known_sources(mutations_df)

    # order the rows of the output
    mutations_df = order_output_rows(mutations_df)

    # track the mutations that have been lost
    report_lost_mutations(mutations_df, config)

    # output
    mutations_df.to_csv(config['oncodrivemut_output_fp'], sep='\t', index=False)
    logging.info('File created with {0} entries: {1}'.format(len(mutations_df),
                                                             os.path.basename(config['oncodrivemut_output_fp'])))

    # do report
    config = do_report(config)

    return config
