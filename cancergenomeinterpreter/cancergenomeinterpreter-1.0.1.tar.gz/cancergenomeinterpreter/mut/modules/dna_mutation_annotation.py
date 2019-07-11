import logging
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

import cancergenomeinterpreter.mut.modules.lib as lib
import cancergenomeinterpreter.mut.utils.constants as ct
from cancergenomeinterpreter.mut.utils.progress import ProgressBar


def recover_not_mapped_fs(transvar_dna_out_df: pd.DataFrame, config: dict):
    """
    if input fs protein withou length, recover them here
    """

    fp = os.path.join(config['tmp_folder'], ct.FS_NOT_MAPPED)
    if not os.path.isfile(fp):
        return transvar_dna_out_df

    # remember to drop the column gdna from the non mapped frameshigts to avoid prblems
    non_mapped_fs_df = pd.read_csv(fp, sep='\t')
    non_mapped_fs_df = non_mapped_fs_df.drop('gdna', 1)
    # concat the two, remember to reset the index or it will be problematic for the merge actions based on index
    transvar_dna_out_df = pd.concat([transvar_dna_out_df, non_mapped_fs_df]).reset_index(drop=True)
    logging.debug('{0} not mapped frameshifts recovered'.format(len(non_mapped_fs_df)))

    return transvar_dna_out_df


def select_mutation_transcript(transvar_dna_out_df: pd.DataFrame, chosen_transcripts_fp: str):
    """
    Take the transvar annotated file and select one transcript per mutated gene

    :param transvar_dna_out_df:
    :param chosen_transcripts_fp:
    :return:
    """

    def ref_trans(t):
        return t.split(' ')[0]

    logging.info('Selecting one transcript per gene for annotation..')
    transvar_dna_out_df['transcript'] = transvar_dna_out_df['transcript'].map(ref_trans)

    chosen_transcripts_df = pd.read_csv(chosen_transcripts_fp, sep='\t')
    chosen_transcripts = chosen_transcripts_df[chosen_transcripts_df.columns[1]]

    out_df = transvar_dna_out_df[transvar_dna_out_df['transcript'].isin(chosen_transcripts)]

    genes_i, genes_o = transvar_dna_out_df['gene'].unique(), out_df['gene'].unique()
    if len(genes_i) > len(genes_o):
        logging.debug('The following genes have no transcript chosen and are not passed downstream: {0}'
                      .format(lib.difference_lists([genes_i, genes_o])))

    if len(genes_o) == 0:
        logging.error('ERROR: after the transcript filtering, there is no gene mutation to process!')
        sys.exit(-1)

    return out_df


def format_mutation_annotation(annotated_df: pd.DataFrame, config: dict):
    """
    I split the gDNA/cDNA/protein coordinates in three columns;
    I create the consequence type columns
    If the file is vcf, I create the input column

    :param annotated_df:
    :param config:
    :return:
    """

    def get_ct(info_field):
        try:
            return info_field.split('CSQN=')[1].split(';')[0]
        except Exception:
            return 'N/A'

    def get_exon(region_field):
        if 'cds_in_exon' in region_field:
            try:
                return int(''.join(re.findall("\d", region_field)))
            except Exception:
                logging.warning('I can not find the exon number in region entry {0}'.format(region_field))
                return '-'
        return '-'

    # put the gDNA/cDNA/protein coordinates in three columns: 'gDNA' 'cDNA' 'protein'
    annotated_df = annotated_df.merge(
        annotated_df.apply(lambda row: lib.split_transvar_coordinates(row['coordinates(gDNA/cDNA/protein)'])
                           , axis=1), left_index=True, right_index=True)

    annotated_df = annotated_df.drop(['coordinates(gDNA/cDNA/protein)'], 1)

    # create the ct column
    annotated_df[ct.CONSEQUENCE_TYPE] = annotated_df['info'].map(get_ct)

    # create the exon column
    annotated_df[ct.EXON] = annotated_df['region'].map(get_exon)

    # get the protein position and the aminoacid ref/alt as it is necessary for the
    # driver call (and later for the in silico prescription)
    annotated_df = annotated_df.merge(annotated_df.apply(lambda row: lib.retrieve_prot_entries(row[ct.PROT]), axis=1),
                                      left_index=True, right_index=True)

    input_format = config['input_format']

    # if the file is vcf, i will create the input column by myself from the columns present in the outputed file
    if input_format == ct.VCF_FORMAT:
        annotated_df['input'] = annotated_df[annotated_df.columns[0]].astype(str) + '|' + \
                                annotated_df[annotated_df.columns[1]].astype(str) + '|' + \
                                annotated_df[annotated_df.columns[3]] + '|' + annotated_df[annotated_df.columns[4]]
        cols = list(annotated_df.columns)
        annotated_df = annotated_df[[cols[-1]] + [cols[2]] + cols[5:-1]]

    return annotated_df


def run_transvar(config: dict):
    """
    Run the transvar command to annotate the mutations in dna coordinates, always using ENSEMBL

    :param config: The configuration dictionary
    :return:
    """
    transvar_dna_input_fp = config['transvar_dna_input']
    input_format = config['input_format']

    # select the arguments depending on the input format
    if input_format == ct.VCF_FORMAT:
        arg = '--vcf'
    else:
        arg = '-l'

    # run the command
    cmd = " ".join([
        'transvar ganno',
        arg,
        transvar_dna_input_fp,
        '--ensembl',
        '--seqmax -1'])

    logging.debug('Executing command: {0}'.format(cmd))

    progress_bar = ProgressBar(message_prefix="Running TransVar")
    progress_bar.start()

    try:
        fnull = open(os.devnull, 'w')
        results = subprocess.check_output(cmd, shell=True, stderr=fnull)
    except Exception:
        logging.error('Some problem occurred when trying to execute command {0}'.format(cmd))
        sys.exit(-1)
    finally:
        progress_bar.stop()

    return results


def run(config: dict):
    """
    Annotate the nucleotide mutations to protein coordicates per transcript

    :param config: The config dictionary
    :return: The config dictionary
    """

    logging.info('Annotating the nucleotide mutations to protein coordinates per transcript')

    # retrieve the paths of the output files
    out_fp = os.path.join(config['tmp_folder'], ct.ANNOTATED_MUTS)
    config['annotated_mutations_fp'] = out_fp
    config['transvar_dna_input'] = os.path.join(config['tmp_folder'], ct.TRANSVAR_DNA_INPUT)

    # assess if i need to run this stage by checking whether the *final* outputed file already exists
    if not config['force_output'] and os.path.isfile(out_fp):
        logging.debug('Stage skipped: file {0} already exists'.format(out_fp))
        return config

    # the input keep only the first field and locate the second in the internal id column
    def extract_internal_id(df):

        def splt(i):
            i_s = i.split('|')
            return pd.Series({'input': i_s[0], ct.INTERNAL_ID: i_s[1]})

        df2 = df.copy().drop(['input'], 1)
        df2 = df2.merge(df.apply(lambda row: splt(row['input']), axis=1), left_index=True, right_index=True)

        # reorder
        df2 = df2.reindex(
            columns=pd.Index(['input', ct.INTERNAL_ID]).append(df.columns.difference(['input', ct.INTERNAL_ID])))

        return df2

    # -- run transvar ganno --
    results = run_transvar(config)

    # put the transvar output in a dataframe (since i need extra ops)
    transvar_dna_out_df = lib.transvarb2df(results)

    # output the transvar file as it is created
    transvar_dna_output_fp = os.path.join(config['tmp_folder'], ct.TRANSVAR_DNA_OUTPUT)
    config['transvar_dna_output_fp'] = transvar_dna_output_fp
    transvar_dna_out_df.to_csv(transvar_dna_output_fp, sep='\t', index=False)
    logging.debug(
        'Temporal file with {0} entries created: {1}'.format(len(transvar_dna_out_df), transvar_dna_output_fp))

    # recover internal id from the 'input' column if it is not a vcf format
    # (since the ganno vcf already keep the columns separated instead of concatening
    # the extra columns in the 'input' column)
    if config['input_format'] != ct.VCF_FORMAT:
        transvar_dna_out_df = extract_internal_id(transvar_dna_out_df)

    # if the input is protein format, i recover here the non mapped frameshift mutations
    if config['input_format'] == ct.PROT_FORMAT:
        transvar_dna_out_df = recover_not_mapped_fs(transvar_dna_out_df, config)

    # separate the non mapped variants to output in a separate file
    not_mapped_dna_variants_df = transvar_dna_out_df[transvar_dna_out_df.apply(
        lambda row: lib.incorrect_transvar_map(row['coordinates(gDNA/cDNA/protein)'].split('/')[0], row['info']), axis=1
    )]
    
    if len(not_mapped_dna_variants_df) > 0:

        # keep the correctly mapped ones for inputing to the next module
        transvar_dna_out_df = transvar_dna_out_df[
            np.invert(transvar_dna_out_df.index.isin(not_mapped_dna_variants_df.index))]

        # output the incorrectly mapped variants, but only if the mutation has no correct mapping
        not_mapped_dna_variants_df = not_mapped_dna_variants_df[
            np.invert(not_mapped_dna_variants_df[ct.INTERNAL_ID].isin(transvar_dna_out_df[ct.INTERNAL_ID]))]

        if len(not_mapped_dna_variants_df) > 0:
            not_mapped_variants_fp = os.path.join(config['tmp_folder'], ct.GANNO_NOT_MAPPED)
            not_mapped_dna_variants_df.to_csv(not_mapped_variants_fp, sep='\t', index=False)
            logging.debug('File with non mapped entries created: {0}'.format(not_mapped_variants_fp))

        eoi = len(not_mapped_dna_variants_df.drop_duplicates(ct.INTERNAL_ID))
        if eoi > 0:
            if eoi > (len(transvar_dna_out_df.drop_duplicates(ct.INTERNAL_ID)) * ct.MAX_NONMAPPED_RATIO) + \
                    config['recoverable_fs']:
                text = 'There are more than {0}% of the entries that can not be mapped'.format(
                    ct.MAX_NONMAPPED_RATIO * 100)
                if config['input_format'] in [ct.GDNA_FORMAT, ct.FREE_FORMAT]:
                    text += '. Maybe the mutations are not annotated in the positive strand?'
                logging.error(text)
                logging.error('The CGI will stop the analysis, since the data seems not consistent')
                sys.exit(-1)
            logging.warning('There are {0} mutations that can not be mapped to a certain gene transcript'.format(eoi))

    # if the input is protein format, i recover here the non mapped frameshift mutations
    if config['input_format'] == ct.PROT_FORMAT:
        transvar_dna_out_df = recover_not_mapped_fs(transvar_dna_out_df, config)

    # transvar map each mutation per all the transcripts, here i select only the annotations per canonical transcript
    annotated_df = select_mutation_transcript(transvar_dna_out_df, config['chosen_transcripts_fp'])

    # do some formating of the resulting transvar results, including the split of the gDNA coordinates in a separate
    # column in the case of the input is protein, here i also state more info in the input column
    annotated_df = format_mutation_annotation(annotated_df, config)

    # and output these results in a file placed in the root
    annotation_output_fp = config['annotated_mutations_fp']
    annotated_df.to_csv(annotation_output_fp, sep='\t', index=False)
    logging.debug('File with {0} entries created: {1}'.format(len(annotated_df), annotation_output_fp))

    return config
