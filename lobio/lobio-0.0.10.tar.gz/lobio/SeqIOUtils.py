from itertools import chain
from Bio import SeqIO
import tempfile


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
