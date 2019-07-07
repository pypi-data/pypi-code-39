from Bio.Seq import Seq
import random
from Bio.Alphabet.IUPAC import IUPACUnambiguousDNA
from Bio.SeqFeature import FeatureLocation, CompoundLocation


def random_sequence(size, alphabet, seqclass=Seq):
    letters = [random.choice(alphabet.letters) for _ in range(size)]
    return seqclass("".join(letters))


def random_dna(size, seqclass=Seq):
    return random_sequence(size, IUPACUnambiguousDNA, seqclass)


def topology(record):
    return record.annotations.get("topology", "linear")


def is_circular(record):
    return topology(record).strip().lower() == "circular"


def make_location_parts(start, end, length, strand):
    if start > end:
        if length is None:
            raise ValueError(
                "A length must be provided to create a feature with start > end."
            )
        f1 = FeatureLocation(start, length, strand)
        f2 = FeatureLocation(1, end, strand)
        if strand == -1:
            parts = [f2, f1]
        else:
            parts = [f1, f2]
    else:
        parts = [FeatureLocation(start, end, strand=strand)]
    return parts


def make_circular_location(start, end, length, strand):
    """
    Make a location. If spans origin, a CompoundLocation is created.

    :param start: inclusive start position
    :type start: int
    :param end: exclusive end position
    :type end: int
    :param length: length of the sequence
    :type length: int
    :param strand: strand (1 or -2)
    :type strand: int
    :return:
    :rtype:
    """
    parts = make_location_parts(start, end, length, strand)
    if len(parts) > 1:
        return CompoundLocation(parts)
    else:
        return parts[0]
