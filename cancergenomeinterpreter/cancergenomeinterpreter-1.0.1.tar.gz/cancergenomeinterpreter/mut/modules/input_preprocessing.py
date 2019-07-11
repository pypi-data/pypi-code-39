import csv
import logging
import os
import subprocess
import sys

import itab
import numpy as np
import pandas as pd
from itab.files import open_file

import cancergenomeinterpreter.mut.modules.lib as lib
import cancergenomeinterpreter.mut.utils.constants as ct

# Input file column definitions
CHROMOSOME_FIELD = {'nullable': False,
                    'reader': "str(x).upper().replace('CHR', '').replace('24', 'X').replace('25', 'Y')",
                    'validator': "x in ([str(c) for c in range(1,23)] + ['X', 'Y'])"}
POSITION_FIELD = {'nullable': False, 'reader': "int(x)", 'validator': "x > 0"}
STRAND_FIELD = {'nullable': True, 'validator': "x  in '+-'"}
REF_FIELD = {'nullable': False, 'reader': "str(x).upper()", 'validator': "re.match('^[ACTGN-]*$', x) is not None"}
ALT_FIELD = {'nullable': False, 'reader': "str(x).upper()", 'validator': "re.match('^[ACTGN-]*$', x) is not None"}
SAMPLE_FIELD = {'nullable': True}
PROTEIN_FIELD = {'nullable': False}
GDNA_FIELD = {'nullable': False}

# Input file formats definitions
SCHEMAS = {
    ct.VCF_FORMAT: {
        'fields': {
            '#CHROM': CHROMOSOME_FIELD,
            'POS': POSITION_FIELD,
            'REF': REF_FIELD,
            'ALT': ALT_FIELD
        },
        'skip_empty': True
    },

    ct.PROT_FORMAT: {
        'fields': {},
        'skip_empty': True
    },

    ct.GDNA_FORMAT: {
        'fields': {
            'protein': PROTEIN_FIELD,
            'sample': SAMPLE_FIELD
        },
        'skip_empty': True
    },

    ct.FREE_FORMAT: {
        'fields': {
            'chr': CHROMOSOME_FIELD,
            'CHR': CHROMOSOME_FIELD,
            'pos': POSITION_FIELD,
            'POS': POSITION_FIELD,
            'ref': REF_FIELD,
            'REF': REF_FIELD,
            'alt': ALT_FIELD,
            'ALT': ALT_FIELD,
            'sample': SAMPLE_FIELD,
            'SAMPLE': SAMPLE_FIELD,
            'strand': STRAND_FIELD,
            'STRAND': STRAND_FIELD
        },
        'skip_empty': True
    }
}


def replicate_input_file(config: dict):
    """
    Creates a copy of the input file in the local directory with minor generic edits

    :param config:
    :return:
    """

    with itab.reader(config['source_fp'], schema=SCHEMAS[config['input_format']], commentchar='##') as reader, \
            open(config['input_fp'], 'wt') as fd_out, \
            open(os.path.join(config['tmp_folder'], ct.MALFORMED_INPUT), 'wt') as fd_discarted:

        # Output writer
        writer = csv.writer(fd_out, delimiter='\t')
        writer_discarted = csv.writer(fd_discarted, delimiter='\t')
        headers = reader.headers

        # Convert VCF header to uppercase
        if config['input_format'] == ct.VCF_FORMAT:
            headers = [h.upper() for h in headers]
        else:
            headers = [h.lower() for h in headers]

        # Add an internal id column at the end
        headers += [ct.INTERNAL_ID]

        # Write the headers + an internal id column
        writer.writerow(headers)
        writer_discarted.writerow(headers + ['errors'])

        all_errors = []
        rows_total = 0
        rows_valid = 0
        for row, errors in reader:
            rows_total += 1
            if len(errors) > 0:
                all_errors.append(errors)
                writer_discarted.writerow(row + [reader.line_num, '{}'.format(', '.join(errors))])
            else:
                rows_valid += 1
                writer.writerow(row + [reader.line_num])

    if len(all_errors) > 0:
        logging.debug("There are {} input format errors".format(len(all_errors)))
        logging.debug("Showing only the ten first:" if len(errors) > 10 else "They are:")
        for e in all_errors[:10]:
            logging.debug(e)
    else:
        os.remove(os.path.join(config['tmp_folder'], ct.MALFORMED_INPUT))

        if rows_valid < (rows_total * 0.5):
            if rows_valid == 0:
                logging.error("All the entries were discarded due to format errors.")
            else:
                logging.error("{}% were discarded due to format errors. Aborting execution.".format(
                    int((rows_total - rows_valid) * 100 / rows_total)))
            sys.exit(-1)

        logging.debug('Original file copied to {0} with generic minor edits'.format(config['input_fp']))

    return config


'''
All the following functions are for changing the original input file to a format accepted by TransVar
'''


def reformat4transvar_vcf(config: dict):
    vcf_fp = config['input_fp']
    reformated_vcf_fp = config['transvar_dna_input_fp']

    vcf_df = pd.read_csv(vcf_fp, sep='\t')

    for m in ['#CHROM', 'POS', 'ID', 'REF', 'ALT']:
        if m not in vcf_df.columns:
            logging.error(
                'The vcf file does not contain the mandatory field {0}. Some format error in the mutation file?'.format(
                    m))
            sys.exit(-1)

    # output
    vcf_df.to_csv(reformated_vcf_fp, sep='\t', index=False)
    logging.debug(
        'Temporal file with {0} entries with the input for "transvar ganno vcf" created: {1}'.format(len(vcf_df),
                                                                                                     reformated_vcf_fp))

    return config


def reformat4transvar_free(config):

    def construct_gdna(row):

        chrom, pos, ref, alt = row[ct.CHR], row[ct.POS], row[ct.REF], row[ct.ALT]

        # remember that transvar is happy with and without the 'chr' prefix
        pos = int(str(pos).replace('.0', ''))
        if alt == '-':
            # deletion
            gdna = str(chrom) + ':g.' + str(pos) + '_' + str(pos + len(ref) - 1) + 'del'
        elif ref == '-':
            # insertion
            gdna = str(chrom) + ':g.' + str(pos) + '_' + str(pos + 1) + 'ins' + alt
        elif len(ref) != len(alt):
            # deletion and insertion
            #  or deletion/insertion without the '-', i.e. 17 1000 A ACCT -> chr10:g.1000_1000delinsACCT
            gdna = str(chrom) + ':g.' + str(pos) + '_' + str(pos + len(ref) - 1) + 'delins' + alt
        else:
            # point mutation or complex mutation (AA>CT)
            gdna = str(chrom) + ':g.' + str(pos) + ref + '>' + alt

        return gdna

    free_fp = config['input_fp']
    reformated_free_fp = config['transvar_dna_input_fp']

    free_df = pd.read_csv(free_fp, sep='\t')

    # just take the columns of interest and write them in the order is going to be expected later on by transvar
    for e in [ct.CHR, ct.POS, ct.REF, ct.ALT]:
        if e not in free_df.columns:
            logging.error('The file {0} has not the expected column named {1}'.format(free_fp, e))
            sys.exit(-1)

    if ct.STRAND in free_df.columns:
        logging.warning(
            'The ref and alt alleles will be complemented depending on the {0} column content'.format(ct.STRAND))
        free_df.loc[:, ct.REF] = np.where(free_df[ct.STRAND] == '-', free_df[ct.REF].map(lib.complement_seq),
                                          free_df[ct.REF])
        free_df.loc[:, ct.ALT] = np.where(free_df[ct.STRAND] == '-', free_df[ct.ALT].map(lib.complement_seq),
                                          free_df[ct.ALT])
        logging.debug('{0} entries complemented'.format(len(free_df[free_df[ct.STRAND] == '-'])))

    free_df[ct.GDNA] = free_df.apply(construct_gdna, axis=1)

    # output remembering that transvar do not accept header
    free_df.to_csv(reformated_free_fp, columns=[ct.GDNA, ct.INTERNAL_ID], sep='\t', header=False, index=False)

    logging.debug('Temporal file with {0} entries with the input for "transvar ganno" with tab format created: {1}'.
                  format(len(free_df), reformated_free_fp))

    return config


def reformat4transvar_gdna(config):
    gdna_fp = config['input_fp']
    reformated_gdna_fp = config['transvar_dna_input_fp']

    gdna_df = pd.read_csv(gdna_fp, sep='\t')

    # just take the columns of interest and write them in the order is going to be expected later on by transvar
    if ct.GDNA not in gdna_df.columns:
        logging.error('The file {0} as not the expected columns named "{1}"'.format(gdna_fp, ct.GDNA))
        sys.exit(-1)

    # output remembering that transvar do not accept header
    gdna_df.to_csv(reformated_gdna_fp, columns=[ct.GDNA, ct.INTERNAL_ID], sep='\t', header=False, index=False)

    logging.debug('Temporal file with {0} entries with the input for "transvar ganno" created {1}'
                  .format(len(gdna_df), reformated_gdna_fp))

    return config


def reformat4transvar_prot(config):
    def get_prot_annotation(prot):
        if 'M_' in prot:
            return 'refseq'
        return 'enst'

    prot_fp = config['input_fp']  # the original file copied in the output folder
    reformated_prot_fp = config['transvar_revprot_input']  # the input i will create for revprot
    reverse_prot_converted_fp = config['transvar_revprot_output']  # the output of the revprot
    transvar_dna_input_fp = config['transvar_dna_input_fp']  # the output of the revprot formated for the next module

    prot_df = pd.read_csv(prot_fp, sep='\t')

    # (1) reformat the protein annotation file to perform the panno;
    # just take the columns of interest and write them in the order is going to be expected later on by transvar
    if ct.PROT not in prot_df.columns:
        logging.error('The file {0} has not the expected columns named {1}'.format(prot_fp, ct.PROT))
        sys.exit(-1)

    # deduce whether the input annotation is ensembl or refseq
    prot_df['annotation'] = prot_df[ct.PROT].map(get_prot_annotation)

    # separate them
    ensembl_prot_df = prot_df[prot_df['annotation'] != 'refseq']
    refseq_prot_df = prot_df[prot_df['annotation'] == 'refseq']

    reverse_prot_converted_df = pd.DataFrame()
    if len(ensembl_prot_df) > 0:
        # when writing the file, remember that transvar do not accept header
        out_fp = reformated_prot_fp + '_ens'
        ensembl_prot_df.to_csv(out_fp, columns=[ct.PROT, ct.INTERNAL_ID], sep='\t', header=False, index=False)
        logging.debug(
            'Temporal file with {0} entries with the input for "transvar panno" with ensmbl annotation created: {1}'
            .format(len(ensembl_prot_df), out_fp))

        # conversion from protein to dna by transvar
        cmd = " ".join(['transvar panno', '-l', out_fp, '--ensembl', '--seqmax -1'])
        logging.debug('Executing command: {0}'.format(cmd))
        results = subprocess.check_output(cmd, shell=True)

        # keep the results in a dataframe
        # tmp_df = pd.DataFrame.from_csv(StringIO(results.decode("utf-8")), sep="\t", parse_dates=False, index_col=None)
        tmp_df = lib.transvarb2df(results)
        reverse_prot_converted_df = reverse_prot_converted_df.append(tmp_df, ignore_index=True)

    if len(refseq_prot_df) > 0:
        # when output remembering that transvar do not accept header
        out_fp = reformated_prot_fp + '_refseq'
        refseq_prot_df.to_csv(out_fp, columns=[ct.PROT, ct.INTERNAL_ID], sep='\t', header=False, index=False)
        logging.debug(
            'Temporal file with {0} entries with the input for "transvar panno" with refseq annotation created: {1}'
            .format(len(refseq_prot_df), out_fp))

        # conversion from protein to dna by transvar
        cmd = " ".join(['transvar panno', '-l', out_fp, '--refseq', '--seqmax -1'])
        logging.debug('Executing command: {0}'.format(cmd))
        try:
            results = subprocess.check_output(cmd, shell=True)
        except Exception:
            logging.error('Some problem occurred when trying to execute command {0}'.format(cmd))
            sys.exit(-1)

        # keep the results in a dataframe
        # tmp_df = pd.DataFrame.from_csv(StringIO(results.decode("utf-8")), sep="\t", parse_dates=False, index_col=None)
        tmp_df = lib.transvarb2df(results)
        reverse_prot_converted_df = reverse_prot_converted_df.append(tmp_df, ignore_index=True)

    # (2) output the results of the panno since i want to keep them before
    # reformating for the ganno part of the next module
    reverse_prot_converted_df.to_csv(reverse_prot_converted_fp, sep='\t', index=False)
    logging.debug('Temporal file with {0} entries containing the output of transvar panno created: {1}'
                  .format(len(reverse_prot_converted_df), reverse_prot_converted_fp))

    # (3) put panno results for being ready to be inputed to the transvar dna part
    # --> note that here the selection of mutations mapped to several transcrips with the same dna nucleotide change
    reverse_prot_converted_df[ct.GDNA] = reverse_prot_converted_df['coordinates(gDNA/cDNA/protein)'].map(
        lib.get_gdna_from_transvar_coordinates)

    # recover the mutation internal id only if it is not a vcf
    reverse_prot_converted_df[ct.INTERNAL_ID] = reverse_prot_converted_df.apply(lambda row: row['input'].split('|')[1],
                                                                                axis=1)

    # keep the non_mapped frameshift in a separate file
    non_mapped_fs_df = reverse_prot_converted_df[
        reverse_prot_converted_df.apply(lambda row: lib.get_non_mapped_fs(row), axis=1)]
    if len(non_mapped_fs_df) > 0:
        reverse_prot_converted_df = reverse_prot_converted_df[
            np.invert(reverse_prot_converted_df.index.isin(non_mapped_fs_df.index))]
        non_mapped_fs_fp = os.path.join(config['tmp_folder'], ct.FS_NOT_MAPPED)
        non_mapped_fs_df.to_csv(non_mapped_fs_fp, sep='\t', index=False)
        logging.debug('File with the non mapped frameshift mutations created {0}'.format(non_mapped_fs_fp))
        config['recoverable_fs'] = len(non_mapped_fs_df['input'].unique())

    # put the non mapped ones in a separate file
    if len(reverse_prot_converted_df) > 0:
        non_mapped_prot_muts_df = reverse_prot_converted_df[
            reverse_prot_converted_df.apply(lambda row: lib.incorrect_transvar_map(row[ct.GDNA],
                                                                                   row['info']), axis=1)]
        if len(non_mapped_prot_muts_df) > 0:

            # keep the correctly mapped ones for inputing to the next module
            reverse_prot_converted_df = reverse_prot_converted_df[
                np.invert(reverse_prot_converted_df.index.isin(non_mapped_prot_muts_df.index))]

            # output only those entries that are not in the input (since one input is mapped to several transcripts, and
            # if one of these are incorrect but the other are corrects, better not to report it)
            non_mapped_prot_muts_df = non_mapped_prot_muts_df[np.invert(non_mapped_prot_muts_df[ct.INTERNAL_ID].isin(
                reverse_prot_converted_df[ct.INTERNAL_ID]))]

            if len(non_mapped_prot_muts_df) > 0:
                non_mapped_prot_muts_fp = os.path.join(config['tmp_folder'], ct.PANNO_NOT_MAPPED)
                non_mapped_prot_muts_df.to_csv(non_mapped_prot_muts_fp, sep='\t', index=False)
                logging.debug('File with the non mapped protein mutations created {0}'.format(non_mapped_prot_muts_fp))

            eoi = len(non_mapped_prot_muts_df.drop_duplicates([ct.INTERNAL_ID]))

            if eoi > 0:
                if eoi > (len(reverse_prot_converted_df.drop_duplicates(ct.INTERNAL_ID)) * ct.MAX_NONMAPPED_RATIO) + \
                        config['recoverable_fs']:
                    logging.error('There are more than {0}% of the entries that can not be mapped'.format(
                        int(ct.MAX_NONMAPPED_RATIO * 100)))
                    sys.exit(-1)
                logging.warning(
                    'There are {0} protein mutations that have been not able to be mapped to DNA'.format(eoi))

    # keep only one gDNA position per protein mutation (the reverse mapping gives the info for all the transcripts)
    li = len(reverse_prot_converted_df)
    reverse_prot_converted_df = reverse_prot_converted_df.drop_duplicates(subset=[ct.INTERNAL_ID, ct.GDNA])
    lo = len(reverse_prot_converted_df)
    if lo < li:
        logging.debug('There are {0} identical gDNA change per protein mutation in the reverse mapping'.format(li - lo))

    # output a file containing just the gDNA to be used for ganno command in the next module
    reverse_prot_converted_df.to_csv(transvar_dna_input_fp, columns=[ct.GDNA, ct.INTERNAL_ID], sep='\t', index=False,
                                     header=False)

    logging.debug('Temporal file with {0} entries for "tansvar ganno" created: {1}'
                  .format(len(reverse_prot_converted_df), transvar_dna_input_fp))

    return config


def detect_original_format(original_fp):
    """
    The detection of the format of the original input file; based on the header of the file

    :param original_fp: Input file path
    :return: The format type
    """

    with open_file(original_fp, commentchar="##") as fd:
        header = fd.readline().lower()

        if "#chrom" in header:
            return ct.VCF_FORMAT

        if ct.CHR in header:
            return ct.FREE_FORMAT

        if ct.GDNA in header:
            return ct.GDNA_FORMAT

        if ct.PROT in header:
            return ct.PROT_FORMAT

    logging.error('Format of the input file not recognized {0}'.format(original_fp))
    sys.exit(-1)


def run(config: dict):
    logging.info('Processing the mutations input file')

    try:
        # detect original format and insert the tumor offspring always when starting the run,
        # since i need to use it for the rest of the pipeline
        config['input_format'] = detect_original_format(config['source_fp'])
    except Exception:
        logging.error("Impossible to detect the input format")
        sys.exit(-1)

    logging.info('The detected format is {0}'.format(config['input_format']))
    try:
        config['tumor_offspring'] = lib.get_offspring_tumors(config['cancer_types'], config['tumor_type'])
    except Exception:
        logging.warning(
            'The tumor type {0} is not recognized. Generic cancer analysis will be run'.format(config['tumor_type']))
        config['tumor_type'] = ct.PANCANCER
        config['tumor_offspring'] = [ct.PANCANCER]
    logging.debug('The sample tumor is {0} and the offspring is {1}'.format(config['tumor_type'],
                                                                            ','.join(config['tumor_offspring'])))

    # retrieve the paths of the outputs of the module
    copy_fp = os.path.join(config['output_folder'], ct.INPUT_MUTS)
    out_fp = os.path.join(config['tmp_folder'], ct.TRANSVAR_DNA_INPUT)
    config['input_fp'] = copy_fp
    config['transvar_dna_input_fp'] = out_fp

    if config['input_format'] == ct.PROT_FORMAT:
        config['transvar_revprot_input'] = os.path.join(config['tmp_folder'], ct.TRANSVAR_REVPROT_INPUT)
        config['transvar_revprot_output'] = os.path.join(config['tmp_folder'], ct.TRANSVAR_REVPROT_OUTPUT)

    # assess if i need to run this stage by checking whether the *final* outputed file already exists
    if not config['force_output'] and os.path.isfile(out_fp):
        logging.debug('Stage skipped: file {0} already exists'.format(out_fp))
        return config

    # first, it copies the input file as it is
    config = replicate_input_file(config)

    # then create the input for transvar ganno, which is the next module
    if config['input_format'] == ct.VCF_FORMAT:
        config = reformat4transvar_vcf(config)

    elif config['input_format'] == ct.GDNA_FORMAT:
        config = reformat4transvar_gdna(config)

    elif config['input_format'] == ct.FREE_FORMAT:
        config = reformat4transvar_free(config)

    elif config['input_format'] == ct.PROT_FORMAT:
        config = reformat4transvar_prot(config)

    else:
        logging.error('No format recognized')
        sys.exit(-1)

    return config
