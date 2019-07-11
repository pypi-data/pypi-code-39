import csv

from cancergenomeinterpreter.prescription.entities.alteration import Alteration
from cancergenomeinterpreter.prescription.entities.genemarks import MATCH_LEVEL_NONE, MutMark, ExprMark, FusMark, CnaMark, BiaMark
from cancergenomeinterpreter.prescription.entities.tumor import Tumor

GENE_MARKS = {
    MutMark.MARK_TYPE: MutMark.parse,
    ExprMark.MARK_TYPE: ExprMark.parse,
    FusMark.MARK_TYPE: FusMark.parse,
    CnaMark.MARK_TYPE: CnaMark.parse,
    BiaMark.MARK_TYPE: BiaMark.parse
}


class Biomarker(object):

    def __init__(self, idx, marks, drugs, tumors, association, row):
        self.idx = idx
        self.marks = marks
        self.drugs = drugs
        self.tumors = tumors
        self.association = association
        self.row = row

    def match_alteration(self, observed_alterations):
        """
        Check if all the marks in this biomarker match the observed alterations at
        some level

        :param observed_alterations: List of the observed alterations
        :return: match_level, matched_alterations. The match level and the list of observed alterations that match.

        :type observed_alterations: list[Alteration]
        :rtype: (bool, list[Alteration])
        """

        match_level = None
        matched_alterations = []
        for mark in self.marks:
            level, m = mark.match(observed_alterations)

            # All the marks must much, otherwise return match none and an empty list.
            if level == MATCH_LEVEL_NONE:
                return MATCH_LEVEL_NONE, []

            # First level
            if match_level is None:
                match_level = level

            # In next iterations, the worst level has predominance
            if level < match_level:
                match_level = level

            # Add matched alterations
            matched_alterations += m

        return match_level, matched_alterations

    def match_tumor(self, tumor_type):
        """
        Check if this tumor is a valid tumor for this biomarker.

        :param tumor_type: The tumor type to check
        :return: True if it's a valid tumor type for this biomarker
        """
        for tumor in self.tumors:
            if tumor.match(tumor_type):
                return True

        return False

    def __str__(self):
        return "{}".format(self.row['Biomarker'])

    def __repr__(self):
        return self.__str__()


class Drug(object):

    def __init__(self, key, family=""):
        self.id = None if "[" in key or "]" in key else key
        self.family = family.replace("[", "").replace("]", "")

    def match(self, other):

        if self.family.find(other.family) == -1:
            return False

        if other.id is None:
            return True

        return self.id == other.id

    def __eq__(self, other):
        return id == other.id

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self):

        key = "" if self.id is None else self.id
        family = "" if self.family is None else self.family

        if family != "" and key != "":
            return "{} ({})".format(key, family)

        if family != "" and key == "":
            return family

        return key


def parse_biomarker(row, idx) -> Biomarker:
    # Parse tumors
    tumors = [Tumor(n) for n in to_list(row['Primary Tumor type'])]

    # Parse drugs
    drugs = [Drug(n, f) for n, f in zip(to_list(row['Drug']), to_list(row['Drug family']))]

    # Parse marks
    marks = [GENE_MARKS[t](g, a) for g, t, a in
             zip(to_list(row['Gene']), to_list(row['Alteration type']), to_list(row['Alteration']))]

    # Biomarker type
    association = row['Association']

    return Biomarker(idx, marks, drugs, tumors, association, row)


def load_biomarkers(file_path):
    """
    Load, parse and validate a file with biomarkers

    :param file_path: Path to the biomarkers file
    :return: A list of biomarkers
    :rtype: list[Biomarker]
    """

    biomarkers = []
    with open(file_path, 'rt') as fd:
        reader = csv.DictReader(fd, delimiter='\t')
        for idx, row in enumerate(reader, start=1):

            #try:
            biomarker = parse_biomarker(row, idx)
            #except Exception as e:
            #    logging.error("Malformed biomarker at '{}' row {}: {}".format(os.path.basename(file_path), idx, e))
            #    continue

            biomarkers.append(biomarker)

    return biomarkers


def to_list(value, sep=';', null_value='.'):
    if value is None:
        return None

    values = []
    for v in value.split(sep):
        if v == null_value:
            values.append(None)
        else:
            values.append(v.strip())

    return values