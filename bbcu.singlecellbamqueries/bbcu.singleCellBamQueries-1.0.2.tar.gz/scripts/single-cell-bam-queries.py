#!/usr/bin/env python

__author__ = 'Refael Kohen'


import argparse
import logging

from singleCellBamQueries.query import Query
from argparse import RawTextHelpFormatter, ArgumentDefaultsHelpFormatter
logger = logging.getLogger(__name__)

class myArgparserFormater(RawTextHelpFormatter, ArgumentDefaultsHelpFormatter):
    """
    RawTextHelpFormatter: can break lines in the help text, but don't print default values
    ArgumentDefaultsHelpFormatter: print default values, but don't break lines in the help text
    """
    pass

def parse_args():
    help_txt = """
    Queries on bam file of single cell per genome position.

    The bam file must be sorted and indexed with the commands:

    samtools sort filename.bam > filename.sorted.bam
    samtools index filename.sorted.bam
    
    By default the umi and barcode cells are comptible to bam files from cellranger. 
    For other formats you need to change the parameters of tags and cell barcodes.  
    
    For now, the script filter out the reads with deletions/insersions/soft and hard clipped.
    In the next version it will be parameter to user.
    """
    # parser = argparse.ArgumentParser(description=help_txt, formatter_class=RawTextHelpFormatter)
    # parser = argparse.ArgumentParser(description=help_txt, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser = argparse.ArgumentParser(description=help_txt, formatter_class=myArgparserFormater)

    parser.add_argument('--input-file', help='Full path to input .bam or .sam file', required=True)
    parser.add_argument('--output-file', help='Full path to output file name', required=True)
    parser.add_argument('--coordinates',
                        help='Coordinates of the genome. The default is all genome. For example: chr1:1000000-2000000, or for all chromosom: chr1',
                        default='all', required=False)
    parser.add_argument('--filtered-cell-barcodes-file',
                        help='Text file with list of cell barcodes. Counts only these cells (optional)', default=None,
                        required=False)
    parser.add_argument('--min-mapq', help='Minimum quality of the read mapping', type=int, default=10, required=False)
    parser.add_argument('--max-gene-length',
                        help='Maximum length of the gene. Reads that will be mapped to longer bases will be discarded',
                        type=int, default=100000, required=False)
    parser.add_argument('--threads',
                        help='number of threads. You can run the chromosome itself in several threads. You can use this prameter only if you specify the start and end coordinates explicitely in the format: chr1:0-14000000 or if the bam file contains header lines with the lengths of the chromosomes, you can check it with the commands: samtools view -h filename.bam',
                        type=int, default=1, required=False)
    parser.add_argument('--min-cells',
                        help='mininum cells in genome position that contains the number of umis and reads according to the other parameters',
                        type=int, default=1, required=False)
    parser.add_argument('--max-cells',
                        help='maximum cells in genome position that contains the number of umis and reads according to the other parameters',
                        type=int, default=1000000000, required=False)
    parser.add_argument('--min-mutated-umis',
                        help='mininum umis per cell that all reads contain mutation in the position',
                        type=int, default=1, required=False)
    parser.add_argument('--max-mutated-umis',
                        help='maximum umis per cell that all reads contain mutation in the position',
                        type=int, default=1000000000, required=False)
    parser.add_argument('--min-reads-per-non-mutated-umi',
                        help='mininum reads in at least one of umis in the cell in genome position',
                        type=int, default=1, required=False)
    parser.add_argument('--max-reads-per-non-mutated-umi',
                        help='maximum reads in at least one of umis in the cell in genome position',
                        type=int, default=1000000000, required=False)
    parser.add_argument('--min-non-mutated-umis',
                        help='mininum umis per cell that all reads not contain mutation in the genome position',
                        type=int, default=1, required=False)
    parser.add_argument('--max-non-mutated-umis',
                        help='maximum umis per cell that all reads not contain mutation in the genome position',
                        type=int, default=1000000000, required=False)
    parser.add_argument('--min-reads-per-mutated-umi',
                        help='mininum reads in at least one of umis in the cell in genome position',
                        type=int, default=1, required=False)
    parser.add_argument('--max-reads-per-mutated-umi',
                        help='maximum reads in at least one of umis in the cell in genome position',
                        type=int, default=1000000000, required=False)
    parser.add_argument('--enable-cells-with-invalid-umis-num',
                        help='enable positions that contain cell/s with not valid umis number (according to ther range in the other parameters)',
                        action='store_true', default=False, required=False)
    parser.add_argument('--enable-umis-with-invalid-reads-num',
                        help='enable positions that contain umi/s with not valid reads number (according to ther range in the other parameters)',
                        action='store_true', default=False, required=False)
    parser.add_argument('--tag-of-umi', help='the tag of umi in bam file', type=str, default='UR', required=False)
    parser.add_argument('--tag-of-cell-barcode', help='the tag of umi in bam file', type=str, default='CR', required=False)
    parser.add_argument('--umi-start', help='location in tag where the umi start (0-based)', type=int, default=0, required=False)
    parser.add_argument('--umi-length', help='length of umi', type=int, default=10, required=False)
    parser.add_argument('--cell-barcode-start', help='location in tag where the cell barcode start (0-based)', type=int, default=0, required=False)
    parser.add_argument('--cell-barcode-length', help='length of cell barcode', type=int, default=16, required=False)
    parser.add_argument('--log-file', help='Log File', default=None, required=False)
    return parser.parse_args()


if __name__ == "__main__":
    logging_args = {
        "level": logging.DEBUG,
        "filemode": 'w',
        "format": '%(asctime)s %(message)s',
        "datefmt": '%m/%d/%Y %H:%M:%S'
    }
    args = parse_args()

    # set up log file
    if args.log_file is not None:
        logging_args["filename"] = args.logFile
    logging.basicConfig(**logging_args)

    logging.info('Program started')

    Query(args.input_file, args.output_file, args.coordinates, args.filtered_cell_barcodes_file,
          args.min_mapq, args.max_gene_length, args.threads, args.min_cells, args.max_cells,
          args.min_mutated_umis, args.max_mutated_umis, args.min_reads_per_mutated_umi,
          args.max_reads_per_mutated_umi, args.min_non_mutated_umis, args.max_non_mutated_umis,
          args.min_reads_per_non_mutated_umi, args.max_reads_per_non_mutated_umi,
          args.enable_cells_with_invalid_umis_num,
          args.enable_umis_with_invalid_reads_num, args.tag_of_umi, args.tag_of_cell_barcode, args.umi_start,
          args.umi_length, args.cell_barcode_start, args.cell_barcode_length).run()

    logging.info('Program finished')

"""
#Run on sura:
cd /data/users/pmrefael/workspace/single-cell-bam-queries/singleCellBamQueries/
python /data/users/pmrefael/workspace/single-cell-bam-queries/singleCellBamQueries/single-cell-bam-queries.py --input-file /data/users/pmrefael/workspace/rvcu/tests-statistics/input-data-bigfiles/TTAGGACCAGCAGTTT.sort.bam --output-file /data/users/pmrefael/workspace/rvcu/tests-statistics/output-data/non-mutated_bases --filtered-cell-barcodes-file /data/users/pmrefael/workspace/rvcu/tests-statistics/input-data-bigfiles/pp1-barcodes.tsv --min-mapq 10 --max-gene-length 100000 --threads 1 --tag-of-umi RX --tag-of-cell-barcode RX --umi-start 16 --umi-length 10 --cell-barcode-start 0 --cell-barcode-length 16

#bam must be sorted and indexed.
samtools sort ...bam > ...sorted.bam
samtools index ...sorted.bam

#Filter barcodes files:
/home/labs/gillev/Collaboration/180417_NB501465_0284_AHNYLHBGX5_10X/cell_ranger_out/micePP1_force1500/outs/filtered_gene_bc_matrices/mm10/barcodes.tsv
/home/labs/gillev/Collaboration/180417_NB501465_0284_AHNYLHBGX5_10X/cell_ranger_out/micePP2_force1500/outs/filtered_gene_bc_matrices/mm10/barcodes.tsv

"""
#TODO:
#Support also reads with deletions/insertions/clipped
#Filter reads: user will can select the filtering.





