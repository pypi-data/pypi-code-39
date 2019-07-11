import logging
import os
import sys

import numpy as np
import pandas as pd

import cancergenomeinterpreter.mut.utils.constants as ct


def known_split_in_dna_and_prot(df):
    def collapse_values(tumor_se):
        return ct.SEPARATOR.join(list(set(list(tumor_se))))

    # select those entries in which the protein change does not exist (e.g. because it is a splice site variant
    dna_df = df[df[ct.PROT].isin(['.'])].copy()
    dna_df.loc[:, 'key'] = dna_df[ct.GDNA]

    # for those entries with protein change stated, collapse if the same protein change
    # appears several times (this should not happen if the file is ok!)
    prot_df = df[np.invert(df.index.isin(dna_df.index))]
    prot_df = prot_df.groupby([ct.GENE, ct.PROT]).agg(collapse_values).reset_index()  # [[ct.GENE, ct.PROT, label]]
    try:
        prot_df['key'] = prot_df[ct.PROT]
    except KeyError:  # possible due to empty df
        prot_df = pd.DataFrame()

    # append the entries
    out_df = dna_df.append(prot_df, sort=True)

    return out_df


# the known oncogenic file is assumed to have a field called 'source' and 'reference'
def match_known_oncogenic(mutation_df, run_info_d):
    def replace_is_known_inframe(row):
        # this condition is hard coded while waiting to implement the special regional conditions overlap
        cond = (row[ct.GENE] == 'EGFR') & ((row[ct.CONSEQUENCE_TYPE] in ct.INFRAME_CT and row[ct.EXON] == 19) |
                                           (row[ct.CONSEQUENCE_TYPE] == ct.INFRAME_CT[1] and row[ct.EXON] == 20))
        if cond:
            return 'L'

        return row[ct.KNOWN_ONCOGENIC]

    logging.debug('Matching protein/gDNA coordinates of the mutations with known oncogenic events..')

    known_oncogenic_df = pd.read_csv(run_info_d['known_oncogenic_fp'], sep='\t')

    # just in case there is some duplicate value
    duplicated_df = known_oncogenic_df[known_oncogenic_df.duplicated(subset=['gdna'], keep='first')]
    if len(duplicated_df):
        logging.warning('There are {0} entries duplicated in the known oncogenic dataset'.format(len(duplicated_df)))
        known_oncogenic_df = known_oncogenic_df.drop_duplicates(subset='gdna')

    for c in [ct.GDNA, ct.GENE, ct.PROT]:
        if c not in known_oncogenic_df.columns:
            logging.error('ERROR: The file {0} has no column named {1}!!'.format(run_info_d['known_oncogenic_fp'], c))
            sys.exit(-1)

    # rename columns and drop duplicates because in that file, a single mutation may
    # map to two genes and thus has two entries
    # TODO: remove it in the metadata file, and not here
    known_oncogenic_df = known_oncogenic_df.rename(columns={'cancer_acronym': ct.KNOWN_ONCOGENIC})
    known_oncogenic_df = known_oncogenic_df.drop_duplicates([ct.GDNA, ct.KNOWN_ONCOGENIC])
    known_oncogenic_df = known_oncogenic_df.rename(
        columns={'source': 'known_oncogenic_source', 'reference': 'known_oncogenic_reference'})

    # divide the known mutations depending on they have protein changes (and then collapse to
    # avoid duplicated protein changes) and dna
    known_oncogenic = known_split_in_dna_and_prot(known_oncogenic_df)

    # merge with the input file (note that i include the gene name because one mutation can
    # map to two genes) by the key, which is the dna change if the protein change is not available
    # (e.g. for splice variants that have only the dna change) or the protein change otherwise
    mutation_df['key'] = np.where(mutation_df[ct.PROT].isin(['.']), mutation_df[ct.GDNA], mutation_df[ct.PROT])
    mutation_df = mutation_df.merge(
        known_oncogenic[[ct.GENE, ct.KNOWN_ONCOGENIC, 'key', 'known_oncogenic_source', 'known_oncogenic_reference']],
        how='left', on=[ct.GENE, 'key'])

    # remove the tmp key
    mutation_df = mutation_df.drop(['key'], 1)

    # special condition for egfr inframe indels that are known but the current match script is not suited to detect them
    mutation_df[ct.KNOWN_ONCOGENIC] = mutation_df.apply(lambda row: replace_is_known_inframe(row), axis=1)

    return mutation_df


# the known benign file is assumed to have a field called 'source' and 'reference'
def match_known_neutral(mutation_df, run_info_d):
    logging.debug('Matching protein/gDNA coordinates of the mutations with known neutral events..')

    known_neutral_df = pd.read_csv(run_info_d['known_neutral_fp'], sep='\t')

    for c in [ct.GDNA, ct.GENE, ct.PROT]:
        if c not in known_neutral_df.columns:
            logging.error('ERROR: The file {0} has no column named {1}!!'.format(run_info_d['known_neutral_fp'], c))
            sys.exit(-1)

    # rename columns and drop duplicates because in that file, a single mutation may map to
    # two genes and thus has two entries
    # TODO: remove it in the metadata file, and not here
    known_neutral_df = known_neutral_df.rename(columns={'cancer_acronym': ct.KNOWN_NEUTRAL})

    # just in case there are duplicated entries
    duplicated_df = known_neutral_df[known_neutral_df.duplicated(subset=['gdna'], keep='first')]
    if len(duplicated_df):
        logging.warning('There are {0} entries duplicated in the known neutral dataset'.format(len(duplicated_df)))
        known_neutral_df = known_neutral_df.drop_duplicates(subset='gdna')

    known_neutral_df = known_neutral_df.drop_duplicates([ct.GDNA, ct.KNOWN_NEUTRAL])
    known_neutral_df = known_neutral_df.rename(
        columns={'source': 'known_neutral_source', 'reference': 'known_neutral_reference'})

    # divide the known mutations depending on they have protein changes
    # (and then collapse to avoid duplicated protein changes) and dna
    known_neutral_df = known_split_in_dna_and_prot(known_neutral_df)

    mutation_df['key'] = np.where(mutation_df[ct.PROT].isin(['.']), mutation_df[ct.GDNA], mutation_df[ct.PROT])
    mutation_df = mutation_df.merge(
        known_neutral_df[[ct.GENE, ct.KNOWN_NEUTRAL, 'key', 'known_neutral_source', 'known_neutral_reference']],
        how='left', on=[ct.GENE, 'key'])

    # remove the tmp key
    mutation_df = mutation_df.drop(['key'], 1)

    return mutation_df


# the known predisposing file is assumed to have a field called 'source' and 'reference'
def match_known_predisposing(mutation_df, run_info_d):
    logging.debug('Matching protein/gDNA coordinates of the mutations with known predisposing variants..')

    known_predisposing_df = pd.read_csv(run_info_d['known_predisposing_fp'], sep='\t')

    # just in case there is some duplicate value
    duplicated_df = known_predisposing_df[known_predisposing_df.duplicated(subset=['gdna'], keep='first')]
    if len(duplicated_df):
        logging.warning('There are {0} entries duplicated in the known predisposing dataset'.format(len(duplicated_df)))
        known_predisposing_df = known_predisposing_df.drop_duplicates(subset='gdna')

    known_predisposing_df = known_predisposing_df.rename(
        columns={'source': 'known_predisposing_source', 'reference': 'known_predisposing_reference'})

    for c in [ct.GDNA, ct.GENE, ct.PROT]:
        if c not in known_predisposing_df.columns:
            logging.error(
                'ERROR: The file {0} has no column named {1}!!'.format(run_info_d['known_predisposing_fp'], c))
            sys.exit(-1)

    # rename columns and drop duplicates because in that file, a single mutation may map
    # to two genes and thus has two entries
    # TODO: remove it in the metadata file, and not here
    known_predisposing_df = known_predisposing_df.rename(columns={'cancer_acronym': ct.KNOWN_PREDISPOSING})
    known_predisposing_df = known_predisposing_df.drop_duplicates([ct.GDNA, ct.KNOWN_PREDISPOSING])

    # divide the known mutations depending on they have protein changes (and then collapse to avoid
    # duplicated protein changes) and dna
    known_predisposing_df = known_split_in_dna_and_prot(known_predisposing_df)

    # merge with the input file (note that i include the gene name because one mutation can map to
    # two genes) by prot if availabe by dna if not
    mutation_df.loc[:, 'key'] = np.where(mutation_df[ct.PROT].isin(['.']), mutation_df[ct.GDNA], mutation_df[ct.PROT])
    mutation_df = mutation_df.merge(known_predisposing_df[
                                        [ct.GENE, ct.KNOWN_PREDISPOSING, 'key', 'known_predisposing_source',
                                         'known_predisposing_reference']],
                                    how='left', on=[ct.GENE, 'key'])

    # remove the tmp key
    mutation_df = mutation_df.drop(['key'], 1)

    return mutation_df


def match_domains(mutation_df, config):
    def is_domain_overlapped(row):
        try:
            if int(row['Pfam start'] <= int(row[ct.AA_POS])) and int(row[ct.AA_POS]) <= int(row['Pfam end']):
                return 1
            return 0
        except Exception:
            return 0

    logging.debug('Matching with Pfam domains by using protein positions..')

    if ct.TRANSCRIPT not in mutation_df.columns:
        logging.error('ERROR: The mutation file has no column named "transcript" as expected!!')
        sys.exit(-1)

    # read and format pfam file
    pfam_df = pd.read_csv(config['pfam_fp'], sep='\t')
    pfam_df = pfam_df.rename(columns={'Ensembl Transcript ID': ct.TRANSCRIPT, 'Pfam domain': ct.PFAM_DOMAIN})

    # integrate pfam data
    mutation_df = mutation_df.merge(pfam_df[[ct.TRANSCRIPT, 'Pfam start', 'Pfam end', ct.PFAM_DOMAIN]], how='left',
                                    on=ct.TRANSCRIPT)

    # for all the gene pfam domains, see if there is overlap with the protein change
    mutation_df['Pfam_overlap'] = mutation_df.apply(lambda row: is_domain_overlapped(row), axis=1)

    # this drop duplicates is necessary because i did the merge at the level of transcript, so all the
    # mutation of a gene are duplicated by all the Pfam entries of that gene. Therefore, this dropduplciates
    # solves this issue by keeping that entry that overlaps (if any) with the pfam domain
    #  (note that the drop duplicates also take into account gdna, because vcf with several alt alleles
    #   creates several ouptuts with the same input, and transcript, becasue the same input can map to two genes)
    mutation_df = mutation_df.sort_values(by=['input', 'Pfam_overlap'], ascending=False) \
        .drop_duplicates(['input', ct.TRANSCRIPT, ct.GDNA, ct.INTERNAL_ID], keep='first')

    # recodify to have a filled domain field only if indeed there is match
    mutation_df[ct.PFAM_DOMAIN] = np.where(mutation_df['Pfam_overlap'] == 1, mutation_df[ct.PFAM_DOMAIN], '')

    # remove tmp columns
    mutation_df = mutation_df.drop(['Pfam start', 'Pfam end', 'Pfam_overlap'], 1)

    return mutation_df


def match_polymorphisms(mutation_df, run_info_d):
    logging.debug('Matching with polymorphisms rettrieved from Exac..')

    polym_df = pd.read_csv(run_info_d['polym_fp'], sep='\t')
    polym_df = polym_df.rename(columns={polym_df.columns[1]: ct.EXAC_AF})

    # merge
    mutation_df = mutation_df.merge(polym_df, on=ct.GDNA, how='left')

    return mutation_df


def match_transcript_metadata(mutation_df: pd.DataFrame, config: dict):
    logging.debug('Matching with transcript metadata..')

    transcript_df = pd.read_csv(config['transcript_metrics_fp'], sep='\t')
    transcript_df = transcript_df.rename(
        columns={'Ensembl Transcript ID': ct.TRANSCRIPT, 'transcript_exons': ct.TRANSCRIPT_EXONS,
                 'transcript_aminoacids': ct.TRANSCRIPT_AMINOACIDS})

    # merge
    mutation_df = mutation_df.merge(transcript_df[[ct.TRANSCRIPT, ct.TRANSCRIPT_AMINOACIDS, ct.TRANSCRIPT_EXONS]],
                                    how='left',
                                    on=ct.TRANSCRIPT)
    return mutation_df


def match_fiscore(mutation_df: pd.DataFrame, config: dict):
    def create_fiscore_key(row, cols):
        return '|'.join([str(row[cols[0]]), str(row[cols[1]]), row[cols[2]], row[cols[3]]])

    if not os.path.isfile(config['fiscore_output_fp']):
        logging.debug('No functional impact score available')
        mutation_df[ct.FISCORE_SCORE] = ''
        return mutation_df

    logging.debug('Matching with functional impact scores obtained in a previous step..')
    fiscore_output_df = pd.read_csv(config['fiscore_output_fp'], sep='\t', skiprows=1)
    fiscore_output_df = fiscore_output_df.rename(columns={'FISCORE': ct.FISCORE_SCORE})

    # if the input format is vcf, i can merge by the vcf coordinates
    if config['input_format'] == ct.VCF_FORMAT:
        fiscore_output_df['input'] = fiscore_output_df.apply(lambda row: create_fiscore_key(row, fiscore_output_df.columns), axis=1)
        mutation_df = mutation_df.merge(fiscore_output_df[['input', ct.FISCORE_SCORE]], how='left', on='input')

    # if the input file is not a vcf, i need to check the input file passed to fiscore to recover the original gdna key
    # to do the merge with the score in the fiscore output file
    else:
        fiscore_input_df = pd.read_csv(config['fiscore_input_fp'], sep='\t')

        # merge the fiscore files to have the gdna key (from the fiscore input) and the score
        # (from the fiscore output) in a single file
        fiscore_df = fiscore_output_df.merge(fiscore_input_df, how='outer', left_on=fiscore_output_df.columns.tolist()[0:4],
                                       right_on=[fiscore_input_df.columns.tolist()[i] for i in [0, 1, 3, 4]])

        # merge
        mutation_df = mutation_df.merge(fiscore_df[[ct.GDNA, ct.FISCORE_SCORE]], how='left', on=ct.GDNA)

    fiscore_na_df = mutation_df[mutation_df[ct.FISCORE_SCORE].isnull()]
    if len(fiscore_na_df) > 0 and config['extended']:
        logging.warning('There are {0} entries with no functional impact scores:'.format(len(fiscore_na_df)))
        logging.debug('They are:\n{0}'.format(fiscore_na_df[[ct.GDNA]]))

    return mutation_df


def run(config: dict):
    logging.info('Matching with several metadata files')

    # retrieve the paths of the outputed files
    out_fp = os.path.join(os.path.join(config['tmp_folder'], ct.METADATA_MUTS))
    config['metadata_output_fp'] = out_fp

    # assess if i need to run this stage by checking whether the *final* outputed file already exists
    if not config['force_output'] and os.path.isfile(out_fp):
        logging.debug('Stage skipped: file {0} already exists'.format(out_fp))
        return config

    mutation_df = pd.read_csv(config['annotated_mutations_fp'], sep='\t')

    # match with transcript metrics metadata
    mutation_df = match_transcript_metadata(mutation_df, config)

    # match with known oncogenic mutations
    mutation_df = match_known_oncogenic(mutation_df, config)

    # match with known benign mutations
    mutation_df = match_known_neutral(mutation_df, config)

    # match with known cancer predisposing variants
    mutation_df = match_known_predisposing(mutation_df, config)

    # match with polymorphisms
    mutation_df = match_polymorphisms(mutation_df, config)

    # match with pfam
    mutation_df = match_domains(mutation_df, config)

    # match with fiscore (that have been obtained before)
    mutation_df = match_fiscore(mutation_df, config)

    # output
    metadata_output_fp = config['metadata_output_fp']
    mutation_df.to_csv(metadata_output_fp, index=False, sep='\t')
    logging.debug('File with {0} entries created: {1}'.format(len(mutation_df), metadata_output_fp))

    return config
