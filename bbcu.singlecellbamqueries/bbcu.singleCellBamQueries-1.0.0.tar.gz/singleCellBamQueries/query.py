import logging
import multiprocessing
from math import ceil, floor

from positions_query import PositionsQuery

logger = logging.getLogger(__name__)


class Query(object):
    """
    Read bam input file sorted by coordinates. Read the records of one chromosom.

    Args:
        bam_input                               (str): path to input file (bam format sorted by coordinates). Must to be bam.bai file in the same folder
        output_file                             (str): path to output file
        min_mapq                                (int): Minimum quality of the read mapping
        max_gene_length                         (int): Maximum length of the gene. Reads that will be mapped to longer bases will be discarded
        threads                                 (int): number of threads in each chromosome. The program run each chromose in parallel. You can run the chromosome itself in several threads. You can use this prameter only if you specify the start and end coordinates explicitely in the format: chr1:0-14000000 or if the bam file contains header lines with the lengths of the chromosomes, you can check it with the commands: samtools view -h filename.bam
        min_cells                               (int): mininum cells in genome position that contains the number of umis and reads according to the other parameters
        max_cells                               (int): maximum cells in genome position that contains the number of umis and reads according to the other parameters
        min_mutated_umis                        (int): mininum umis per cell that all reads contain mutation in the position
        max_mutated_umis                        (int): maximum umis per cell that all reads contain mutation in the position
        min_reads_per_mutated_umi               (int): mininum reads in at least one of umis in the cell in genome position
        max_reads_per_mutated_umi               (int): maximum reads in at least one of umis in the cell in genome position
        min_non_mutated_umis                    (int): mininum umis per cell that all reads not contain mutation in the genome position
        max_non_mutated_umis                    (int): maximum umis per cell that all reads not contain mutation in the genome position
        min_reads_per_non_mutated_umi           (int): mininum reads in at least one of umis in the cell in genome position
        max_reads_per_non_mutated_umi           (int): maximum reads in at least one of umis in the cell in genome position
        enable_cells_with_invalid_umis_num    (int): enable positions that contain cell/s with not valid umis number (according to ther range in the other parameters)
        enable_umis_with_invalid_reads_num    (int): enable positions that contain umi/s with not valid reads number (according to ther range in the other parameters)
    """

    def __init__(self, input_file, output_file, coordinates, filtered_cell_barcodes_file, min_mapq, max_gene_length,
                 threads, min_cells, max_cells, min_mutated_umis, max_mutated_umis, min_reads_per_mutated_umi,
                 max_reads_per_mutated_umi, min_non_mutated_umis, max_non_mutated_umis, min_reads_per_non_mutated_umi,
                 max_reads_per_non_mutated_umi, enable_cells_with_invalid_umis_num,
                 enable_umis_with_invalid_reads_num, tag_of_umi, tag_of_cell_barcode, umi_start, umi_length,
                 cell_barcode_start, cell_barcode_length):
        self.input_file = input_file
        self.output_file = output_file
        self.coordinates = self.parse_coordinates(coordinates)
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length
        self.threads = threads
        self.min_cells = min_cells
        self.max_cells = max_cells
        self.min_mutated_umis = min_mutated_umis
        self.max_mutated_umis = max_mutated_umis
        self.min_reads_per_mutated_umi = min_reads_per_mutated_umi
        self.max_reads_per_mutated_umi = max_reads_per_mutated_umi
        self.min_non_mutated_umis = min_non_mutated_umis
        self.max_non_mutated_umis = max_non_mutated_umis
        self.min_reads_per_non_mutated_umi = min_reads_per_non_mutated_umi
        self.max_reads_per_non_mutated_umi = max_reads_per_non_mutated_umi
        self.filtered_cell_barcodes_file = filtered_cell_barcodes_file
        self.enable_cells_with_invalid_umis_num = enable_cells_with_invalid_umis_num
        self.enable_umis_with_invalid_reads_num = enable_umis_with_invalid_reads_num
        self.tag_of_umi = tag_of_umi
        self.tag_of_cell_barcode = tag_of_cell_barcode
        self.umi_start = umi_start
        self.umi_length = umi_length
        self.cell_barcode_start = cell_barcode_start
        self.cell_barcode_length = cell_barcode_length

        if filtered_cell_barcodes_file:
            self.filtered_cell_barcodes = self.find_valid_cells()

    def find_valid_cells(self):
        filtered_cell_barcodes = {}
        with open(self.filtered_cell_barcodes_file, 'r') as filtered_cell_barcodes_fh:
            for line in filtered_cell_barcodes_fh:
                line = line.strip()
                if line.endswith("-1"):
                    line = line[:-2]  # Remove -1 characters in end of line
                filtered_cell_barcodes[line] = None
        return filtered_cell_barcodes

    def parse_coordinates(self, coordinates):
        if coordinates == 'all':
            return [coordinates]
        import re
        # coordinates = 'chr1'
        # coordinates = 'chr1:223-444'
        chrom = re.compile('(\S+)')
        coor = re.compile('(\S+):(\d+)-(\d+)')
        if coor.match(coordinates):
            return coor.match(coordinates).groups()
        elif chrom.match(coordinates):
            return [chrom.match(coordinates).groups()[0]]
        else:
            raise IOError("The coordinates are not valid")

    def run(self):
        chrom_list, starts, ends = [], [], []
        # if need to get the lengths of the chromosomes from the bam file
        if self.coordinates == ['all'] or (self.threads > 1 and len(self.coordinates) != 3):
            chrom_list, starts, ends = PositionsQuery.get_chrom_list(self.input_file)
        if self.coordinates != ['all'] and len(self.coordinates) == 1:
            if self.threads > 1:  # get the chrom length
                for c, l in zip(chrom_list, ends):  # chrom_list already defined in previous "if"
                    if self.coordinates[0] == c:
                        ends = [l]
                        break
            else:
                ends = [None]

            chrom_list, starts = [self.coordinates[0]], [0]
        if len(self.coordinates) == 3:
            chrom_list, starts, ends = [self.coordinates[0]], [int(self.coordinates[1])], [int(self.coordinates[2])]

        if self.threads > len(chrom_list):
            segment_num_per_chrom = int(floor(self.threads / len(chrom_list)))
            cutted_chrom_list = []
            cutted_starts = []
            cutted_ends = []
            for chrom, start, end in zip(chrom_list, starts, ends):
                segment_size = int(ceil(float(end - start + 1) / segment_num_per_chrom))
                s = start
                for i in xrange(segment_num_per_chrom):
                    cutted_chrom_list.append(chrom)
                    cutted_starts.append(s)
                    cutted_ends.append(min(s + segment_size, end))
                    s += segment_size + 1
            chrom_list = cutted_chrom_list
            starts = cutted_starts
            ends = cutted_ends

        logger.info('The program run with %s threads in parallel on the segments:' % self.threads)
        for chrom, start, end in zip(chrom_list, starts, ends):
            logger.info('%s:%s-%s' % (chrom, start, end))

        pool = multiprocessing.Pool(processes=self.threads)
        for chrom, start, end in zip(chrom_list, starts, ends):
            bam_reader = PositionsQuery(self.input_file, self.output_file, self.filtered_cell_barcodes,
                                        self.min_mapq,
                                        self.max_gene_length, self.min_cells, self.max_cells, self.min_mutated_umis,
                                        self.max_mutated_umis, self.min_reads_per_mutated_umi,
                                        self.max_reads_per_mutated_umi, self.min_non_mutated_umis,
                                        self.max_non_mutated_umis,
                                        self.min_reads_per_non_mutated_umi, self.max_reads_per_non_mutated_umi,
                                        self.enable_cells_with_invalid_umis_num,
                                        self.enable_umis_with_invalid_reads_num,
                                        self.tag_of_umi, self.tag_of_cell_barcode, self.umi_start, self.umi_length,
                                        self.cell_barcode_start, self.cell_barcode_length)
            pool.apply_async(bam_reader.find_base_coverage, args=(chrom, start, end))
        pool.close()
        pool.join()
