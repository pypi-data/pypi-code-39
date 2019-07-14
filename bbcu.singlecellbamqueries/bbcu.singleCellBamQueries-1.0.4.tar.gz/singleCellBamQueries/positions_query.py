import datetime
import logging
import re
import sys

import pysam

logger = logging.getLogger(__name__)


class PositionsQuery(object):
    """
    Read bam input file sorted by coordinates. Read the records of one chromosom.

    Args:
        bam_input                               (str): path to input file (bam format sorted by coordinates). Must to be bam.bai file in the same folder
        output_file                             (str): path to output file
        filtered_cell_barcodes                  (dict): keys are valid cells, filtered by Seurat. values are None
        min_mapq                                (int): Minimum quality of the read mapping
        max_gene_length                         (int): Maximum length of the gene. Reads that will be mapped to longer bases will be discarded
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
        enable_cells_with_invalid_umis_num      (int): enable positions that contain cell/s with not valid umis number (according to ther range in the other parameters)
        enable_umis_with_invalid_reads_num      (int): enable positions that contain umi/s with not valid reads number (according to ther range in the other parameters)

    Attributes:
        prev_sam_record             (pysam.AlignedSegment object): save the previous read

    """

    def __init__(self, bam_input, output_file, filtered_cell_barcodes, min_mapq, max_gene_length, min_cells, max_cells,
                 min_mutated_umis, max_mutated_umis, min_reads_per_mutated_umi,
                 max_reads_per_mutated_umi, min_non_mutated_umis, max_non_mutated_umis, min_reads_per_non_mutated_umi,
                 max_reads_per_non_mutated_umi, enable_cells_with_invalid_umis_num,
                 enable_umis_with_invalid_reads_num, tag_of_umi, tag_of_cell_barcode, umi_start, umi_length,
                 cell_barcode_start, cell_barcode_length):
        self.bam_input = bam_input
        self.output_file = output_file
        self.filtered_cell_barcodes = filtered_cell_barcodes
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length
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
        self.enable_cells_with_invalid_umis_num = enable_cells_with_invalid_umis_num
        self.enable_umis_with_invalid_reads_num = enable_umis_with_invalid_reads_num
        self.tag_of_umi = tag_of_umi
        self.tag_of_cell_barcode = tag_of_cell_barcode
        self.umi_start = umi_start
        self.umi_length = umi_length
        self.cell_barcode_start = cell_barcode_start
        self.cell_barcode_length = cell_barcode_length

        if self.bam_input:  # for the tests
            self.bam_reader = pysam.AlignmentFile(self.bam_input, "rb")
        self.prev_sam_record = None
        self.valid_positions = []

    def close_file(self):
        self.bam_reader.close()

    @staticmethod
    def get_chrom_list(bam_input):
        """
        Get the list of chromosoms from the header lines of the bam file
        Also check that the file is sorted by coordinates

        Args:
            bam_input    (str): path of the input file

        Returns:
            chrom_list    (list of str): list of chromosoms
        """

        bam_reader = pysam.AlignmentFile(bam_input, "rb")
        if bam_reader.header['HD']['SO'] != "coordinate":
            raise ValueError("Bam is not sorted by coordinate")
        chrom_list = []
        chroms_starts = []
        chroms_len = []

        try:
            for line in bam_reader.header['SQ']:
                chrom_list.append(line['SN'])
                chroms_len.append(int(line['LN']))
                chroms_starts.append(0)
        except Exception:
            raise IOError(
                "You cannot run on all genome because the bam file don't contain header lines with information on the chromosomes. You need supply coordinates manually.")
        return (chrom_list, chroms_starts, chroms_len)

    def is_mutated_read(self, pileupread):
        ref_base = pileupread.alignment.get_reference_sequence()[pileupread.query_position]
        if pileupread.alignment.query_sequence[pileupread.query_position] != ref_base:
            return ref_base
        else:
            return False

    def find_base_coverage(self, chrom='all', start=0, end=None):
        str_end = '-' + str(end) if end else ''
        print "%s Start chromomosome: %s:%s%s " % (datetime.datetime.now(), chrom, start, str_end)
        output_file_name = self.output_file + '_' + str(chrom) + '.txt' if not end else self.output_file + '_' + str(
            chrom) + '_' + str(start) + '_' + str(end) + '.txt'
        with open(output_file_name, 'w') as out_fh:
            # 6248811, 161038034
            # for pos in xrange(6248811, 6248812):
            # for pos in xrange(161038033, 161038034):
            # for pos in xrange(chrom_len):

            for pileupcolumn in self.bam_reader.pileup(contig=chrom, start=start, end=end, flag_filter=0,
                                                       ignore_orphans=False, min_mapping_quality=10,
                                                       steeper='nofilter', max_depth=100000000,
                                                       truncate=True, mark_matches=True, mark_ends=True,
                                                       add_indels=True):
                if pileupcolumn.reference_pos % 10000000 == 0:
                    print "%s: %s:%s%s %s" % (
                        datetime.datetime.now(), chrom, start, str_end, pileupcolumn.reference_pos)

                    sys.stdout.flush()

                # Filter out position with low coverage (get_num_aligned function return the reads that count by pileup
                # function except the filtered reads, but including our filtered reads).
                # if pileupcolumn.get_num_aligned() < min_total_read:
                #     continue
                pos_data = {}
                for pileupread in pileupcolumn.pileups:
                    cell_barcode = pileupread.alignment.get_tag(self.tag_of_cell_barcode)[
                                   self.cell_barcode_start:self.cell_barcode_length]
                    umi = pileupread.alignment.get_tag(self.tag_of_umi)[self.umi_start:self.umi_length]

                    if pileupread.is_del or pileupread.is_refskip or self.filter_record(pileupread.alignment,
                                                                                        cell_barcode, umi,
                                                                                        self.min_mapq,
                                                                                        self.max_gene_length):
                        continue

                    if self.filtered_cell_barcodes:
                        if cell_barcode not in self.filtered_cell_barcodes:
                            continue
                    if cell_barcode not in pos_data:
                        pos_data[cell_barcode] = {}
                    if umi not in pos_data[cell_barcode]:
                        pos_data[cell_barcode][umi] = {'mut_reads': 0, 'no_mut_reads': 0}
                    if self.is_mutated_read(pileupread):
                        pos_data[cell_barcode][umi]['mut_reads'] += 1
                    else:
                        pos_data[cell_barcode][umi]['no_mut_reads'] += 1
                valid_cells_num, valid_cells = self.valid_pos(pos_data)
                if valid_cells_num:
                    self.write_pos_data(out_fh, chrom, pileupcolumn.reference_pos + 1, valid_cells_num, valid_cells)
            self.write_pos_data(out_fh)  # last iteration
        print "%s End chromomosome: %s:%s%s " % (datetime.datetime.now(), chrom, start, str_end)

    def write_pos_data(self, out_fh, chrom=None, pos=None, valid_cells_num=None, valid_cells=None):
        if pos:
            cells = ','.join(valid_cells)
            self.valid_positions.append('\t'.join([str(chrom), str(pos), str(valid_cells_num), cells, '\n']))
        if pos and len(self.valid_positions) > 100:
            out_fh.writelines(self.valid_positions)
            self.valid_positions = []
        if not pos:  # last iteration
            out_fh.writelines(self.valid_positions)
            self.valid_positions = []

    def valid_pos(self, pos_data):
        """
        Requiremnts:
        At least 10 valid cells

        valid cell:
        - At least 5 umis
        - No read with mutation
        - There exist at least one umi with at least 2 reads.

        Args:
            pos_data:   (dict): cells:umis:num_mutated_reads
                                          :num_not_mutated_reads

        Returns:
            number of valid cells and list of their cell barcodes
        """
        valid_cells_num = 0
        valid_cells = []
        cells_num = len(pos_data.keys())
        if cells_num < self.min_cells or cells_num > self.max_cells:
            return (False, False)
        for cell in pos_data:
            invalid_cell = False
            umis_num = len(pos_data[cell].keys())
            if (umis_num < self.min_mutated_umis and umis_num < self.min_non_mutated_umis) or (
                    umis_num > self.max_mutated_umis and umis_num > self.max_non_mutated_umis):
                if not self.enable_cells_with_invalid_umis_num:
                    return (False, False)
                else:
                    continue
            valid_mutated_umis_num = 0
            valid_non_mutated_umis_num = 0
            for umi in pos_data[cell]:
                mut_reads_num = pos_data[cell][umi]['mut_reads']
                no_mut_reads_num = pos_data[cell][umi]['no_mut_reads']
                if mut_reads_num and no_mut_reads_num:
                    if not self.enable_umis_with_invalid_reads_num:
                        invalid_cell = True
                        if not self.enable_cells_with_invalid_umis_num:
                            return (False, False)
                        break  # enable invalid cells, but not invalid umis - break from the cell.
                    continue  # enable invalid umi, continue to the next umi
                if mut_reads_num:
                    if mut_reads_num < self.min_reads_per_mutated_umi or mut_reads_num > self.max_reads_per_mutated_umi:
                        if not self.enable_umis_with_invalid_reads_num:
                            invalid_cell = True
                            if not self.enable_cells_with_invalid_umis_num:
                                return (False, False)
                            break  # enable invalid cells, but not invalid umis - break from the cell.
                        continue  # enable invalid umi, continue to the next umi
                    valid_mutated_umis_num += 1
                elif no_mut_reads_num:
                    if no_mut_reads_num < self.min_reads_per_non_mutated_umi or no_mut_reads_num > self.max_reads_per_non_mutated_umi:
                        if not self.enable_umis_with_invalid_reads_num:
                            invalid_cell = True
                            if not self.enable_cells_with_invalid_umis_num:
                                return (False, False)
                            break  # enable invalid cells, but not invalid umis - break from the cell.
                        continue  # enable invalid umi, continue to the next umi
                    valid_non_mutated_umis_num += 1
            if not invalid_cell:
                if (
                        valid_mutated_umis_num >= self.min_mutated_umis and valid_mutated_umis_num <= self.max_mutated_umis) or (
                        valid_non_mutated_umis_num >= self.min_non_mutated_umis and valid_non_mutated_umis_num <= self.max_non_mutated_umis):
                    valid_cells_num += 1
                    valid_cells.append(cell)
                else:
                    if not self.enable_cells_with_invalid_umis_num:
                        return (False, False)
        # print 'num valid cells %s' %valid_cells_num
        if valid_cells_num < self.min_cells or valid_cells_num > self.max_cells:
            return (False, False)
        else:
            return (valid_cells_num, valid_cells)

    def filter_record(self, record, cell_barcode, umi, min_mapq, max_gene_length):
        """
        Args:
            record              (pysam.AlignedSegment object): one read
            min_mapq            (int): Minimum quality of the read mapping
            max_gene_length     (int): Maximum length of the gene. Reads that will be mapped to longer bases will be discarded

        Returns:
            filtered            (bool): True if filtered out, else False
        """

        if re.findall(r"([DSHI]+)", record.cigarstring):  # filter reads with mutation/insertion/softclipped/hardclipped
            return True
        if record.mapq < min_mapq:  # Mapq 10 and above is uniquely mapped
            return True
        if 'N' in umi:
            return True
        if 'N' in cell_barcode:
            return True
        if record.get_tag('XF').startswith('__'):  # filter out reads that didn't mapped to genes
            return True
        if record.reference_length > max_gene_length:
            return True
        else:
            return False
