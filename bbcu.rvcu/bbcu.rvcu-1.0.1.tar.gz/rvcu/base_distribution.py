import os
import sys
from collections import Counter, OrderedDict

from sam_record import SamRecord


# The script filter out all reads with long junction so the total read length (the read and the junctions) is higher than max_gene_length parameter
class FilterSam(object):
    def __init__(self, sam_file, min_mapq, max_gene_length, filter_edge_mutations, bases_distribution, reads_count):
        self.sam_file = sam_file
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length
        self.filter_edge_mutations = filter_edge_mutations
        self.bases_distribution = bases_distribution
        self.reads_count = reads_count

    def update_bases_distribution(self, record):
        if SamRecord.is_record_umi_duplication(record):  # Count only one read per UMI
            return
        minus_strand = SamRecord.reverse_complement_if_needed(record)
        if self.bases_distribution:  # for the tests - the value in None
            self.reads_count[0] += 1
            if filter_edge_mutations != 0:
                c = Counter(record.seq[filter_edge_mutations:-filter_edge_mutations])
            else:  # -0 don't give the end of the string
                c = Counter(record.seq)
            self.bases_distribution['A'] += c['A']
            self.bases_distribution['G'] += c['G']
            self.bases_distribution['C'] += c['C']
            self.bases_distribution['T'] += c['T']
            self.bases_distribution['N'] += c['N']

    def filter_sam(self):
        self.sf = open(self.sam_file)
        for line in self.sf:
            if line.startswith("@"):
                continue
            ls = line.split()
            sam_record = SamRecord(*ls[:11], tags=ls[11:])
            umi = SamRecord.umi_from_record(sam_record)
            if not SamRecord.filter_record(sam_record, umi, min_mapq, max_gene_length):
                self.update_bases_distribution(sam_record)


if __name__ == '__main__':
    input_sam_file = sys.argv[1]
    filter_edge_mutations = int(sys.argv[2])
    min_mapq = int(sys.argv[3])
    max_gene_length = int(sys.argv[4])
    bases_distribution = OrderedDict({'A': 0, 'C': 0, 'G': 0, 'T': 0, 'N': 0})
    reads_count = [0]
    FilterSam(input_sam_file, min_mapq, max_gene_length, filter_edge_mutations, bases_distribution,
              reads_count).filter_sam()
    with open(os.path.splitext(input_sam_file)[0] + '_bases_distribution-%s-end.txt' % filter_edge_mutations,
              'w') as df:
        df.writelines('Base\tCount\n')
        for base, count in bases_distribution.items():
            df.writelines('%s\t' % base)
        df.writelines('\n')
        for base, count in bases_distribution.items():
            df.writelines('%s\t' % str(count))
        df.writelines('\n')
        df.writelines('total filtered reads: %s' % (str(reads_count[0])))
