import os
import re
import sys

from sam_record import SamRecord


# The script:
# 1) filter out all reads that not cover a specific position (also filter out reads with juction on this position)
#    The purpose is to facilitate the showing in IGV
# 2) give a new tag that composed of RX tag (umi) and start position of mapping.
#    for example AGCCTAT_34562
#    The goal is to enable IGV to sort by this tag.

class FilterSam(object):
    def __init__(self, sam_file, chr, position, strand):
        self.sam_file = sam_file
        self.position = position
        self.strand = strand
        self.chr = chr

    def filter_sam(self):
        self.sf = open(self.sam_file)
        umi_tags = {}
        total_umis = 0
        output_base = os.path.join(os.path.dirname(self.sam_file), str(self.position) + self.strand + self.chr)
        with open(output_base + '.sam', 'w') as df:
            for line in self.sf:
                if line.startswith("@"):
                    df.writelines(line)
                    continue
                ls = line.split()
                sam_record = SamRecord(*ls[:11], tags=ls[11:])
                minus_strand = SamRecord.reverse_complement_if_needed(sam_record)
                if (self.strand == '-' and minus_strand) or (self.strand == '+' and not minus_strand):
                    if SamRecord.read_on_position(sam_record, self.position):
                        umi = SamRecord.umi_from_record(sam_record)
                        umi_start_pos_tag = "UP:Z:" + "_".join([umi, str(sam_record.pos)])
                        df.writelines(line.rstrip() + "\t" + umi_start_pos_tag + "\n")
                        if umi not in umi_tags:
                            umi_tags[umi] = 1
                            total_umis += 1
                        else:
                            umi_tags[umi] += 1
                            total_umis += 1

        with open(output_base + '.umi-stat.txt', 'w') as df:
            df.writelines("Total umis:\t%s\n" % total_umis)
            for umi, counts in umi_tags.items():
                df.writelines("\t".join([umi, str(float(counts)), str(float(counts) / total_umis), '\n']))


if __name__ == '__main__':
    input_sam_file = sys.argv[1]
    coord = sys.argv[2]  # chr1
    position, strand, chr = re.split('(-|\+)', coord)
    FilterSam(input_sam_file, chr, int(position), strand).filter_sam()
