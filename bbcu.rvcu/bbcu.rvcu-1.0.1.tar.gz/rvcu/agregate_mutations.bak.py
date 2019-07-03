import bisect
import datetime
import sys
from collections import OrderedDict ,Counter

from create_vcf import CreateVCF, MutationClassifier
from sam_record import SamRecord, SamReader
"""
samtools view -F 1024 {input} | grep -v RX:Z:[ACTG]*N[ACTGN]*

self.locations = sorted OrderedDict.
    keys: location numbers
    values: Location object
        loc (int)
        ref_letter (char)
        all_mutations (list)
        umis: dict
            keys: umi
            values: UMImutation
                umi (string)
                mutations_all_positions_pure: dict:
                    keys: mutation
                    values: counts mutations on all positions
                no_mutations_all_positions_pure (int)
                position: dict:
                    keys: mapping start
                    values: UMIPositionMutation object
"""



class Location(object):
    def __init__(self, loc, chr,
                 ref_letter):  # loc is location number without chr number (in order to facilitate the access to this number
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
    def __init__(self, umi):
        self.umi = umi
        self.mut_pure_pos = {}  # keys: mutation type, values: [num pure positions (contain only this mutation/s), total counts of reads over all pos]
        self.mut_dirty_total_per_mutation = {} # for each mutation, how much reads there is in total over all dirty positions. non-mutations signed by 'None' key
        self.total_per_mutation = {} # for each mutation, how much reads there is in total over all (dirty and pure) positions.
        self.mut_dirty_positions = {} # keys: dirty positions, values: None. For sorting the umis
        self.mut_dirty_total = 0
        self.non_mutation_total = 0 #all non mutations on all positions
        self.total_reads = 0
        self.positions_number = 0
        self.positions = {}  # key: start position of the read, value: UMIPositionMutation

    # Must run before add_mutation or add_no_mutation of UMIPositionMutation object
    def update_umi_mutations(self, record, mut_letter=None):  # mut_letter=None if updating record without mutation
        # This step all positions are pure (meantime we have no non-mutations reads) unless position contains more than one mutation type
        # add if not exists
        pos = record.pos
        self.total_reads += 1
        if mut_letter:
            if mut_letter not in self.total_per_mutation:
                self.total_per_mutation[mut_letter] = 0
            self.total_per_mutation[mut_letter] += 1
        else:
            self.non_mutation_total += 1
        if self.positions[pos].pos_type == 0:  # A new pure position
            self.positions_number += 1
            if mut_letter:
                self.positions[pos].pos_type = 1  # Pure position
                if mut_letter not in self.mut_pure_pos:
                    self.mut_pure_pos[mut_letter] = [0, 0]
                self.mut_pure_pos[mut_letter][0] += 1
                self.mut_pure_pos[mut_letter][1] += 1
            else:  # Record without mutation
                self.positions[pos].pos_type = 2  # Dirty position
                self.mut_dirty_positions[pos] = None
                if mut_letter not in self.mut_dirty_total_per_mutation:
                    self.mut_dirty_total_per_mutation[mut_letter] = 0
                self.mut_dirty_total_per_mutation[mut_letter] += 1
                self.mut_dirty_total += 1
        elif self.positions[pos].pos_type == 1:  # An old pure position
            old_mutation = self.positions[pos].qry_letter_counts.keys()[0]
            if mut_letter == old_mutation:  # Only one mutaion because pos_type is 1
                self.mut_pure_pos[mut_letter][1] += 1  # This pos already exists in mut_pure_pos
            else:  # The new mutation differ than old mutation OR mut_letter is None (record without mutation)
                self.positions[pos].pos_type = 2
                self.mut_dirty_positions[pos] = None
                #add this position to dirty 
                if mut_letter not in self.mut_dirty_total_per_mutation:
                    self.mut_dirty_total_per_mutation[mut_letter] = 0
                if old_mutation not in self.mut_dirty_total_per_mutation:
                    self.mut_dirty_total_per_mutation[old_mutation] = 0
                #for each mutation the dirty is the counts of the other different mutations
                self.mut_dirty_total_per_mutation[old_mutation] += self.positions[pos].qry_letter_counts[old_mutation]
                self.mut_dirty_total_per_mutation[mut_letter] += 1 #add current record
                self.mut_dirty_total += self.positions[pos].qry_letter_counts[old_mutation] + 1

                # Remove this position form pure positions of the old_mutation
                self.mut_pure_pos[old_mutation][0] -= 1
                self.mut_pure_pos[old_mutation][1] -= self.positions[pos].qry_letter_counts[old_mutation]
                if self.mut_pure_pos[old_mutation][0] == 0: # No remained positions
                    del self.mut_pure_pos[old_mutation]
        elif self.positions[pos].pos_type == 2:  # An old dirty position
            if mut_letter not in self.mut_dirty_total_per_mutation:
                self.mut_dirty_total_per_mutation[mut_letter] = 0
            self.mut_dirty_total_per_mutation[mut_letter] += 1
            self.mut_dirty_total += 1


class UMIPositionMutation(object):
    def __init__(self, umi, start_loc, ref_letter):
        self.umi = umi
        self.start_loc = start_loc
        self.ref_letter = ref_letter
        self.qry_letter_counts_total = 0  # count of all mutations
        self.no_mutation = 0
        self.qry_letter_counts = {}
        self.quality = {}
        self.pos_type = 0  # 0-initialization, 1-pure with one mutation, 2-dirty with more than one mutation

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
    def __init__(self, sam_reader_mutation, sam_reader_no_mutation, chr, filter_edge_mutations, min_mapq, bases_distribution=None):
        self.sam_reader_mutation = sam_reader_mutation
        self.sam_reader_no_mutation = sam_reader_no_mutation
        self.chr = chr
        self.filter_edge_mutations = filter_edge_mutations
        self.min_mapq = min_mapq
        self.bases_distribution = bases_distribution
        self.locations = {}  # List of lists of UMIPositionMutation

    def update_bases_distribution(self, record):
        if SamRecord.is_record_umi_duplication(record): # Count only one read per UMI
            return
        if self.bases_distribution:#for the tests - the value in None
            c = Counter(record.seq)
            self.bases_distribution['A'] += c['A']
            self.bases_distribution['G'] += c['G']
            self.bases_distribution['C'] += c['C']
            self.bases_distribution['T'] += c['T']
            self.bases_distribution['N'] += c['N']
        
    def find_mutations(self, records=None):  # can get list of records for tests
        if not records:
            records = self.sam_reader_mutation.read(self.chr)
        for record in records:
            if not record:
                break
            minus_strand = SamRecord.reverse_complement_if_needed(record)

            umi = SamRecord.umi_from_record(record)
            if SamRecord.filter_record(record, umi, self.min_mapq):
                continue
            self.update_bases_distribution(record)
            for ref_pos_num, (ref_pos_full_name, qry_pos, ref_letter) in SamRecord.mutation_locations_from_md(record,
                                                                                                          self.filter_edge_mutations).items():
                mut_letter = record.seq[qry_pos]
                #checking of bugs - this case cannot be occure
                if ref_letter == mut_letter:
                    raise Exception("The reference letter and the mutation is equal %s in record %s" %(ref_letter, record.__dict__))
                if ref_pos_full_name not in self.locations:
                    self.locations[ref_pos_full_name] = Location(ref_pos_num, chr=record.rname ,ref_letter=ref_letter)
                if umi not in self.locations[ref_pos_full_name].umis:
                    self.locations[ref_pos_full_name].umis[umi] = UMImutation(umi=umi)
                umi_object = self.locations[ref_pos_full_name].umis[umi]
                if record.pos not in umi_object.positions:
                    umi_object.positions[record.pos] = UMIPositionMutation(umi=umi, start_loc=record.pos,
                                                                           ref_letter=ref_letter)
                umi_object.update_umi_mutations(record, mut_letter)  # Must to be called BEFORE adding the mutation
                umi_object.positions[record.pos].add_mutation(mut_letter, record.qual[qry_pos])
                if mut_letter not in self.locations[ref_pos_full_name].all_mutations:
                    self.locations[ref_pos_full_name].all_mutations[mut_letter] = 0
                self.locations[ref_pos_full_name].all_mutations[mut_letter] += 1

    def natural_keys(self, text):
        return int(text.split('_')[1])

    def sort_locations(self):
        ordered_locations = OrderedDict()
        for k in sorted(self.locations.keys(), key=self.natural_keys):
            ordered_locations[k] = self.locations[k]
        self.locations = ordered_locations

    # Can run only after sort_locations and the records (or sam file) must to be sorted
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
            records = self.sam_reader_no_mutation.read(self.chr)
        for record in records:  # Suppose that sam is sorted - there are overlapping between the reads
            if not record:
                break
            minus_strand = SamRecord.reverse_complement_if_needed(record)
            if minus_strand:
                sorted_locations = sorted_locations_minus_strand
            else:
                sorted_locations = sorted_locations_plus_strand

            # print record.rname, chr
            if not sorted_locations:
                continue
            umi = SamRecord.umi_from_record(record)
            if SamRecord.filter_record(record, umi, self.min_mapq):
                continue

            mutation_locations_in_record = SamRecord.mutation_locations_from_md(record, self.filter_edge_mutations)
            # Ranges of ref positions of the record. No overlapping between the ranges
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
                    #         print self.locations['chr1_47605'].umis['TATCGTGG'].positions[47559].pos_type
                    #         # ['EE/AEAA/'].positions[47500]



                    if mut_loc in mutation_locations_in_record:  # The record also contains mutation, mutation_locations_in_record Includes also N lettets, we through out records with N
                        continue
                    # Must to be loc key with Location value in self.locations
                    full_loc = record.rname + "_" + str(mut_loc)
                    if umi not in self.locations[full_loc].umis:
                        self.locations[full_loc].umis[umi] = UMImutation(umi=umi)
                    umi_object = self.locations[full_loc].umis[umi]
                    if record.pos not in umi_object.positions:
                        umi_object.positions[record.pos] = UMIPositionMutation(umi=umi, start_loc=record.pos,
                                                                               ref_letter=self.locations[
                                                                                   full_loc].ref_letter)
                    umi_object.update_umi_mutations(record)  # Must to be called BEFORE adding the mutation
                    umi_object.positions[record.pos].add_no_mutation()
                    # print umi_object[record.pos].no_mutation, full_loc


if __name__ == '__main__':
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
    eb_star_class_threshold = float(4)
    output_file = sys.argv[5]
    sample_name = sys.argv[6]

    sam_reader_mutation = SamReader(input_sam_file)
    sam_reader_no_mutation = SamReader(input_sam_file)
    first_chr = True
    mut_type_stat = {'ABC_EB-star_mut_types':{}} #common to all chromosomes
    mut_type_stat_normalized = {'ABC_EB-star_mut_types':{}} #common to all chromosomes
    bases_distribution = {'A':0,'G':0,'C':0,'T':0,'N':0}
    for chr in sam_reader_mutation.chr_list:
        print 'start chr number: ' + chr, sam_reader_mutation.chr_list
        sys.stdout.flush()
        loc_mutations = LocationsWithMutations(sam_reader_mutation, sam_reader_no_mutation, chr, filter_edge_mutations, min_mapq, bases_distribution)
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
        classifier_file = MutationClassifier(loc_mutations.locations, chr, output_file, mut_type_stat, mut_type_stat_normalized, first_chr, eb_star_class_threshold)
        classifier_file.classify_mutations()
        print '%s start print mutations classification' % datetime.datetime.now()
        sys.stdout.flush()
        classifier_file.print_classes()
        del classifier_file
        del loc_mutations
        # print '%s start create vcf' % datetime.datetime.now()
        # sys.stdout.flush()
        # vcf_file = CreateVCF(loc_mutations.locations, chr, output_file, first_chr)
        # vcf_file.summar_mutations()
        # print '%s start print vcf' % datetime.datetime.now()
        # sys.stdout.flush()
        # vcf_file.print_vcf()
        # del vcf_file
        first_chr = False

    sam_reader_mutation.close_file()
    sam_reader_no_mutation.close_file()
    with open(output_file + '_bases_distribution.txt', 'w') as df:
        df.writelines('Base\tCount\n')
        for base, count in bases_distribution.items():
            df.writelines('%s\t%s\n' %(base, count))

    print '%s start concatenate classification output files' % datetime.datetime.now()
    sys.stdout.flush()
    MutationClassifier(None, None, '', None, None, None, None).cat_classifications_files(output_file)
    MutationClassifier(None, None, '', None, None, None, None).print_mute_type_stat(sample_name, output_file, mut_type_stat, norm=False)
    # MutationClassifier(None, None, '', None, None, None).print_mute_type_stat(sample_name, output_file, mut_type_stat_normalized, norm=True)
    # CreateVCF(None, None, None, None).cat_vcf_files(output_file)
    print '%s Run is ended' % datetime.datetime.now()
    sys.stdout.flush()

