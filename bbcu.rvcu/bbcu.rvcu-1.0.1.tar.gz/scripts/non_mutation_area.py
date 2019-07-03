import argparse
import logging
import re
import datetime
import pysam
import multiprocessing

logger = logging.getLogger(__name__)


class BamReader(object):
    """
    Read bam input file sorted by coordinates. Read the records of one chromosom.

    Args:
        bam_input                   (str): path to input file (bam format sorted by coordinates). Must to be bam.bai file in the same folder
        output_file                 (str): path to output file
        filtered_cell_barcodes      (dict): keys are valid cells, filtered by Seurat. values are None
        min_mapq                    (int): Minimum quality of the read mapping
        max_gene_length             (int): Maximum length of the gene. Reads that will be mapped to longer bases will be discarded
        min_cells                   (int): For each position on genome: mininum cells
        min_umis                    (int): For each position on genome: mininum umis per cell
        min_reads_per_umi           (int): For each position on genome: mininum reads in each umi

    Attributes:
        prev_sam_record             (pysam.AlignedSegment object): save the previous read

    """

    def __init__(self, bam_input, output_file, filtered_cell_barcodes, min_mapq, max_gene_length, min_cells, min_umis, min_reads_per_umi):
        self.bam_input = bam_input
        self.output_file = output_file
        self.filtered_cell_barcodes = filtered_cell_barcodes
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length
        self.bam_reader = pysam.AlignmentFile(self.bam_input, "rb")
        self.prev_sam_record = None
        self.min_cells = min_cells
        self.min_umis = min_umis
        self.min_reads_per_umi = min_reads_per_umi
        self.valid_positions = []

    def close_file(self):
        self.bam_reader.close()

    @staticmethod
    def get_chr_list(bam_input):
        """
        Get the list of chromosoms from the header lines of the bam file
        Also check that the file is sorted by coordinates

        Args:
            bam_input    (str): path of the input file

        Returns:
            chrs_list    (list of str): list of chromosoms
        """

        bam_reader = pysam.AlignmentFile(bam_input, "rb")
        if bam_reader.header['HD']['SO'] != "coordinate":
            raise ValueError("Bam is not sorted by coordinate")
        chrs_list = []
        chrs_len = []
        for line in bam_reader.header['SQ']:
            chrs_list.append(line['SN'])
            chrs_len.append(line['LN'])
        return (chrs_list, chrs_len)

    def is_mutated_read(self, pileupread):
        ref_base = pileupread.alignment.get_reference_sequence()[pileupread.query_position]
        if pileupread.alignment.query_sequence[pileupread.query_position] != ref_base:
            return ref_base
        else:
            return False

    def find_base_coverage(self, chr, chr_len):
        print "%s Start chromosome: %s" % (datetime.datetime.now(), chr)

        with open(self.output_file + '_' + chr + '.txt', 'w') as out_fh:
            # 6248811, 161038034
            # for pos in xrange(6248811, 6248812):
            # for pos in xrange(161038033, 161038034):
            # for pos in xrange(chr_len):

            for pileupcolumn in self.bam_reader.pileup(contig=chr, start=0, flag_filter=0,
                                                       ignore_orphans=False, min_mapping_quality=10,
                                                       steeper='nofilter', max_depth=100000000,
                                                       truncate=True, mark_matches=True, mark_ends=True,
                                                       add_indels=True):
                if pileupcolumn.reference_pos % 10000000 == 0:
                    print "%s: %s %s" % (datetime.datetime.now(), chr, pileupcolumn.reference_pos)

                # Filter out position with low coverage (get_num_aligned function return the reads that count by pileup
                # function except the filtered reads, but including our filtered reads).
                # if pileupcolumn.get_num_aligned() < min_total_read:
                #     continue
                pos_data = {}
                for pileupread in pileupcolumn.pileups:
                    cell_umi = pileupread.alignment.get_tag('RX')
                    if pileupread.is_del or pileupread.is_refskip or self.filter_record(pileupread.alignment,
                                                                                        cell_umi,
                                                                                        self.min_mapq,
                                                                                        self.max_gene_length):
                        continue
                    cell_barcode = cell_umi[:16]
                    if cell_barcode not in self.filtered_cell_barcodes:
                        continue
                    umi = cell_umi[16:]
                    if cell_barcode not in pos_data:
                        pos_data[cell_barcode] = {}
                    if umi not in pos_data[cell_barcode]:
                        pos_data[cell_barcode][umi] = {'mut_reads': 0, 'no_mut_reads': 0}
                    if self.is_mutated_read(pileupread):
                        pos_data[cell_barcode][umi]['mut_reads'] += 1
                    else:
                        pos_data[cell_barcode][umi]['no_mut_reads'] += 1
                valid_cells_num = self.valid_pos(pos_data)
                if valid_cells_num:
                    self.write_pos_data(out_fh, chr, pileupcolumn.reference_pos + 1, valid_cells_num)
            self.write_pos_data(out_fh)  # last iteration
        print "%s End chromosome: %s" % (datetime.datetime.now(), chr)

    def write_pos_data(self, out_fh, chr=None, pos=None, valid_cells_num=None):
        if pos:
            self.valid_positions.append('\t'.join([str(chr), str(pos), str(valid_cells_num), '\n']))
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

        """
        valid_cells_num = 0
        cells_num = len(pos_data.keys())
        if cells_num < self.min_cells:
            return False
        for cell in pos_data:
            umis_num = len(pos_data[cell].keys())
            if umis_num < self.min_umis:
                continue
            min_reads = False
            all_umis_valid = True
            for umi in pos_data[cell]:
                if pos_data[cell][umi]['mut_reads']:
                    all_umis_valid = False
                    break
                # At least one of umis contains min_reads_per_umi
                if pos_data[cell][umi]['no_mut_reads'] >= self.min_reads_per_umi:
                    min_reads = True
            if min_reads and all_umis_valid:
                valid_cells_num += 1
        if valid_cells_num < self.min_cells:
            return False
        else:
            return valid_cells_num

    def filter_record(self, record, umi, min_mapq, max_gene_length):
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
        if record.get_tag('XF').startswith('__'):  # filter out reads that didn't mapped to genes
            return True
        if record.reference_length > max_gene_length:
            return True
        else:
            return False


class StatisticsNonMutationsBases(object):
    """
    Read bam input file sorted by coordinates. Read the records of one chromosom.

    Args:
        bam_input                   (str): path to input file (bam format sorted by coordinates). Must to be bam.bai file in the same folder
        output_file                 (str): path to output file
        min_mapq                    (int): Minimum quality of the read mapping
        max_gene_length             (int): Maximum length of the gene. Reads that will be mapped to longer bases will be discarded
        min_cells                   (int): For each position on genome: mininum cells
        min_umis                    (int): For each position on genome: mininum umis per cell
        min_reads_per_umi           (int): For each position on genome: mininum reads in each umi
    """

    def __init__(self, input_file, output_file, filtered_cell_barcodes_file, min_mapq, max_gene_length, min_cells, min_umis, min_reads_per_umi):
        self.input_file = input_file
        self.output_file = output_file
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length
        self.chr_list = None  # Initialized in run function
        self.chr_lne = None  # Initialized in run function
        self.min_cells = min_cells
        self.min_umis = min_umis
        self.min_reads_per_umi = min_reads_per_umi
        self.filtered_cell_barcodes_file = filtered_cell_barcodes_file
        self.filtered_cell_barcodes = self.find_valid_cells()

    def find_valid_cells(self):
        filtered_cell_barcodes = {}
        with open(self.filtered_cell_barcodes_file, 'r') as filtered_cell_barcodes_fh:
            for line in filtered_cell_barcodes_fh:
                barcode = line[:-3]  # Remove -1\n characters in end of line
                filtered_cell_barcodes[barcode] = None
        return filtered_cell_barcodes

    def run(self):
        self.chr_list, self.chr_len = BamReader.get_chr_list(self.input_file)
        proc = []
        for chr, chr_len in zip(self.chr_list, self.chr_len):
            bam_reader = BamReader(self.input_file, self.output_file, self.filtered_cell_barcodes, self.min_mapq, self.max_gene_length,
                                   self.min_cells, self.min_umis,
                                   self.min_reads_per_umi)
            p = multiprocessing.Process(target=bam_reader.find_base_coverage, args=(chr, chr_len))
            proc.append(p)
            p.start()
        for p in proc:
            p.join()



def parse_args():
    help_txt = "Acurate assembly of transcripts according mapped reads"
    parser = argparse.ArgumentParser(description=help_txt, formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--input-file', help='Full path to input .bam or .sam file', required=True)
    parser.add_argument('--output-file', help='Full path to output file name', required=True)
    parser.add_argument('--filtered-cell-barcodes-file', help='Text file with list of cell barcodes (generally ended with -1)', required=True)
    parser.add_argument('--min-mapq', help='Minimum quality of the read mapping', type=int, default=10, required=False)
    parser.add_argument('--max-gene-length',
                        help='Maximum length of the gene. Reads that will be mapped to longer bases will be discarded',
                        type=int, default=100000, required=False)
    parser.add_argument('--min-cells', help='For each position on genome: mininum cells', type=int, default=10,
                        required=False)
    parser.add_argument('--min-umis', help='For each position on genome: mininum umis per cell', type=int, default=5,
                        required=False)
    parser.add_argument('--min-reads_per_umi',
                        help='For each position on genome: mininum reads in at least onf of umis in the cell', type=int,
                        default=2, required=False)
    parser.add_argument('--log-file', help='Log File', default=None, required=False)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    logging.info('Program started')

    StatisticsNonMutationsBases(args.input_file, args.output_file, args.filtered_cell_barcodes_file, args.min_mapq, args.max_gene_length, args.min_cells,
                                args.min_umis, args.min_reads_per_umi).run()

    logging.info('Program finished')

"""
#Run on sura:
cd /data/users/pmrefael/workspace/rvcu/scripts
python /data/users/pmrefael/workspace/rvcu/scripts/non_mutation_area.py --input-file /data/users/pmrefael/workspace/rvcu/tests-statistics/input-data-bigfiles/micePP1.bam  --output-file /data/users/pmrefael/workspace/rvcu/tests-statistics/output-data/non-mutated_bases --filtered-cell-barcodes-file /data/users/pmrefael/workspace/rvcu/tests-statistics/input-data-bigfiles/pp1-barcodes.tsv --min-mapq 10 --max-gene-length 100000 
python /data/users/pmrefael/workspace/rvcu/scripts/non_mutation_area.py --input-file /data/users/pmrefael/workspace/rvcu/tests-statistics/input-data-bigfiles/TTAGGACCAGCAGTTT.sort.bam  --output-file /data/users/pmrefael/workspace/rvcu/tests-statistics/output-data/non-mutated_bases --filtered-cell-barcodes-file /data/users/pmrefael/workspace/rvcu/tests-statistics/input-data-bigfiles/pp1-barcodes.tsv --min-mapq 10 --max-gene-length 100000

#Command for wexac (pp1 and pp2 together):
python /data/users/pmrefael/workspace/rvcu/scripts/non_mutation_area.py --input-file /home/labs/bioservices/bioinfo/eugene_project/gillev_project/micePP1-PP2.bam  --output-file /home/labs/bioservices/bioinfo/eugene_project/gillev_project/run_per_cell/positions_without_mutations/non-mutated_positions --filtered-cell-barcodes-file /home/labs/bioservices/bioinfo/eugene_project/gillev_project/pp1-pp2-barcodes.tsv --min-mapq 10 --max-gene-length 100000 


#bam must be sorted and indexed.
samtools sort ...bam > ...sorted.bam
samtools index ...sorted.bam

#Filter barcodes files:
/home/labs/gillev/Collaboration/180417_NB501465_0284_AHNYLHBGX5_10X/cell_ranger_out/micePP1_force1500/outs/filtered_gene_bc_matrices/mm10/barcodes.tsv
/home/labs/gillev/Collaboration/180417_NB501465_0284_AHNYLHBGX5_10X/cell_ranger_out/micePP2_force1500/outs/filtered_gene_bc_matrices/mm10/barcodes.tsv

"""




