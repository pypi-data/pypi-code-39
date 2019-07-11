import csv
import gzip
import logging
import os
from collections import defaultdict

from cancergenomeinterpreter.prescription.entities.alteration import Alteration
from cancergenomeinterpreter.prescription.entities.genemarks import MATCH_LEVEL_NONE, MATCH_LEVEL_COMPLETE, MATCH_LEVEL_GENE


class Bioactivity(object):

    def __init__(self, idx, row):
        self.idx = idx

        self.gene = row['SYMBOL']
        self.moa_parent = row['MOA_PARENT'].lower()
        self.row = row

    def match_alteration(self, observed_alterations):
        """
        Check if all this biomarker match the observed alterations at some level

        :param observed_alterations: List of the observed alterations
        :return: match_level, matched_alterations. The match level and the list of observed alterations that match.

        :type observed_alterations: list[Alteration]
        :rtype: (bool, list[Alteration])
        """

        match_alterations = [a for a in observed_alterations if a.driver and self.gene in a.gene]

        if len(match_alterations) == 0:
            return MATCH_LEVEL_NONE, []

        # Check MOA match
        moa_matches = [self.moa_match(a) for a in match_alterations]

        if any(moa_matches):
            return MATCH_LEVEL_COMPLETE, match_alterations

        return MATCH_LEVEL_GENE, match_alterations

    def moa_match(self, a):
        """
        Check if this alteration matches the MOA

        :param a: alteration
        :return: True if MOA matches otherwise False

        :type a: Alteration
        :rtype: bool
        """

        moa = self.moa_parent
        if a.mark_type == "FUS":
            return moa == 'negative'
        elif a.mark_type == "CNA":
            cna = a.row['cna'].lower()
            return (cna == 'amp' and moa == 'negative') or (cna == 'del' and moa == 'positive')
        elif a.mark_type == "MUT":
            role = a.row['gene_role']
            return (role == 'Act' and moa == 'negative') or (role == 'LoF' and moa == 'positive')

        return False

    def __str__(self):
        return "{}".format(self.row)

    def __repr__(self):
        return self.__str__()


def parse_bioactivity(row, idx) -> Bioactivity:
    return Bioactivity(idx, row)


def load_bioactivities(file_path):
    """
        Load, parse and validate a file with bioactivities

        :param file_path: Path to the bioativities file
        :return: A list of bioactivities
        :rtype: list[Bioactivity]
        """

    bioactivities_dict = defaultdict(list)
    openfile = gzip.open if file_path.endswith(".gz") else open
    with openfile(file_path, 'rt') as fd:
        reader = csv.DictReader(fd, delimiter='\t')
        for idx, row in enumerate(reader, start=1):

            try:
                bioactivity = parse_bioactivity(row, idx)
            except Exception as e:
                logging.error(
                    "Malformed bioactivity at '{}' row {}: {}".format(os.path.basename(file_path), idx, e))
                continue

            bioactivities_dict[bioactivity.gene].append(bioactivity)

    return bioactivities_dict
