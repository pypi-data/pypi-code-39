import bisect
import datetime
import gc
import math
import os
import sys
from collections import OrderedDict, Counter
from multiprocessing import Process, Queue, Manager

import resource

from create_vcf import MutationClassifier, CreateVCF
from sam_record import SamRecord, SamReader
from utils import limit_memory_usage_gb

FILES_TO_REMOVE = []

"""
samtools view -F 1024 {input} | grep -v RX:Z:[ACTG]*N[ACTGN]*

LocationsWithMutations
    locations (dict) - sorted during the run.
        keys: location numbers
        values: Location object
            loc (int)
            ref_letter (char)
            all_mutations (list)
            umis: (dict)
                keys: umi
                values: UMImutation
                            umi (string)
                            fragments: (dict):
                                keys: mapping start
                                values: UMIFragMutation object
"""


class Location(object):
    """Storage information on mutation on specific location on the reference genome

    Args:
        loc             (int): coordinate on the genome - without chr number (in order to facilitate the access to this number)
        chr             (str): name of the chromosom
        ref_letter      (str): base on the reference genome
    Attributes:
        umis            (dict of str: UMImutation):
                            keys - umi string,
                            values - UMImutation object. all UMIs that mapped to this location
        all_mutations   (dict of str: int):
                            keys - mutation (base A/G/C/T),
                            values - total number of reads with this mutation (all umis)
    """

    def __init__(self, loc, chr, ref_letter):
        self.loc = loc
        self.chr = chr
        self.ref_letter = ref_letter
        self.umis = {}
        self.all_mutations = {}

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)


class UMImutation(object):
    """Storage the information on mutations in specific UMI (all fragments)
    Args:
        umi                             (str): UMI sequence
    Attributes:
        pure_fragments_per_mut          (dict of str: list of [int, int]):
                                            keys - mutation type,
                                            values - [num pure fragments (contain only this mutation/s),
                                            total counts of reads over all fragments]
        dirty_fragments                 (dict of int:None):
                                            keys: location of fragment,
                                            values: None. Using for the number of the dirty fragments by len(dirty_fragments)
        total_reads                     (int): total number of reads (with/out mutation), on pure and dirty fragments for all mutations
        mutated_reads_num_per_mut       (dict of str:int): for each mutation, how many reads contains the mutation
                                            keys - mutation (A/G/C/T),
                                            value - counts of reads. For each mutation,
                                            how much reads there is in total over all (dirty and pure) fragments.
        no_mutated_reads_num            (int): total reads without mutation (and apear only in dirty fragments).
        fragments                       (dict of int: UMIFragMutation object):
                                            key - start position of the read,
                                            value - UMIFragMutation
        # total_reads_dirty             (int): total number of reads without mutation or with other mutation (total on all mutations) TODO: Not in using. remove it
        # mut_dirty_total_per_mutation    for each mutation, how much reads there is in total over all dirty fragments. non-mutations signed by 'None' key TODO: Not in using. remove it
    """

    def __init__(self, umi):
        self.umi = umi
        self.pure_fragments_per_mut = {}
        self.dirty_fragments = {}
        self.total_reads = 0
        self.mutated_reads_num_per_mut = {}
        # self.total_reads_dirty = 0 TODO: Not in using. remove it
        self.no_mutated_reads_num = 0
        self.fragments = {}
        # self.mut_dirty_total_per_mutation = {} TODO: Not in using. remove it

    # Must run before add_mutation or add_no_mutation of UMIFragMutation object
    def update_umi_mutations(self, record, mut_letter=None):  # mut_letter=None if updating record without mutation
        # This step all fragments are pure (meantime we have no non-mutations reads) unless position contains more than one mutation type
        # add if not exists
        pos = record.pos
        self.total_reads += 1
        if mut_letter:
            if mut_letter not in self.mutated_reads_num_per_mut:
                self.mutated_reads_num_per_mut[mut_letter] = 0
            self.mutated_reads_num_per_mut[mut_letter] += 1
        else:
            self.no_mutated_reads_num += 1
        if self.fragments[pos].frag_type == 0:  # A new pure position
            if mut_letter:
                self.fragments[pos].frag_type = 1  # Pure position
                if mut_letter not in self.pure_fragments_per_mut:
                    self.pure_fragments_per_mut[mut_letter] = [0, 0]
                self.pure_fragments_per_mut[mut_letter][0] += 1
                self.pure_fragments_per_mut[mut_letter][1] += 1
            else:  # Record without mutation
                self.fragments[pos].frag_type = 2  # Dirty position
                self.dirty_fragments[pos] = None
                # if mut_letter not in self.mut_dirty_total_per_mutation: TODO: Not in using. remove it
                #     self.mut_dirty_total_per_mutation[mut_letter] = 0 TODO: Not in using. remove it
                # self.mut_dirty_total_per_mutation[mut_letter] += 1 TODO: Not in using. remove it
                # self.total_reads_dirty += 1 TODO: Not in using. remove it
        elif self.fragments[pos].frag_type == 1:  # An old pure position
            old_mutation = self.fragments[pos].qry_letter_counts.keys()[0]
            if mut_letter == old_mutation:  # Only one mutaion because frag_type is 1
                self.pure_fragments_per_mut[mut_letter][1] += 1  # This pos already exists in pure_fragments_per_mut
            else:  # The new mutation differ than old mutation OR mut_letter is None (record without mutation)
                self.fragments[pos].frag_type = 2
                self.dirty_fragments[pos] = None
                # add this position to dirty
                # if mut_letter not in self.mut_dirty_total_per_mutation: TODO: Not in using. remove it
                #     self.mut_dirty_total_per_mutation[mut_letter] = 0 TODO: Not in using. remove it
                # if old_mutation not in self.mut_dirty_total_per_mutation: TODO: Not in using. remove it
                #     self.mut_dirty_total_per_mutation[old_mutation] = 0 TODO: Not in using. remove it
                # for each mutation the dirty is the counts of the other different mutations
                # self.mut_dirty_total_per_mutation[old_mutation] += self.fragments[pos].qry_letter_counts[old_mutation] TODO: Not in using. remove it
                # self.mut_dirty_total_per_mutation[mut_letter] += 1  # add current record TODO: Not in using. remove it
                # self.total_reads_dirty += self.fragments[pos].qry_letter_counts[old_mutation] + 1 TODO: Not in using. remove it

                # Remove this position form pure fragments of the old_mutation
                self.pure_fragments_per_mut[old_mutation][0] -= 1
                self.pure_fragments_per_mut[old_mutation][1] -= self.fragments[pos].qry_letter_counts[old_mutation]
                if self.pure_fragments_per_mut[old_mutation][0] == 0:  # No remained fragments
                    del self.pure_fragments_per_mut[old_mutation]
        elif self.fragments[pos].frag_type == 2:  # An old dirty position
            # if mut_letter not in self.mut_dirty_total_per_mutation: TODO: Not in using. remove it
            #     self.mut_dirty_total_per_mutation[mut_letter] = 0 TODO: Not in using. remove it
            # self.mut_dirty_total_per_mutation[mut_letter] += 1 TODO: Not in using. remove it
            # self.total_reads_dirty += 1 TODO: Not in using. remove it
            pass


class UMIFragMutation(object):
    """Save the information on mutations (and reads without mutation) in specific fragment of specific umi

    Args:
        umi                         (str): umi sequence. for example GCTTACTC
        start_loc                   (int): start location of the reads. It is characterizing of one product of the fragmentation
        ref_letter                  (str): one letter ('A','G','C' or 'T'). the base in the reference in the location of the mutation

    Attributes:
        qry_letter_counts_total     (int): total number of reads in this fragmets (with and without mutation)
        no_mutation                 (int): number of reads without mutation in this fragment
        qry_letter_counts           (dict of str: int):
                                        key - mutation (A,G,C or T) in reads.
                                        value - number of reads with this mutation. for example:{'G': 2, 'T':1}
        quality                     (dict of str: list of str):
                                        key - mutation (A,G,C or T) in reads.
                                        value - list of qualities of this mutation on the different reads on this fragment.
                                        for example: {'G': ['B', 'O'], 'T':['Z']}
        frag_type                   (int): type of the mutations in this fragment.
                                        0-initialization, 1-pure i.e. all read have the same mutation,
                                        2-dirty i.e. the reads contain several different mutations or part of reads no have mutations
    """

    def __init__(self, umi, start_loc, ref_letter):
        self.umi = umi
        self.start_loc = start_loc
        self.ref_letter = ref_letter
        self.qry_letter_counts_total = 0  # count of all mutations
        self.no_mutation = 0
        self.qry_letter_counts = {}
        self.quality = {}
        self.frag_type = 0  # 0-initialization, 1-pure with one mutation, 2-dirty with more than one mutation

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def add_mutation(self, qry_letter, quality):
        if qry_letter in self.qry_letter_counts:
            self.qry_letter_counts[qry_letter] += 1
            self.quality[qry_letter].append(quality)
        else:
            self.qry_letter_counts[qry_letter] = 1
            self.quality[qry_letter] = [quality]
        self.qry_letter_counts_total += 1

    def add_no_mutation(self):
        self.no_mutation += 1


class LocationsWithMutations(object):
    """Read the sam file twice.
    In first iteration save the locations with mutation.
    In second iteration save the locations without mutation for any umi if in this location mutation found for other umi
    This run per chromosome separately and only on segment of the chromosome between chr_start:chr_end.
    All information (of the two iterations) save in locations attribute.

    Args:
        sam_reader_mutation     (SamReader object):
                                    object that read the sam file. Read the sam and save the locations
                                    with mutations in any umi
        sam_reader_no_mutation  (SamReader object):
                                    object that read the sam file. Read the sam and save the locations
                                    without mutations in any umi iff in this location mutation found in other
        chr                     (str): name of the chromosom. For example: chr1
        chr_start               (int): start coordinate on chromosom, run only from this coordinate
        chr_end                 (int): end coordinate on chromosom, run only until this coordinate
        chr_prev_start          (int): start coordinate of the previous segment needed for SamReader
        filter_edge_mutations   (int): ignore this number of bases in each edge of the read
        min_mapq                (int): min map quality. only mutation with higher quality is considered
        bases_distribution      (dict): (optional)
                                    bases distribution in all reads.
                                    In the run the class update this dictinary and print *_bases_distribution.txt file.
                                    Need to supply such dict: {'A':0,'G':0,'C':0,'T':0,'N':0}. For tests you can leave None.
        max_gene_length         (int): needed for SamReader

    Attributes:
        locations               (OrderedDict of int: Location objects):
                                    keys - sorted locations of the mutation on the reference genome.
                                    values - Location object that contain information on the mutations in specific location on the genome
    """

    def __init__(self, sam_reader_mutation, sam_reader_no_mutation, chr, chr_start, chr_end, chr_prev_start,
                 filter_edge_mutations, min_mapq, max_gene_length, bases_distribution=None, max_gb=100000000000000,
                 child_queue=None):
        self.sam_reader_mutation = sam_reader_mutation
        self.sam_reader_no_mutation = sam_reader_no_mutation
        self.chr = chr
        self.chr_start = chr_start
        self.chr_end = chr_end
        self.chr_prev_start = chr_prev_start
        self.filter_edge_mutations = filter_edge_mutations
        self.min_mapq = min_mapq
        self.max_gene_length = max_gene_length
        self.bases_distribution = bases_distribution
        self.locations = {}  # List of lists of Location objects. In function sort_locations we override it with OrderedDict (sorted)
        self.max_gb = max_gb
        self.child_queue = child_queue

    def update_bases_distribution(self, record):
        if SamRecord.is_record_umi_duplication(record):  # Count only one read per UMI
            return
        if self.bases_distribution:  # for the tests - the value in None
            c = Counter(record.seq)
            self.bases_distribution['A'] += c['A']
            self.bases_distribution['G'] += c['G']
            self.bases_distribution['C'] += c['C']
            self.bases_distribution['T'] += c['T']
            self.bases_distribution['N'] += c['N']

    def find_mutations(self, records=None):  # can get list of records for tests
        if not records:
            records = self.sam_reader_mutation.read(self.chr, self.chr_start, self.chr_end, self.chr_prev_start,
                                                    self.min_mapq, self.max_gene_length)
        num_records = 0
        for record in records:
            num_records += 1
            if num_records % 5000 == 0:
                print '%s Num records with mutations is (until now) %s' % (datetime.datetime.now(), num_records)
            limit_memory_usage_gb(self.max_gb, self.child_queue)
            # The function change the content of the record. we don't use with the return value.
            minus_strand = SamRecord.reverse_complement_if_needed(record)
            self.update_bases_distribution(record)
            umi = SamRecord.umi_from_record(record)
            for ref_pos_num, (ref_pos_full_name, qry_pos, ref_letter) in SamRecord.mutation_locations_from_md(record,
                                                                                                              self.filter_edge_mutations).items():
                if ref_pos_num < self.chr_start or ref_pos_num > self.chr_end:  # one part of the mappings of read can be mapped out of our range
                    continue
                mut_letter = record.seq[qry_pos]
                # checking of bugs - this case cannot be occure
                if ref_letter == mut_letter:
                    raise Exception("The reference letter and the mutation is equal %s in record %s" % (
                        ref_letter, record.__dict__))
                if ref_pos_full_name not in self.locations:
                    self.locations[ref_pos_full_name] = Location(ref_pos_num, chr=record.rname, ref_letter=ref_letter)
                if umi not in self.locations[ref_pos_full_name].umis:
                    self.locations[ref_pos_full_name].umis[umi] = UMImutation(umi=umi)
                umi_object = self.locations[ref_pos_full_name].umis[umi]
                if record.pos not in umi_object.fragments:
                    umi_object.fragments[record.pos] = UMIFragMutation(umi=umi, start_loc=record.pos,
                                                                       ref_letter=ref_letter)
                umi_object.update_umi_mutations(record, mut_letter)  # Must to be called BEFORE adding the mutation
                umi_object.fragments[record.pos].add_mutation(mut_letter, record.qual[qry_pos])
                if mut_letter not in self.locations[ref_pos_full_name].all_mutations:
                    self.locations[ref_pos_full_name].all_mutations[mut_letter] = 0
                self.locations[ref_pos_full_name].all_mutations[mut_letter] += 1
        print '%s Num records with mutations is %s' % (datetime.datetime.now(), num_records)
        del records

    def natural_keys(self, text):
        return int(text.split('_')[1])

    def sort_locations(self):
        ordered_locations = OrderedDict()
        for k in sorted(self.locations.keys(), key=self.natural_keys):
            ordered_locations[k] = self.locations[k]
        self.locations = ordered_locations
        del ordered_locations

    # Can run only after sort_locations and the records (or sam file) must to be sorted - run only on positions that exists in self.locations (i.e. only on chr:chr_start-chr_end positions)
    def find_no_mutations(self, records=None):  # can get list of records for tests
        sorted_locations_plus_strand = []
        sorted_locations_minus_strand = []
        sorted_locations = None
        for loc in self.locations:
            if '-minusStrand' in loc:
                sorted_locations_minus_strand.append(self.locations[loc].loc)
            else:
                sorted_locations_plus_strand.append(self.locations[loc].loc)
        if not records:
            records = self.sam_reader_no_mutation.read(self.chr, self.chr_start, self.chr_end, self.chr_prev_start,
                                                       self.min_mapq,
                                                       self.max_gene_length)
        num_records = 0
        for record in records:  # Suppose that sam is sorted - there are overlapping between the reads
            num_records += 1
            if num_records % 5000 == 0:
                print '%s Num records without mutations is (until now) %s' % (datetime.datetime.now(), num_records)
            limit_memory_usage_gb(self.max_gb, self.child_queue)
            minus_strand = SamRecord.reverse_complement_if_needed(record)
            if minus_strand:
                sorted_locations = sorted_locations_minus_strand
            else:
                sorted_locations = sorted_locations_plus_strand

            # print record.rname, chr
            if not sorted_locations:
                continue
            umi = SamRecord.umi_from_record(record)
            mutation_locations_in_record = SamRecord.mutation_locations_from_md(record, self.filter_edge_mutations)
            # Ranges of ref positions of the record. No overlapping between the ranges.
            for start, end in SamRecord.mapped_ref_ranges(record.pos, record.cigar):
                if end < sorted_locations[0] or start > sorted_locations[-1]:
                    continue
                mut_start_idx = bisect.bisect_left(sorted_locations, start - 0.9)
                mut_end_idx = bisect.bisect_left(sorted_locations, end + 0.1) - 1
                # print start, end, sorted_locations[mut_start_idx:mut_end_idx+1], sorted_locations
                for mut_loc in sorted_locations[mut_start_idx:mut_end_idx + 1]:  # locations with mutations
                    # if mut_loc == 47605:
                    #     # print mut_loc, mutation_locations_in_record, record.tags['RX']
                    #     if record.tags['RX'] == 'TATCGTGG':
                    #         print record.__dict__
                    #         print self.locations['chr1_47605'].umis['TATCGTGG'].fragments[47559].frag_type
                    #         # ['EE/AEAA/'].fragments[47500]

                    if mut_loc in mutation_locations_in_record:  # The record also contains mutation, mutation_locations_in_record Includes also N lettets, we through out records with N
                        continue
                    # Must to be loc key with Location value in self.locations
                    full_loc = record.rname + "_" + str(mut_loc)
                    if umi not in self.locations[full_loc].umis:
                        self.locations[full_loc].umis[umi] = UMImutation(umi=umi)
                    umi_object = self.locations[full_loc].umis[umi]
                    if record.pos not in umi_object.fragments:
                        umi_object.fragments[record.pos] = UMIFragMutation(umi=umi, start_loc=record.pos,
                                                                           ref_letter=self.locations[
                                                                               full_loc].ref_letter)
                    umi_object.update_umi_mutations(record)  # Must to be called BEFORE adding the mutation
                    umi_object.fragments[record.pos].add_no_mutation()
                    # print umi_object[record.pos].no_mutation, full_loc
        print '%s Num records without mutations is %s' % (datetime.datetime.now(), num_records)


def run_on_interval(chr, chr_prev_start, chr_start, interval_size, filter_edge_mutations, min_mapq,
                    eb_star_class_threshold,
                    max_gene_length, output_file, sam_reader_mutation, sam_reader_no_mutation, first_iteration,
                    classes_stat, bases_distribution, serial_file_number, max_gb, child_queue):
    chr_end = chr_length if chr_length == chr_start + interval_size else min(chr_length, chr_start + interval_size - 1)
    print '%s start chr number: %s in locations: [%s, %s]' % (datetime.datetime.now(), chr, chr_start, chr_end)
    sys.stdout.flush()
    loc_mutations = LocationsWithMutations(sam_reader_mutation, sam_reader_no_mutation, chr, chr_start, chr_end,
                                           chr_prev_start, filter_edge_mutations, min_mapq, max_gene_length,
                                           bases_distribution, max_gb, child_queue)
    print '%s start find mutataion' % datetime.datetime.now()
    sys.stdout.flush()
    loc_mutations.find_mutations()
    print '%s start sort locations' % datetime.datetime.now()
    sys.stdout.flush()
    loc_mutations.sort_locations()
    print '%s start find no mutations' % datetime.datetime.now()
    sys.stdout.flush()
    loc_mutations.find_no_mutations()
    print '%s start create mutation classification' % datetime.datetime.now()
    sys.stdout.flush()
    classifier_file = MutationClassifier(loc_mutations.locations, chr, chr_start, chr_end, output_file, classes_stat,
                                         first_iteration, eb_star_class_threshold, serial_file_number)
    FILES_TO_REMOVE.append(classifier_file.output_files())
    classifier_file.classify_mutations()
    print '%s start print mutations classification' % datetime.datetime.now()
    sys.stdout.flush()
    classifier_file.print_classes()
    del classifier_file

    # ========================================

    print '%s start create vcf' % datetime.datetime.now()
    sys.stdout.flush()
    vcf_file = CreateVCF(loc_mutations.locations, chr, chr_start, chr_end, output_file, first_iteration, serial_file_number)
    FILES_TO_REMOVE.append(vcf_file.output_files())
    vcf_file.summar_mutations()
    print '%s start print vcf' % datetime.datetime.now()
    sys.stdout.flush()
    vcf_file.print_vcf()
    del vcf_file
    # ==========================================
    del loc_mutations


if __name__ == '__main__':
    # We suppose that input sam file is sorted
    # argv[1] - sam file, argv[2] - distance of the mutation from the edge of the mapping, argv[3] = output file name

    # if os.path.isfile(sys.argv[3]):
    #     ans = query_yes_no('Are you want to delete the file %s ?' % (sys.argv[3]))
    #     if ans:
    #         os.remove(sys.argv[3])
    #     else:
    #         print 'Before running remove the old output file %s' % (sys.argv[3])
    #         exit()

    input_sam_file = sys.argv[1]
    filter_edge_mutations = int(sys.argv[2])
    min_mapq = int(sys.argv[3])
    eb_star_class_threshold = float(sys.argv[4])
    # interval size on the chr. for each interval the script run separately and read all sam file. large interval consume more memory, small interval enlarge the IO time
    interval_size = int(sys.argv[5])
    # for filtering: max size of gap in mapping. the script filter out mapping with longer gap. need to be large than the longest gene in the creature.
    # For efficiency interval_size need not be much bigger than max_gene_length,
    # but max_gene_length can to be much bigger than interval_size but then recommended to find N such as N*interval_size=max_gene_length
    max_gene_length = int(sys.argv[6])
    output_file = sys.argv[7]
    sample_name = sys.argv[8]
    max_gb = float(sys.argv[9])
    minimum_interal = int(sys.argv[10])  # under this interval the program will raise exception

    sam_reader_mutation = SamReader(input_sam_file)
    sam_reader_no_mutation = SamReader(input_sam_file)
    first_iteration = True
    classes_stat = {}  # common to all chromosomes
    manager = Manager()
    bases_distribution = manager.dict({'A': 0, 'G': 0, 'C': 0, 'T': 0, 'N': 0})  # shared memory

    serial_file_number = 0
    for chr, chr_length in sam_reader_mutation.chr_list:
        for chr_start in xrange(0, int(chr_length), interval_size):
            # minus epsilon for the case that max_gene_length and interval_size are equal
            intervals_num = math.floor(float(max_gene_length) / interval_size + 1 - 0.000000001)
            chr_prev_start = int(max(0, chr_start - intervals_num * interval_size))

            serial_file_number_try = 0
            sub_interval_size = interval_size
            iteration = 1
            child_queue = Queue()
            while True:
                FILES_TO_REMOVE = []
                serial_file_number_try = 0
                sub_interval_size = int(math.floor(float(interval_size) / iteration))
                failed = False
                iteration_number = int(math.log(iteration, 2) + 1)
                print '%s Trying run number (before memory failed): %s' % (datetime.datetime.now(), iteration_number)
                for sub_chr_start in xrange(chr_start, chr_start + interval_size, sub_interval_size):
                    if sub_chr_start + sub_interval_size > chr_start + interval_size:  # handle in last sub interval
                        sub_interval_size = chr_start + interval_size - sub_chr_start

                    if sub_interval_size < minimum_interal:
                        error_message = '%s The interval %s-%s contains many reads and consume a lot of memory. You need to enlarge the amount of memory allocation' % (
                            datetime.datetime.now(), sub_chr_start, int(sub_chr_start + sub_interval_size))
                        print error_message
                        raise Exception(error_message)

                    print '%s Memory usage (gb) before process: %s' % (
                    datetime.datetime.now(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1e-6)
                    serial_file_number += 1
                    serial_file_number_try += 1
                    p = Process(target=run_on_interval, args=(chr, chr_prev_start, sub_chr_start, sub_interval_size,
                                                              filter_edge_mutations, min_mapq,
                                                              eb_star_class_threshold, max_gene_length, output_file,
                                                              sam_reader_mutation, sam_reader_no_mutation,
                                                              first_iteration, classes_stat, bases_distribution,
                                                              serial_file_number, max_gb, child_queue))
                    p.start()
                    p.join()
                    print '%s Memory usage (gb) after process: %s' % (
                    datetime.datetime.now(), resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * 1e-6)
                    if not child_queue.empty() and child_queue.get_nowait() == 'MemoryError':
                        failed = True
                        serial_file_number -= serial_file_number_try
                        iteration *= 2
                        gc.collect()
                        for file_to_remove in FILES_TO_REMOVE:
                            if os.path.exists(file_to_remove):
                                os.remove(file_to_remove)
                            FILES_TO_REMOVE = []
                        break
                if not failed:
                    first_iteration = False
                    break

    sam_reader_mutation.close_file()
    sam_reader_no_mutation.close_file()

    with open(output_file + '_bases_distribution.txt', 'w') as df:
        df.writelines('Base\tCount\n')
        for base, count in bases_distribution.items():
            df.writelines('%s\t%s\n' % (base, count))

    print '%s start concatenate classification output files' % datetime.datetime.now()
    sys.stdout.flush()
    MutationClassifier.cat_classifications_files(output_file)
    MutationClassifier.print_mute_type_stat(sample_name, output_file, classes_stat, norm=False)

    # MutationClassifier.print_mute_type_stat(sample_name, output_file, norm=True)
    CreateVCF.cat_vcf_files(output_file)
    print '%s Run is ended' % datetime.datetime.now()
    sys.stdout.flush()
