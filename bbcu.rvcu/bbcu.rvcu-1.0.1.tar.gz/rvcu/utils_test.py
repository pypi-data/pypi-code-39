import unittest

from nose.plugins.attrib import attr

from agregate_mutations import LocationsWithMutations, Location, UMIFragMutation, UMImutation
from sam_record import SamRecord


@attr(test_type='unit')
class ReadBarcodeFileTest(unittest.TestCase):
    def setUp(self):
        # Last parmeter is 0 - The mutation can to be located in the last location of the mapping
        self.expected_loc_mutations = LocationsWithMutations(sam_reader_mutation=None, sam_reader_no_mutation=None, chr='chr1', chr_start=0, chr_end=10000, chr_prev_start=0, filter_edge_mutations=0, min_mapq=0, max_gene_length=10000, bases_distribution=None)
        self.loc_mutations = LocationsWithMutations(sam_reader_mutation=None, sam_reader_no_mutation=None, chr='chr1', chr_start=0, chr_end=10000, chr_prev_start=0, filter_edge_mutations=0, min_mapq=0, max_gene_length=10000, bases_distribution=None)
        # self.dirpath = tempfile.mkdtemp()
        # _, self.bam_output_file = tempfile.mkstemp(prefix='output', suffix='.bam', dir=self.dirpath)

    def tearDown(self):
        pass

    # Mapping can get values [5..10], The ref letter is G, mut can get [ACT]* value
    def buildSamRecordsMutationInChr1_10(self, rc, copies_num, umi, mapping, mut=''):
        records = []

        flag = 255 if rc else 239
        if mapping < 5 or mapping > 10:
            raise Exception(
                "The read (length 6) don't overlap with the mutation location of the ref genome (location 10). Select mapping value between [5..10].")
        if not mut:
            md_field = 6
            seq = 'TTTTTT'
        else:
            s_match = 10 - mapping
            e_match = 5 - s_match
            md_field = (str(s_match) if s_match else '') + 'G' + (str(e_match) if e_match else '')
            seq = (s_match * 'T' if s_match else '') + mut + (e_match * 'T' if e_match else '')
        for i in xrange(copies_num):
            qname = 'READ:%s:%s:%s:%s' %(i, umi, mapping, flag)
            record = '%s %s chr1 %s 255 6M * 0 0 %s ZZZZZZ' % (qname, flag, mapping, seq)
            records.append(SamRecord(*record.split(), tags=['MD:Z:%s' % md_field, 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:%s' % umi]))
        return records

    def compare_locations(self):
        output_locations = self.loc_mutations.locations
        self.assertEqual(output_locations.keys(), self.expected_loc_mutations.locations.keys())
        for loc in self.expected_loc_mutations.locations:
            self.assertEqual(output_locations[loc].all_mutations, self.expected_loc_mutations.locations[loc].all_mutations)
            self.assertEqual(output_locations[loc].chr, self.expected_loc_mutations.locations[loc].chr)
            self.assertEqual(output_locations[loc].loc, self.expected_loc_mutations.locations[loc].loc)
            self.assertEqual(output_locations[loc].umis.keys(), self.expected_loc_mutations.locations[loc].umis.keys())
            for umi in self.expected_loc_mutations.locations[loc].umis:
                self.assertEqual(output_locations[loc].umis[umi].pure_fragments_per_mut,
                                 self.expected_loc_mutations.locations[loc].umis[umi].pure_fragments_per_mut)
                self.assertEqual(output_locations[loc].umis[umi].total_reads,
                                 self.expected_loc_mutations.locations[loc].umis[umi].total_reads)
                self.assertEqual(output_locations[loc].umis[umi].mutated_reads_num_per_mut,
                                 self.expected_loc_mutations.locations[loc].umis[umi].mutated_reads_num_per_mut)
                self.assertEqual(output_locations[loc].umis[umi].dirty_fragments,
                                 self.expected_loc_mutations.locations[loc].umis[umi].dirty_fragments)
                # self.assertEqual(output_locations[loc].umis[umi].mut_dirty_total_per_mutation, TODO: Not in using. remove it
                #                  self.expected_loc_mutations.locations[loc].umis[umi].mut_dirty_total_per_mutation) TODO: Not in using. remove it
                # self.assertEqual(output_locations[loc].umis[umi].total_reads_dirty, TODO: Not in using. remove it
                #                  self.expected_loc_mutations.locations[loc].umis[umi].total_reads_dirty) TODO: Not in using. remove it
                self.assertEqual(output_locations[loc].umis[umi].fragments.keys(),
                                 self.expected_loc_mutations.locations[loc].umis[umi].fragments.keys())
                for map_position in self.expected_loc_mutations.locations[loc].umis[umi].fragments:
                    out_map_pos = output_locations[loc].umis[umi].fragments[map_position]
                    true_map_pos = self.expected_loc_mutations.locations[loc].umis[umi].fragments[map_position]
                    self.assertEqual(out_map_pos.__dict__, true_map_pos.__dict__)

    # set mutation for specific location, umi, and mapping start
    # frag_type is 1 for pure, 2 for dirty.
    def set_test_mutation(self, location, umi, mapping, ref_letter, qry_counts, qry_counts_total, quality, frag_type,
                          no_mutation=0):
        ref_position_num = int(location.split("_")[1])
        mutation = UMIFragMutation(umi, mapping, ref_letter=ref_letter)
        mutation.no_mutation = no_mutation
        mutation.qry_letter_counts = qry_counts
        mutation.qry_letter_counts_total = qry_counts_total
        mutation.quality = quality
        mutation.frag_type = frag_type
        if location not in self.expected_loc_mutations.locations:
            self.expected_loc_mutations.locations[location] = Location(loc=ref_position_num, chr='chr1', ref_letter=ref_letter)
        if umi not in self.expected_loc_mutations.locations[location].umis:
            self.expected_loc_mutations.locations[location].umis[umi] = UMImutation(umi=umi)
        self.expected_loc_mutations.locations[location].umis[umi].fragments.update({mapping: mutation})

        # update sum of fragments
        self.expected_loc_mutations.locations[location].umis[umi].umi = umi
        for mutation in qry_counts:
            self.expected_loc_mutations.locations[location].umis[umi].total_reads += qry_counts[mutation]
        self.expected_loc_mutations.locations[location].umis[umi].total_reads += no_mutation

        if frag_type == 1:  # No mutation must be 0, must to be only one mutation
            mute = qry_counts.keys()[0]  # there is only one mutation in this position
            if mute not in self.expected_loc_mutations.locations[location].umis[umi].mutated_reads_num_per_mut:
                self.expected_loc_mutations.locations[location].umis[umi].mutated_reads_num_per_mut[mute] = 0
            self.expected_loc_mutations.locations[location].umis[umi].mutated_reads_num_per_mut[mute] += qry_counts[mute]
            if mute not in self.expected_loc_mutations.locations[location].umis[umi].pure_fragments_per_mut:
                self.expected_loc_mutations.locations[location].umis[umi].pure_fragments_per_mut[mute] = [0, 0]
            self.expected_loc_mutations.locations[location].umis[umi].pure_fragments_per_mut[mute][0] += 1
            self.expected_loc_mutations.locations[location].umis[umi].pure_fragments_per_mut[mute][1] += qry_counts[mute]
        elif frag_type == 2:
            self.expected_loc_mutations.locations[location].umis[umi].dirty_fragments[mapping] = None
            for mute in qry_counts:
                if mute not in self.expected_loc_mutations.locations[location].umis[umi].mutated_reads_num_per_mut:
                    self.expected_loc_mutations.locations[location].umis[umi].mutated_reads_num_per_mut[mute] = 0
                self.expected_loc_mutations.locations[location].umis[umi].mutated_reads_num_per_mut[mute] += qry_counts[mute]
                # self.expected_loc_mutations.locations[location].umis[umi].total_reads_dirty += qry_counts[mute] TODO: Not in using. remove it
                # if not mute in self.expected_loc_mutations.locations[location].umis[umi].mut_dirty_total_per_mutation: TODO: Not in using. remove it
                #     self.expected_loc_mutations.locations[location].umis[umi].mut_dirty_total_per_mutation[mute] = 0 TODO: Not in using. remove it
                # self.expected_loc_mutations.locations[location].umis[umi].mut_dirty_total_per_mutation[mute] += qry_counts[
                #     mute] TODO: Not in using. remove it
            if no_mutation:
                # self.expected_loc_mutations.locations[location].umis[umi].total_reads_dirty += no_mutation TODO: Not in using. remove it
                # if None not in self.expected_loc_mutations.locations[location].umis[umi].mut_dirty_total_per_mutation: TODO: Not in using. remove it
                #     self.expected_loc_mutations.locations[location].umis[umi].mut_dirty_total_per_mutation[None] = 0 TODO: Not in using. remove it
                # self.expected_loc_mutations.locations[location].umis[umi].mut_dirty_total_per_mutation[None] += no_mutation TODO: Not in using. remove it
                pass

        for mut in qry_counts:
            if mut not in self.expected_loc_mutations.locations[location].all_mutations:
                self.expected_loc_mutations.locations[location].all_mutations[mut] = 0
            self.expected_loc_mutations.locations[location].all_mutations[mut] += qry_counts[mut]


