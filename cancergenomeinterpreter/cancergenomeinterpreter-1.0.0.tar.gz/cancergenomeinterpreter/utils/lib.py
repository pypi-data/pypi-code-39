import csv
import logging
import os
import shutil
import sys

import pandas as pd
import cancergenomeinterpreter.utils.constants as ct


def concat_files(input_files, output_file, delimiter='\t'):
    with open(input_files[0], 'rt') as fd:
        all_headers = list(next(csv.reader(fd, delimiter=delimiter)))

    for f in input_files[1:]:
        with open(f, 'rt') as fd:
            header = next(csv.reader(fd, delimiter=delimiter))
            for h in header:
                if h not in all_headers:
                    all_headers.append(h)

    with open(output_file, 'wt') as fd_out:
        writer = csv.DictWriter(fd_out, fieldnames=all_headers, delimiter=delimiter)
        writer.writeheader()
        for f in input_files:
            with open(f, 'rt') as fd_in:
                for i, row in enumerate(csv.DictReader(fd_in, delimiter=delimiter), start=2):
                    try:
                        writer.writerow(row)
                    except ValueError:
                        logging.warning("At {} line {} there are unknown columns".format(f, i))


def create_folder(folder):
    """
    Check if a folder exists and create it if necessary.

    :param folder: Folder path
    :return: Folder absolute path
    """
    try:
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)
    except OSError:
        if not os.path.exists(folder):
            logging.error('Error when trying to create folder {0}'.format(folder))
            sys.exit(-1)

    return os.path.abspath(folder)


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


def copy_input_file(config: dict, internal_id: str):
    """
    Creates a copy of the input file in the local directory as it is

    :param internal_id:
    :param config:
    :return:
    """

    df = pd.read_csv(config['source_fp'], sep='\t')

    # add the internal id unless it is a CNA-matrix format
    if config['input_format'] != ct.CNA_MAT_FORMAT:
        df[internal_id] = df.index

    # output
    df.to_csv(config['input_fp'], sep='\t', index=False)
    logging.debug('Original file copied to {0} with an internal id inserted'.format(config['input_fp']))

    return config


def load_configuration():
    # FIXME Don't hardcode this configuration
    return {
        "cancer_types": "/data/cgi/cancertypes/cancer_types.tsv",
        "cna_drivers_fp": "/data/cgi/oncodrivemut/cna_drivers.tsv",
        "fus_drivers_fp": "/data/cgi/oncodrivemut/fus_drivers.tsv",
        "oncodrivemut_package": "/data/cgi/oncodrivemut",
        "gene_role_fp": "/data/cgi/oncodrivemut/gene_role.tsv.gz",
        "chosen_transcripts_fp": "/data/cgi/oncodrivemut/selected_transcripts_ensembl70.tsv.gz",
        "clusters_fp": "/data/cgi/oncodrivemut/oncodriveclust_coordinates.tsv.gz",
        "drivers_fp": "/data/cgi/oncodrivemut/drivers_per_tumor.tsv.gz",
        "known_oncogenic_fp": "/data/cgi/oncodrivemut/known_oncomutations.tsv.gz",
        "known_neutral_fp": "/data/cgi/oncodrivemut/known_neutral.tsv.gz",
        "known_predisposing_fp": "/data/cgi/oncodrivemut/known_predisposing.tsv.gz",
        "polym_fp": "/data/cgi/oncodrivemut/exac_03_polym.tsv.gz",
        "pfam_fp": "/data/cgi/oncodrivemut/ensembl75_pfam_domain_coordinates.tsv.gz",
        "delicate_domains_fp": "/data/cgi/oncodrivemut/delicate_regions.tsv.gz",
        "transcript_metrics_fp": "/data/cgi/oncodrivemut/ensembl70_transcript_metrics.tsv.gz",
        "fi_scores": "/data/cadd/cadd.tsv.bgz" if os.path.exists("/data/cadd/cadd.tsv.bgz") else "/data/bgscore/bgscore.tsv.bgz",
        "stop_file": "/data/cgi/oncodrivemut/frameshift_indel_scores_cadd_1.3.pickle",
        "gene_coordinates": "/data/cgi/oncodrivemut/hg19_ensembl_70_annotations.tree",
        "genomeref": "/data/transvar/Homo_sapiens.GRCh37.70.fa"
    }


def difference_lists(l_l):
    l_diff = list(set(l_l[0]) - set(l_l[1]))

    return l_diff
