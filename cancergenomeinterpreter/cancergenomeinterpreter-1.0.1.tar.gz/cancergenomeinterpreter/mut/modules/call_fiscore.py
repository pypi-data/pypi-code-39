import csv
import gzip
import logging
import os
import subprocess
import sys
import pickle
import tabix

import pandas as pd

import cancergenomeinterpreter.mut.modules.lib as lib
import cancergenomeinterpreter.mut.utils.constants as ct


# Global variables
gene_trees = None


def run(config: dict):
    """
    Retrive Functional Impact scores

    :param config: The configuration dictionary
    :return: The configuration dictionary
    """
    logging.info('Retrieving functional impact scores')

    # retrieve the paths of the outputs of the module
    output_fp = os.path.join(config['tmp_folder'], ct.FISCORE_OUTPUT)
    config['fiscore_input_fp'] = os.path.join(config['tmp_folder'], ct.FISCORE_INPUT)
    config['fiscore_output_fp'] = output_fp

    # assess if i need to run this stage by checking whether the *final* outputed file already exists
    if not config['force_output'] and os.path.isfile(output_fp):
        logging.debug('Stage skipped: file {0} already exists'.format(output_fp))
        return config

    # if the input format is a vcf, i can pass it directly to fiscore after zipping it
    if config['input_format'] == ct.VCF_FORMAT:
        vcf_df = pd.read_csv(config['input_fp'], sep='\t')

        # if not config['extended']:
        #     size = len(vcf_df)
        #     vcf_df = lib.filter_pams(vcf_df, config)
        #     logging.debug(
        #         '{0} out of {1} entries are not PAM and not considered to retrieve fiscore'.format(
        #             size - len(vcf_df), size)
        #     )

        vcf_df.to_csv(config['fiscore_input_fp'], index=False, sep='\t', compression='gzip')
        logging.debug('Input temp file for fiscore copied and zipped from {0} to {1}'.format(config['input_fp'],
                                                                                          config['fiscore_input_fp']))

    # if not a vcf, i have to create a vcf like file to be inputed to fiscore
    else:
        mutations_df = pd.read_csv(config['annotated_mutations_fp'], sep='\t')

        if not config['extended']:
            size = len(mutations_df)
            mutations_df = mutations_df[mutations_df[ct.CONSEQUENCE_TYPE].isin(ct.PAM_CT)]
            logging.debug(
                '{0} out of {1} entries are not PAM and not considered to retrieve functional impact score'.format(
                    size - len(mutations_df), size
                )
            )

        # need to protect that no mutaions to check fiscore are necessary available
        if mutations_df.empty:
            logging.debug('No mutation to be queried to fiscore')
            return config

        # convert the mutations to a vcf needed for fiscore
        vcf_df = lib.gdna_2_vcf(mutations_df, config)

        # this can be useful if the same mutation lead to two annotation
        # (because it map to two genes, the one in +/- strands)
        vcf_df = vcf_df.drop_duplicates()

        # note that the fiscore requires gzip, or it will run but with errors;
        # note that i output the gdna entry to use it as a key to recover the information
        vcf_df.to_csv(config['fiscore_input_fp'], sep='\t', index=False,
                      columns=[ct.CHR, ct.POS, 'ID', ct.REF, ct.ALT, ct.GDNA], compression='gzip')
        logging.debug('Input temp file for fiscore created {0}'.format(config['fiscore_input_fp']))

    fast_fiscore(config)

    logging.debug('Output tmp file with fiscore scores created {0}'.format(config['fiscore_output_fp']))

    return config


def fast_fiscore(config):
    fiscore_tabix = tabix.open(config['fi_scores'])

    in_file, out_file = config['fiscore_input_fp'], config['fiscore_output_fp']

    with gzip.open(in_file, 'rt') as in_fd, gzip.open(out_file, 'wt') as out_fd:

        writer = csv.writer(out_fd, delimiter='\t')
        writer.writerow(['## Fast fiscore 20160418'])
        writer.writerow(['#CHROM', 'POS', 'REF', 'ALT', 'FISCORE'])

        reader = csv.reader(in_fd, delimiter='\t')
        next(reader)

        todo_rows = []

        for m in reader:
            chrom, pos, ref, alt = m[0], int(m[1]), m[3], m[4]

            if len(ref) == 1 and len(alt) == 1 and ref in "ACTG" and alt in "ACTG":
                try:
                    for r in fiscore_tabix.query(chrom, pos, pos):
                        if r[2] == ref and r[3] == alt:
                            writer.writerow([r[0], r[1], r[2], r[3], r[4].strip()])
                except tabix.TabixError:
                    logging.warning("Tabix error at {}".format(m))
                    todo_rows.append(m)
            else:
                todo_rows.append(m)

        if len(todo_rows) > 0:
            fiscore_indels_fast(todo_rows, config, writer)


def is_frameshift(size):
    """
    Determine whether an indel is frameshift

    :param size: int, length of the indel
    :return: bool, whether the size is multiple of 3
    """
    return False if (size % 3) == 0 else True


def load_from_pickle(pickle_file):
    """
    Load an object saved as pickle

    :param pickle_file: str, file path
    :return: object
    """
    with open(pickle_file, 'rb') as fd:
        obj = pickle.load(fd)
    return obj


def get_ensembl_id(chromosome, position):
    """
    Get the ensembl id of the gene that contain the genomic location

    :param chromosome: str, chromosome
    :param position: int, position
    :return: str, ensembl id
    """
    res = set([])
    for r in gene_trees[chromosome][position]:
        res.add(r.data[-1])
    return res


def get_gene_strand(chromosome, position):
    """
    Get the strand of the gene that contain the genomic location

    :param chromosome: str, chromosome
    :param position: int, position
    :return: str, ensembl id
    """
    res = set([])
    for r in gene_trees[chromosome][position]:
        res.add(r.data[0])
    return res


def fiscore_indels_fast(todo_rows, config, writer):
    """
    Calculate the score of indels

    :param todo_rows: list of rows
    :param config: configuration dictionary
    :param writer: writer object
    :return: None
    """
    global gene_trees

    # Load the pre-calculated stop scores per gene
    stops = load_from_pickle(config['stop_file'])

    # Load the annotations
    gene_trees = load_from_pickle(config['gene_coordinates'])

    fiscore_tabix = tabix.open(config['fi_scores'])

    errors = []
    for row in todo_rows:
        chrom, position, ref, alt = row[0], int(row[1]), row[3], row[4]
        size = max(len(ref), len(alt))

        # Frame-shift
        score = None
        if is_frameshift(size):
            ensembl_id = get_ensembl_id(chrom, position)
            if len(ensembl_id) == 0:
                logging.warning('Could not find any ensembl id for {}:{}'.format(chrom, position))
            else:
                ensembl_id = list(ensembl_id)[0]
                score = stops.get(ensembl_id, None)

        if score is None:
            scores = []
            strand = get_gene_strand(chrom, position)
            if len(strand) == 1:
                strand = list(strand)[0]
            else:
                logging.error('More than one strand for {}:{}'.format(chrom, position))
                logging.warning('Assuming the strand is positive')
                strand = '+'
            if strand == '+':
                positions = range(position, position + size)
            else:
                positions = range(position - size + 1, position + 1)
            for pos in positions:
                try:
                    # r: chromosome, position, ref, alt, score
                    for r in fiscore_tabix.query(chrom, pos, pos):
                        scores.append(float(r[4].strip()))
                except tabix.TabixError:
                    logging.warning("Functional Score tabix error at chromosome {}, position {}".format(chrom, pos))
                    errors.append((chrom, pos))
            score = max(scores) if len(scores) > 0 else None

        # Write to the output file
        score = float('nan') if score is None else score
        writer.writerow([chrom, position, ref, alt, score])