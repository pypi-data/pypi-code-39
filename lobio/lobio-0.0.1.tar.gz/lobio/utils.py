from itertools import chain
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqFeature import FeatureLocation, CompoundLocation
import tempfile
import random
from Bio.Alphabet.IUPAC import IUPACUnambiguousDNA


def random_sequence(size, alphabet, seqclass=Seq):
    letters = random.choices(alphabet.letters, k=size)
    return seqclass("".join(letters))


def random_dna(size, seqclass=Seq):
    return random_sequence(size, IUPACUnambiguousDNA, seqclass)


def topology(record):
    return record.annotations.get("topology", "linear")


def is_circular(record):
    return topology(record).strip().lower() == "circular"


def load_glob(*paths, format=None):
    path_iter = chain(*paths)
    records = []
    for path in path_iter:
        records += SeqIO.parse(path, format=format)
    return records


def load_fasta_glob(path):
    return load_glob(path, format="fasta")


def load_genbank_glob(path):
    return load_glob(path, format="genbank")


def write_tmp_records(records, format):
    fd, tmp_path_handle = tempfile.mkstemp(suffix="." + format)
    SeqIO.write(records, tmp_path_handle, format=format)
    return tmp_path_handle


def remove_features_with_no_location(records):
    for r in records:
        r.features = [f for f in r.features if f.location is not None]


def remove_duplicate_features(record):
    pass


def add_feature(record, feature, start, end, strand):
    location = flexible_feature_location(start, end, len(record), strand)
    feature.location = location
    record.features.append(feature)


def flexible_feature_location(start, end, length, strand):
    """

    :param start: start of the feature
    :type start: int
    :param end: end of the feature
    :type end: int
    :param length: lenght of the underlying sequence
    :type length: int
    :param strand: direction; either 1 or -1
    :type strand: int
    :return:
    :rtype:
    """
    if start > end:
        if length is None:
            raise ValueError(
                "A length must be provided to create a feature with start > end."
            )
        f1 = FeatureLocation(start, length, strand)
        f2 = FeatureLocation(1, end, strand)
        if strand == -1:
            location = CompoundLocation([f2, f1])
        else:
            location = CompoundLocation([f1, f2])
    else:
        location = FeatureLocation(start, end, strand=strand)
    return location
