import sys
import os

from sam_record import SamRecord
#The script filter out all reads with long junction so the total read length (the read and the junctions) is higher than max_gene_length parameter
class FilterSam(object):
    def __init__(self, sam_file, min_mapq, max_gene_length):
        self.sam_file = sam_file
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length

    def filter_sam(self):
        self.sf = open(self.sam_file)
        with open(os.path.splitext(self.sam_file)[0] + '_filtered.sam', 'w') as df:
            for line in self.sf:
                if line.startswith("@"):
                    df.writelines(line)
                    continue
                ls = line.split()
                sam_record = SamRecord(*ls[:11], tags=ls[11:])
                umi = SamRecord.umi_from_record(sam_record)
                if not SamRecord.filter_record(sam_record, umi, min_mapq, max_gene_length):
                    df.writelines(line)

if __name__ == '__main__':
    input_sam_file = sys.argv[1]
    min_mapq = int(sys.argv[2])
    max_gene_length = int(sys.argv[3])
    FilterSam(input_sam_file, min_mapq, max_gene_length).filter_sam()


