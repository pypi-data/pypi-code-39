import csv
import logging
import re
from collections import defaultdict

TRANSVAR_TO_INTOGEN_CONSEQUENCE_MAP = {
    "InFrameInsertion": "inframe_insertion",
    "InFrameDeletion": "inframe_deletion",
    "SpliceDonorSNV": "splice_donor_variant",
    "SpliceDonorDeletion": "splice_donor_variant",
    "SpliceDonorBlockSubstitution": "splice_donor_variant",
    "SpliceDonorInsertion": "splice_donor_variant",
    "SpliceAcceptorSNV": "splice_acceptor_variant",
    "SpliceAcceptorDeletion": "splice_acceptor_variant",
    "SpliceAcceptorBlockSubstitution": "splice_acceptor_variant",
    "SpliceAcceptorInsertion": "splice_acceptor_variant",
    "Nonsense": "stop_gained",
    "CdsStopLoss": "stop_lost",
    "Frameshift": "frameshift_variant",
    "Missense": "missense_variant",
    "Synonymous": "synonymous_variant",
    "IntronicSNV": "intron_variant",
    "MultiAAMissense": "missense_variant"
}


def load_alterations(alterations_files: list):
    alterations = defaultdict(list)
    for alterations_file in alterations_files:
        with open(alterations_file, 'rt') as fd:
            rows = csv.DictReader((line for line in fd if not line.startswith('#')), delimiter='\t')

            parse_errors = []
            for idx, row in enumerate(rows, start=1):

                if 'alt_type' not in row:
                    if 'fus' in row:
                        row['alt_type'] = "FUS"
                    elif 'cna' in row:
                        row['alt_type'] = "CNA"
                    else:
                        row['alt_type'] = "MUT"

                try:
                    alteration = parse_alteration(row)
                except Exception as e:
                    parse_errors.append("  At row {}: '{}' ({})".format(idx, row, e))
                    continue

                alterations[(alteration.sample, alteration.cancer_type)].append(alteration)

            if len(parse_errors) > 0:
                logging.error(
                    "There are {} input alteration parsing errors at {}. ".format(len(parse_errors), alterations_file) +
                    ("Showing ten first errors: " if len(parse_errors) > 10 else ""))
                for error in parse_errors[:10]:
                    logging.error(error)

    return alterations


def parse_alteration(row):
    sample = row['sample']
    cancer_type = row['cancer']
    mark_type = row['alt_type']
    oncogenic = row['driver_statement']
    gene = row['gene'] if 'gene' in row else None

    if 'consequence' in row:
        try:
            consequence = TRANSVAR_TO_INTOGEN_CONSEQUENCE_MAP[row['consequence']]
        except KeyError:
            logging.debug("Unknown consequence type '{}'".format(row['consequence']))
            consequence = row['consequence']
    else:
        consequence = None

    if mark_type == 'MUT':
        try:
            pos = int(row['protein_pos'])
            if '/' in row['protein_change']:
                aa_change = row['protein_change'].split('/')
                alteration = "{}{}{}".format(aa_change[0], pos, aa_change[1])
            else:
                alteration = "?{}?".format(pos)
        except Exception:
            if re.search('-', row['protein_pos']):  # Protein pos is a range
                alteration = "{}".format(row['protein_pos'])
            else:
                if row['protein_pos'] != '.':
                    logging.error("Invalid 'protein_pos' value: {}".format(row['protein_pos']))
                alteration = ""

    elif mark_type == "CNA":
        alteration = "{}:{}".format(gene.upper(), row['cna'].lower())

    elif mark_type == "FUS":
        effector_gene = row['effector_gene']
        gene = [effector_gene] + [g.strip() for g in row['fus'].split("__") if g.strip() != effector_gene]
        alteration = "__".join(gene)

    else:
        alteration = ""

    alteration_str = row['protein'].replace('p.', '') if row.get('protein', None) is not None else alteration

    return Alteration(sample, cancer_type, gene, mark_type, alteration, alteration_str, consequence, oncogenic, row)


class Alteration(object):

    def __init__(self, sample, cancer_type, gene, mark_type, alteration, alteration_str, consequence, oncogenic, row):
        self.sample = sample
        self.cancer_type = cancer_type
        self.gene = gene if type(gene) == list else [gene]
        self.mark_type = mark_type
        self.alteration = alteration
        self.alteration_str = alteration_str
        self.consequence = consequence
        self.oncogenic = oncogenic.lower()
        self.perfect_match = False
        self.biomarker_tumors = set()
        self.driver = "known" in self.oncogenic or "predicted driver" in self.oncogenic
        self.pam_no_polymorphism = "known" in self.oncogenic or \
                                   "predicted driver" in self.oncogenic or \
                                   "predicted passenger" in self.oncogenic
        self.row = row

    def __str__(self):

        if self.mark_type == "FUS":
            return "{} {}".format(self.alteration_str, self.mark_type)

        if self.mark_type == "CNA":
            return "{} {}".format(self.alteration, self.mark_type)

        passanger = '' if self.driver else '*'
        if self.alteration == '':
            return "{} {}{} ({})".format('+'.join(self.gene), self.mark_type, passanger, self.consequence)

        return "{} {}{} ({})".format('+'.join(self.gene), self.mark_type, passanger, self.alteration_str)

    def __repr__(self):
        return self.__str__()
