import logging
import os
import re
import sys

import pandas as pd

import cancergenomeinterpreter.mut.utils.constants as ct
from cancergenomeinterpreter.mut.utils.faidx import get_seq
from cancergenomeinterpreter.prescription.entities.tumor import Tumor


def create_folder(folder):
    """
    Check if a folder exists and create it if necessary.

    :param folder: Folder path
    :return: Folder absolute path
    """
    try:
        if not os.path.exists(folder):
            os.makedirs(folder)
    except OSError:
        if not os.path.exists(folder):
            logging.error('Error when trying to create folder {0}'.format(folder))
            sys.exit(-1)

    return os.path.abspath(folder)


def difference_lists(l_l):
    """
    Return the difference of two lists as a new list.

    :param l_l: A tuple/list with two lists
    :return: A list with the elements that are not in both lists
    """
    if len(l_l) > 2:
        logging.error('Difference lists function can accept only two lists as input!')
        sys.exit(-1)
    s_out = set(l_l[0]).difference(set(l_l[1]))

    return list(s_out)


def intersect_lists(l_l):
    l_intersect = list(set(l_l.pop()) & set(l_l.pop()))
    for l in l_l:
        l_intersect = list(set(l_intersect) & set(l))

    return l_intersect


def get_non_mapped_fs(row):
    """
    those entries without the fs length
    """
    if 'CSQN=Frameshift;imprecise' in row['info']:
        return True

    return False


def incorrect_transvar_map(gdna_entry, info_entry):
    """
    To detect if the rev prot step (panno command) found a correct dna mutation

    :param gdna_entry:
    :param info_entry:
    :return:
    """
    '''
    # if it s a protein input and the fs has the length not stated, i accept it
    if config['input_format'] == ct.PROT_FORMAT and 'CSQN=Frameshift;imprecise' in info_entry:
        return False
    '''

    # gene symbol invalid, etc
    if gdna_entry == '.':
        return True

    if '(' in gdna_entry:
        return True

    # either bad format or format fine but i am not able to perform a rev mapping
    for tag in ct.INVALID_TRANSVAR_MAP_TAGS:
        if tag in info_entry:
            return True

    return False


def get_gdna_from_transvar_coordinates(coordinates_entry):
    return coordinates_entry.split('/')[0]


def split_transvar_coordinates(coordinates_entry, labels=[ct.GDNA, ct.CDNA, ct.PROT]):
    coordinates_entry_s = coordinates_entry.split('/')
    gdna, cdna, prot = coordinates_entry_s[0], coordinates_entry_s[1], coordinates_entry_s[2]

    return pd.Series({labels[0]: gdna, labels[1]: cdna, labels[2]: prot})


def retrieve_prot_entries(protein_change_entry):
    # no protein entry (e.g. intronic, splice, etc), so no protein info can be retrieved
    if protein_change_entry == '.':
        return pd.Series({ct.AA_POS: '.', ct.AA_CHANGE: './.'})
    # it s a unexpected protein change statement (as p.(=) that does not contain the info of interest;
    # this cond can collapse with the one of above
    if len(re.findall("\d", protein_change_entry)) == 0:
        logging.debug('Can not decompose protein change {0}'.format(protein_change_entry))
        return pd.Series({ct.AA_POS: '.', ct.AA_CHANGE: './.'})

    # a frameshift
    elif 'fs' in protein_change_entry:
        pos = int(''.join(re.findall("\d", protein_change_entry.split('fs')[0])))
        aa_ref = protein_change_entry[2]
        return pd.Series({ct.AA_POS: pos, ct.AA_CHANGE: aa_ref + '/.'})

    # if not, it is an inframe indel, block substitution or a missense
    # note that i return only the start as a position, in case there is an interval
    pos = ''.join(re.findall("\d", protein_change_entry.split('_')[0])) if '_' in protein_change_entry else \
        ''.join(re.findall("\d", protein_change_entry))

    if 'del' in protein_change_entry:
        aa_ref, aa_alt = protein_change_entry.split('del')[1], '-'

    elif 'ins' in protein_change_entry:
        aa_ref, aa_alt = '-', protein_change_entry.split('ins')[1]

    elif 'dup' in protein_change_entry:
        aa_ref, aa_alt = '-', protein_change_entry.split('dup')[1]

    else:
        tmp_s = protein_change_entry.replace('p.', '').split(pos)
        aa_ref, aa_alt = tmp_s[0], tmp_s[1]

    return pd.Series({ct.AA_POS: pos, ct.AA_CHANGE: aa_ref + '/' + aa_alt})


def decompose_point_mut_gdna(gdna):
    gdna_s = gdna.split(':')
    chrom = gdna_s[0][3:]
    pos = ''.join(re.findall("\d", gdna_s[1]))
    chg_s = gdna_s[1][len(pos) + 2:]
    try:
        ref, alt = chg_s.split('>')
    except Exception:
        # probably means is a non mapped fs
        ref, alt = '', ''
    return pd.Series({ct.CHR: chrom, ct.POS: pos, ct.REF: ref, ct.ALT: alt})


def decompose_indel_gdna(gdna):
    # gdna = 'chr7:g.140453121_140453127delCTCCATCinsAA'
    gdna_s = gdna.split(':')
    chrom = gdna_s[0][3:]
    pos = int(''.join(re.findall("\d", gdna_s[1].split('_')[0])))

    # chr7:g.140453121_140453127delinsAA -> 7 140453120 ACTCCATC AAA
    # chr7:g.140453121_140453127delinsA -> 7 140453120 ACTCCATC AA
    # chr11:g.32417908delinsACCGTACA -> 11 32417907 GC	GGCCGTACA
    if 'delins' in gdna:
        pos = pos - 1
        if '_' in gdna:
            pos2 = int(''.join(re.findall("\d", gdna_s[1].split('_')[1])))
        else:
            pos2 = pos + 1
        ref = get_seq(chrom, pos, pos2)
        alt = ref[0] + gdna_s[1].split('ins')[1]

    # i do not know if this can actually happen even with the --refseq -1
    # chr11:g.32417908delCinsACCGTACA -> 11 32417907 GC	GGCCGTACA
    # chr7:g.140453121_140453127delCTCCATCinsAA -> 7 140453120 ACTCCATC AAA
    elif 'del' in gdna and 'ins' in gdna:
        pos = pos - 1
        ref = get_seq(chrom, pos, pos)
        ref = ref + gdna_s[1].split('del')[1].split('ins')[0]
        alt = ref[0] + gdna_s[1].split('ins')[1]

    # chr2:g.234183368_234183375delACTCATCC --> 2 234183367 . TACTCATCC T
    # chr2:g.234183368_234183375del8 --> 2 234183367 . TACTCATCC T
    # chr2:g.234183368_234183375del --> 2 234183367 . TACTCATCC T
    # chr2:g.234183368delA --> 234183367 TA T
    elif 'del' in gdna:
        pos = pos - 1
        pos2 = int(''.join(re.findall("\d", gdna_s[1].split('_')[1]))) if '_' in gdna_s[1] else pos + 1
        ref = get_seq(chrom, pos, pos2)
        alt = ref[0]

    # chr3:g.178936091_178936092insGATCC ->  3 178936091  G GAGAAT
    elif 'ins' in gdna:
        ref = get_seq(chrom, pos, pos)
        alt = ref + gdna_s[1].split('ins')[1]

    # chr3:g.178936090_178936091dupTG = 178936090 TG TGTG
    elif 'dup' in gdna:
        ref = gdna_s[1].split('dup')[1]
        alt = ref + ref

    # left alignement -> so 3 1000 AGT AGTCC  is 3 1002 T TCC
    #                       3 1000 AG ATT  is 3 1001 G TT
    if len(ref) > 1:
        try:
            while ref[0] == alt[0] and len(ref) > 1 and len(alt) > 1:
                ref = ref[1:]
                alt = alt[1:]
                pos += 1
        except IndexError:
            pass

    return pd.Series({ct.CHR: chrom, ct.POS: pos, ct.REF: ref, ct.ALT: alt})


def gdna_2_vcf(mutation_df: pd.DataFrame, run_info_d: dict):
    """
    This is used to transform a gdna to a vcf format (required for fiscore input)

    :param mutation_df:
    :param run_info_d:
    :return: VCF dataframe
    """

    def decompose_gdna(gdna, run_info_d):

        if 'del' in gdna or 'ins' in gdna or 'dup' in gdna:
            return decompose_indel_gdna(gdna)

        else:
            return decompose_point_mut_gdna(gdna)

    mutation_df = mutation_df.merge(mutation_df.apply(lambda row: decompose_gdna(row[ct.GDNA], run_info_d), axis=1),
                                    left_index=True, right_index=True)
    mutation_df['ID'] = '.'
    vcf_df = mutation_df[[ct.CHR, ct.POS, 'ID', ct.REF, ct.ALT, ct.GDNA]]

    return vcf_df


def filter_pams(vcf_df, config):
    """
    This function filter out mutations that are not PAM from a vcf file given the mutation_id of the annotated file
    """
    annotated_df = pd.read_csv(config['annotated_mutations_fp'], sep='\t')
    ids_to_keep = annotated_df[annotated_df[ct.CONSEQUENCE_TYPE].isin(ct.PAM_CT)][ct.INTERNAL_ID]
    vcf_df = vcf_df[vcf_df[ct.INTERNAL_ID].isin(ids_to_keep)]

    return vcf_df


def get_offspring_tumors(cancer_types_fp, tumor_type):
    """
    here i retrieve the offspring of the tumor type under analysis
    """
    Tumor.load_family(cancer_types_fp)
    tumor_family = [tumor_type] + Tumor(tumor_type).get_offspring()

    return list(set(tumor_family))


def complement_seq(seq: str):
    """
    returns the complementary DNA sequence
    """
    comp_d = {'N': 'N', '-': '-', 'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    try:
        return ''.join([comp_d[e] for e in seq])
    except Exception:
        logging.debug('{0} can not be complemented'.format(seq))
        return seq


def transvarb2df(results):
    """
    convert a byte file with the results of transvar and put it in a dataframe after
    trimming potential extra (inconsistent) rows
    """
    results = results.decode('UTF-8').rstrip().split('\n')
    header = results[0].split('\t')
    rows = []
    for l in results[1:]:
        rows.append(l.split('\t')[0:len(header)])

    return pd.DataFrame(data=rows, columns=header)


def get_prot_pos(e):
    """
    get the position of a protein entry
    """
    try:
        p = int(''.join(re.findall("\d", e)))
    except Exception:
        p = e
    return p


def match_protein_pos(e1, e2):
    """
    whether two protein entries have the same position (if it s indel like, the match is for the indel start)
    """

    def ref_e(e):
        if ':' in e:
            e = e.split(':')[1]
        if '_' in e:
            e = e.split('_')[0]
        return e.replace('p.', '')

    e1, e2 = ref_e(e1), ref_e(e2)
    p1, p2 = get_prot_pos(e1), get_prot_pos(e2)
    if p1 == p2:
        return True

    return False
