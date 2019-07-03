# TODO: Tests that need to check:
# max_mutation_rate_umi (creteria changed in this version. need to repair  the tests)
# mutation_stat_on_max_umi (how worked on wrong previous version ? )
# mutation_stat_on_other_umis
import math
import os
import unittest

from agregate_mutations import LocationsWithMutations
from create_vcf import CreateVCF, MutationClassifier
from sam_record import SamReader
from sam_record import SamRecord
from utils_test import ReadBarcodeFileTest


class refMutationFromMdTest(ReadBarcodeFileTest):
    def test_1(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1001', umi='CCTCTTGA', mapping=1000, ref_letter='C', qry_counts={'G': 1},
                               qry_counts_total=1, quality={'G': ['B']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_1b(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 12M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:0N0N0N2T6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1005', umi='CCTCTTGA', mapping=1000, ref_letter='T', qry_counts={'G': 1},
                               qry_counts_total=1, quality={'G': ['F']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_2(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:2T9', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1002', umi='CCTCTTGA', mapping=1000, ref_letter='T', qry_counts={'C': 1},
                               qry_counts_total=1, quality={'C': ['C']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_3(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:3G8', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1503', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'T': 1},
                               qry_counts_total=1, quality={'T': ['D']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_4(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:4C8', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1504', umi='CCTCTTGA', mapping=1000, ref_letter='C', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['E']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_5(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:5C8', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1505', umi='CCTCTTGA', mapping=1000, ref_letter='C', qry_counts={'G': 1},
                               qry_counts_total=1, quality={'G': ['F']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_6(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:11C', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1511', umi='CCTCTTGA', mapping=1000, ref_letter='C', qry_counts={'T': 1},
                               qry_counts_total=1, quality={'T': ['L']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_7(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1000', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['A']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_8(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AACTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:GG10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1000', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['A']}, frag_type=1)
        self.set_test_mutation(location='chr1_1001', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['B']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_9(self):
        record = SamRecord(
            *'NB1__QX: 239 chr1 1000 255 5M500N7M * 0 0 AGCTGCCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:4AG6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1004', umi='CCTCTTGA', mapping=1000, ref_letter='A', qry_counts={'G': 1},
                               qry_counts_total=1, quality={'G': ['E']}, frag_type=1)
        self.set_test_mutation(location='chr1_1505', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'C': 1},
                               qry_counts_total=1, quality={'C': ['F']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_10(self):
        record = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G3T6C', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.set_test_mutation(location='chr1_1000', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['A']}, frag_type=1)
        self.set_test_mutation(location='chr1_1504', umi='CCTCTTGA', mapping=1000, ref_letter='T', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['E']}, frag_type=1)
        self.set_test_mutation(location='chr1_1511', umi='CCTCTTGA', mapping=1000, ref_letter='C', qry_counts={'T': 1},
                               qry_counts_total=1, quality={'T': ['L']}, frag_type=1)
        self.loc_mutations.find_mutations([record])
        self.compare_locations()

    def test_11(self):
        record1 = SamRecord(
            *'NB8585__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record2 = SamRecord(
            *'NB8586__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT SBCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record3 = SamRecord(
            *'NB8586__QX: 239 chr1 1000 255 3M500N9M * 0 0 TGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record4 = SamRecord(
            *'NB8585__QX: 239 chr1 1500 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record5 = SamRecord(
            *'NB8585__QX: 239 chr1 1500 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGG'])
        record6 = SamRecord(
            *'NB8585__QX: 239 chr1 1500 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:12', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGG'])
        self.set_test_mutation(location='chr1_1000', umi='CCTCTTGA', mapping=1000, ref_letter='G',
                               qry_counts={'A': 2, 'T': 1}, qry_counts_total=3, quality={'A': ['A', 'S'], 'T': ['A']},
                               frag_type=2)
        self.set_test_mutation(location='chr1_1500', umi='CCTCTTGA', mapping=1500, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['A']}, frag_type=1)
        self.set_test_mutation(location='chr1_1500', umi='CCTCTTGG', mapping=1500, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['A']}, frag_type=1)

        self.loc_mutations.find_mutations([record1, record2, record3, record4, record5, record6])
        self.compare_locations()


class mappedRefRanges(ReadBarcodeFileTest):
    def test_12(self):
        self.assertEqual(SamRecord.mapped_ref_ranges(1000, '3M500N9M'), [[1000, 1002], [1503, 1511]])


class FindNoMutationsTest(ReadBarcodeFileTest):
    def setUp(self):
        super(FindNoMutationsTest, self).setUp()
        # The following records have mutations
        # location of mutation: 1000
        record1mut = SamRecord(
            *'NB1__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        # location of mutation: 1000
        record2mut = SamRecord(
            *'NB2__QX: 239 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT SBCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        # location of mutation: 1000
        record3mut = SamRecord(
            *'NB3__QX: 239 chr1 1000 255 3M500N9M * 0 0 TGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        # location of mutation: 2004, no mutation in 1500
        record4mut = SamRecord(
            *'NB4__QX: 239 chr1 1500 255 3M500N9M * 0 0 GGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:4G7', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        # location of mutation: 1500, no mutation in 2004
        record5mut = SamRecord(
            *'NB5__QX: 239 chr1 1500 255 3M500N9M * 0 0 AGCTGGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G11', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGG'])
        # location of mutation: 1500 and 2004
        record6mut = SamRecord(
            *'NB5__QX: 239 chr1 1500 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:G3G7', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGG'])

        # The following records have not mutations
        # same location, umi, mapping
        record1nomut = SamRecord(
            *'NB6nomut__QX: 239 chr1 1000 255 3M500N9M * 0 0 GGCTAGCTAGCT LABCDEFGHIJK'.split(),
            tags=['MD:Z:12', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        # same location, umi, not mapping
        record2nomut = SamRecord(
            *'NB7nomut__QX: 239 chr1 999 255 3M500N9M * 0 0 TGGCTAGCTAGC LABCDEFGHIJK'.split(),
            tags=['MD:Z:12', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        # same location, not umi
        record3nomut = SamRecord(
            *'NB7nomut__QX: 239 chr1 1000 255 3M500N9M * 0 0 TGGCTAGCTAGC LABCDEFGHIJK'.split(),
            tags=['MD:Z:12', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGG'])
        # different location - don't save because it is not on mutation point
        record4nomut = SamRecord(
            *'NB7nomut__QX: 239 chr1 5000 255 3M500N9M * 0 0 TGGCTAGCTAGC LABCDEFGHIJK'.split(),
            tags=['MD:Z:12', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGG'])

        self.set_test_mutation(location='chr1_1000', umi='CCTCTTGA', mapping=1000, ref_letter='G',
                               qry_counts={'A': 2, 'T': 1}, qry_counts_total=3, quality={'A': ['A', 'S'], 'T': ['A']},
                               frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1000', umi='CCTCTTGA', mapping=999, ref_letter='G', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1000', umi='CCTCTTGG', mapping=1000, ref_letter='G', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_2004', umi='CCTCTTGA', mapping=1500, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['E']}, frag_type=1)
        self.set_test_mutation(location='chr1_2004', umi='CCTCTTGG', mapping=1500, ref_letter='G', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['E']}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1500', umi='CCTCTTGG', mapping=1500, ref_letter='G', qry_counts={'A': 2},
                               qry_counts_total=2, quality={'A': ['A', 'A']}, frag_type=1)
        self.set_test_mutation(location='chr1_1500', umi='CCTCTTGA', mapping=1500, ref_letter='G', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)

        self.loc_mutations.find_mutations(
            [record1mut, record2mut, record3mut, record4mut, record5mut, record6mut, record1nomut, record2nomut,
             record3nomut, record4nomut])
        self.loc_mutations.sort_locations()
        self.loc_mutations.find_no_mutations(
            [record1mut, record2mut, record3mut, record4mut, record5mut, record6mut, record1nomut, record2nomut,
             record3nomut, record4nomut])
        self.expected_loc_mutations.sort_locations()

    # Checking the find_no_mutation procedure
    def test_13(self):
        self.compare_locations()


class IntersectionNomutationWithMutationTest(ReadBarcodeFileTest):
    def setUp(self):
        super(IntersectionNomutationWithMutationTest, self).setUp()
        """
        reference position: 1000 1001 1002 1003 1004 <--500 skip--->1505 1506 <--20 skip --->1527 1528 1259 1530 1531 1532 1533 1534 1535 1536 1537 1538 <-2 skip->1541 1542 1543 ....
                            |----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
        reference sequence: A    G    C    T    A                   G    C                   T    A    G    C    T    A    G    C    T    A    G    C              T    A    G
        Query1 mutations:        C              G                   C                             G              A         C                                       A
        Query1 quality:          B              E                   F                             I              L         B                                       H
        Query1 location:    1    2    3    4    5                   6    7                   8    9    10   11   12   13   14   15   16   17   18   19             20    21  22 ...............

        Query1 no mutation: |----|----|----|----|                   |-|
        Query2 no mutation: |----|----|----|----|                   |-|
        Query3 no mutation:                |----|                   |----|                   |----|
        Query4 no mutation:                                         |----|                   |----|----|----|
        Query5 no mutation:                                                                                      |----|----|----|----|----|
        Query6 no mutation:                                                                                           |----|----|----|----|----|
        Query7 no mutation:                                                                                                               |----|----|----|         |----|----|
        """

        # The following records have mutations
        # location of mutation: 1000
        self.record1mut = SamRecord(
            *'NB1__QX: 239 chr1 1000 255 5M500N2M20N12M2N17M * 0 0 ACCTGCCTGGCAACCTAGCAAGCTAGCTAGCTAGCT ABCDEFGHIJKLABCDEFGHIJKLABCDEFGHIJKL'.split(),
            tags=['MD:Z:1G2AG2A2T1G5T16', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])

        # The following records have not mutations
        self.record1nomut = SamRecord(
            *'NB1__QX: 239 chr1 1000 255 5M500N1M * 0 0 AGCTAG ABCDEF'.split(),
            tags=['MD:Z:6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.record2nomut = SamRecord(
            *'NB2__QX: 239 chr1 1000 255 5M500N1M * 0 0 AGCTAG ABCDEF'.split(),
            tags=['MD:Z:6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.record3nomut = SamRecord(
            *'NB3__QX: 239 chr1 1003 255 2M500N2M20N2M * 0 0 AGCTAG ABCDEF'.split(),
            tags=['MD:Z:6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.record4nomut = SamRecord(
            *'NB4__QX: 239 chr1 1505 255 2M20N4M * 0 0 AGCTAG ABCDEF'.split(),
            tags=['MD:Z:6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.record5nomut = SamRecord(
            *'NB5__QX: 239 chr1 1531 255 6M * 0 0 AGCTAG ABCDEF'.split(),
            tags=['MD:Z:6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.record6nomut = SamRecord(
            *'NB6__QX: 239 chr1 1532 255 6M * 0 0 AGCTAG ABCDEF'.split(),
            tags=['MD:Z:6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        self.record7nomut = SamRecord(
            *'NB7__QX: 239 chr1 1536 255 3M2N3M * 0 0 AGCTAG ABCDEF'.split(),
            tags=['MD:Z:6', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])

        # update self.expected_loc_mutations
        self.set_test_mutation(location='chr1_1001', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'C': 1},
                               qry_counts_total=1, quality={'C': ['B']}, frag_type=2, no_mutation=2)
        self.set_test_mutation(location='chr1_1004', umi='CCTCTTGA', mapping=1000, ref_letter='A', qry_counts={'G': 1},
                               qry_counts_total=1, quality={'G': ['E']}, frag_type=2, no_mutation=2)
        self.set_test_mutation(location='chr1_1505', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'C': 1},
                               qry_counts_total=1, quality={'C': ['F']}, frag_type=2, no_mutation=2)
        self.set_test_mutation(location='chr1_1528', umi='CCTCTTGA', mapping=1000, ref_letter='A', qry_counts={'G': 1},
                               qry_counts_total=1, quality={'G': ['I']}, frag_type=1)
        self.set_test_mutation(location='chr1_1531', umi='CCTCTTGA', mapping=1000, ref_letter='T', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['L']}, frag_type=1)
        self.set_test_mutation(location='chr1_1533', umi='CCTCTTGA', mapping=1000, ref_letter='G', qry_counts={'C': 1},
                               qry_counts_total=1, quality={'C': ['B']}, frag_type=1)
        self.set_test_mutation(location='chr1_1541', umi='CCTCTTGA', mapping=1000, ref_letter='T', qry_counts={'A': 1},
                               qry_counts_total=1, quality={'A': ['H']}, frag_type=1)
        self.set_test_mutation(location='chr1_1004', umi='CCTCTTGA', mapping=1003, ref_letter='A', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1505', umi='CCTCTTGA', mapping=1003, ref_letter='G', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1528', umi='CCTCTTGA', mapping=1003, ref_letter='A', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1505', umi='CCTCTTGA', mapping=1505, ref_letter='G', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1528', umi='CCTCTTGA', mapping=1505, ref_letter='A', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1531', umi='CCTCTTGA', mapping=1531, ref_letter='T', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1533', umi='CCTCTTGA', mapping=1531, ref_letter='G', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1533', umi='CCTCTTGA', mapping=1532, ref_letter='G', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        self.set_test_mutation(location='chr1_1541', umi='CCTCTTGA', mapping=1536, ref_letter='T', qry_counts={},
                               qry_counts_total=0, quality={}, frag_type=2, no_mutation=1)
        # update self.loc_mutations
        self.loc_mutations.find_mutations(
            [self.record1mut, self.record1nomut, self.record2nomut, self.record3nomut, self.record4nomut,
             self.record5nomut, self.record6nomut, self.record7nomut])
        self.loc_mutations.sort_locations()
        self.loc_mutations.find_no_mutations(
            [self.record1mut, self.record1nomut, self.record2nomut, self.record3nomut, self.record4nomut,
             self.record5nomut, self.record6nomut, self.record7nomut])
        self.expected_loc_mutations.sort_locations()

    # Checking the intersection mechanism
    def test_14(self):
        self.compare_locations()

    # Test createVcf
    def test_15(self):
        vcf = CreateVCF(self.loc_mutations.locations, 'chr1', 0, 3000, 'output.vcf', False, 0)
        vcf.summar_mutations()
        # true_vcf_rows = [vcf.vcf_rows[0]]  # header line
        true_vcf_rows = [['chr1', '1001', 'G', 'C', 'CCTCTTGA-1/2:;|'],
                         ['chr1', '1004', 'A', 'G', 'CCTCTTGA-1/2:0/1:;|'],
                         ['chr1', '1505', 'G', 'C', 'CCTCTTGA-1/2:0/1:0/1:;|'],
                         ['chr1', '1528', 'A', 'G', 'CCTCTTGA-1/0:0/1:0/1:;|'],
                         ['chr1', '1531', 'T', 'A', 'CCTCTTGA-1/0:0/1:;|'],
                         ['chr1', '1533', 'G', 'C', 'CCTCTTGA-1/0:0/1:0/1:;|'],
                         ['chr1', '1541', 'T', 'A', 'CCTCTTGA-1/0:0/1:;|']]
        self.assertEqual(vcf.vcf_rows, true_vcf_rows)


class MutationClasiffierTest(ReadBarcodeFileTest):
    def setUp(self):
        super(MutationClasiffierTest, self).setUp()
        self.classifier = MutationClassifier(locations=None, chr='chr1', chr_start=0, chr_end=10000,
                                             classifier_output_file_name='', classes_stat={}, print_header=False,
                                             eb_star_class_threshold=0.2, serial_file_number=0)
        self.mutation_loc_on_ref = 'chr1_10'

    def update_data(self, records):
        self.loc_mutations.find_mutations(records)
        self.loc_mutations.sort_locations()
        self.loc_mutations.find_no_mutations(records)
        # self.expected_loc_mutations.sort_locations()
        return self.loc_mutations.locations[self.mutation_loc_on_ref]

    def test_max_umi1(self):
        # TTAA umi has more pure fragments (even though the number of mutated read higher in CCCC umi)
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, 'A')

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        self.assertEqual(max_umi, 'TTAA')

    def test_max_umi2(self):
        # Both umi's have the same number of pure fragmets (1), but CCCC has more mutated reads (including on non-pure fragments)
        records = self.buildSamRecordsMutationInChr1_10(False, 10, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 20, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'CCCC', 8, 'T')
        records += self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 40, 'TTAA', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 40, 'TTAA', 9, 'A')

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        self.assertEqual(max_umi, 'CCCC')

    def test_max_umi3(self):
        # Both umi's have the same number of pure fragmets (1), and the number of mutated reads (80), but TTAA has more total reads (mutated and non-mutated)
        records = self.buildSamRecordsMutationInChr1_10(False, 10, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 20, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'CCCC', 8, 'T')
        records += self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 40, 'TTAA', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 40, 'TTAA', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 10, 'TTAA', 7, 'T')

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        self.assertEqual(max_umi, 'TTAA')

    def test_dirty_frag_num(self):
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 5, 'T')  # Contardiction

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual(dirty_frags_num, 4)

    def test_16(self):  # D type
        # 2 Reads with same umi, mapping and mutation
        records = self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 10, 'A')
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 2))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'D')

    def test_17(self):  # C type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (3, 6))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'C')

    def test_18(self):  # B type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 2))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'B')

    def test_19(self):  # A type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 4))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'A')

    def test_19b(self):  # A type with one reversed complement umi
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(True, 5, 'TTTT', 8, 'A')
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 4))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'A')

    def test_19c(self):  # A type with reversed complement umis and one non rc umi
        self.expected_loc_mutations = LocationsWithMutations(sam_reader_mutation=None, sam_reader_no_mutation=None,
                                                             chr='chr1-minusStrand', chr_start=0, chr_end=10000,
                                                             chr_prev_start=0, filter_edge_mutations=0, min_mapq=0,
                                                             max_gene_length=10000, bases_distribution=None)
        self.loc_mutations = LocationsWithMutations(sam_reader_mutation=None, sam_reader_no_mutation=None,
                                                    chr='chr1-minusStrand', chr_start=0, chr_end=10000,
                                                    chr_prev_start=0, filter_edge_mutations=0, min_mapq=0,
                                                    max_gene_length=10000, bases_distribution=None)
        self.classifier = MutationClassifier(locations=None, chr='chr1-minusStrand', chr_start=0, chr_end=10000,
                                             classifier_output_file_name='', classes_stat={}, print_header=False,
                                             eb_star_class_threshold=0.2, serial_file_number=0)
        self.mutation_loc_on_ref = 'chr1-minusStrand_10'

        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(True, 2, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation
        records += self.buildSamRecordsMutationInChr1_10(True, 2, 'CCCC', 8, 'A')
        records += self.buildSamRecordsMutationInChr1_10(True, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(True, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(True, 5, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 50, 'AAAA', 8, 'T')
        records += self.buildSamRecordsMutationInChr1_10(False, 50, 'AAAA', 8, 'A')

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'T')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'T')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'T')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 4))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'A')

    def test_20(self):  # EA type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 4))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (3, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'EA')

    def test_21(self):  # EB type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')  # Max UMI (more than other UMIs)
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI

        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'CCAA', 7, 'T')  # Contardiction other UMI

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')
        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0.0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (3, 4.0))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2), MEAN(2/0.5))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'EB')

    def test_21b(self):  # EB-star type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')  # Max UMI (more than other UMIs)
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'ATTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'GTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AATT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'GGTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'GGGT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCT', 8, '')

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')
        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0.0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (10, 20))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (1, 6.0))  # MEAN(MEAN(3/0.5, 3/0.5))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'EB-star')

    def test_21c(self):  # EB not EB-star type because we have no at least 2 cutting points in GGGG
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')  # Max UMI (more than other UMIs)
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'ATTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'GTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AATT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'GGTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'GGGT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCT', 8, '')

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')
        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0.0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (10, 20))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (1, 6.0))  # MEAN(MEAN(3/0.5, 3/0.5))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'EB')

    def test_21d(
            self):  # EB not EB-star type because there is 4 umis without mutation against one umi with mutations (GGGG) - more than 0.2 ratio in this variable eb_star_class_threshold
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')  # Max UMI (more than other UMIs)
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'GGGT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCT', 8, '')

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')
        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0.0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (4, 8))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (1, 6.0))  # MEAN(MEAN(3/0.5, 3/0.5))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'EB')

    def test_22(self):  # EC type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')  # Max UMI (more than other UMIs)
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (3, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (2, 3.0))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'EC')

    def test_23(self):  # FA type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation)
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 50))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (3, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num,
                                               o_umi_mut_num, o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'FA')

    def test_24(self):  # FB type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation)
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 50))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0.0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (2, 3.0))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num,
                                               o_umi_mut_num, o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'FB')

    def test_25(self):  # FC type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10,
                                                        'A')  # Max UMI (In other UMI there is no mutation)
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 10, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 3, 'GGGG', 9, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 5, 'TTTT', 8, '')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 50))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (3, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (2, 11))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (2, 3.0))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num,
                                               o_umi_mut_num, o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'FC')

    def test_26(self):  # GA type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 5, 'T')  # Contardiction

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (4, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'GA')

    def test_27(self):  # GB type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (2, 3.0))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'GB')

    def test_28(self):  # GC type
        # 2 Reads with same umi, mapping and mutation AND additional 2 reads with different mapping
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 9, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction

        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (2, 52))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (3, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (2, 3.0))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'GC')

    def test_29(self):  # HA type
        # 2 Reads with same umi, mapping and mutation
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 5, 'T')  # Contardiction

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 50))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (4, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'HA')

    def test_30(self):  # HB type
        # 2 Reads with same umi, mapping and mutation
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 50))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (0, 0))
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (2, 3.0))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'HB')

    def test_31(self):  # HC type
        # 2 Reads with same umi, mapping and mutation
        records = self.buildSamRecordsMutationInChr1_10(False, 50, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'CCCC', 8, 'T')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 8, 'A')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 7, '')  # Contardiction
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 6, 'T')  # Contardiction

        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'AAAA', 8, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 8, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 10, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'A')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 4, 'TTAA', 7, 'T')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 7, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'TTAA', 6, '')  # Contardiction other UMI
        records += self.buildSamRecordsMutationInChr1_10(False, 2, 'CCCC', 5, 'T')  # Contardiction

        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')
        self.assertEqual(self.classifier.total_mutation, 60)
        self.assertEqual(self.classifier.total_non_mutation, 12)
        self.assertEqual(self.classifier.total_other_mutations, 16)
        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (1, 50))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (4, 4.0))  # MEAN((4+4)/2, 2/0.5, 2/0.5)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean),
                         (2, 2.5))  # MEAN(MEAN((2+2)/2), MEAN(2/0.5,2/0.5,(4+4)/2, 0/2))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'HC')

    def test_32(self):  # I type
        # 2 Reads with same umi, mapping and mutation
        records = self.buildSamRecordsMutationInChr1_10(False, 10, 'CCCC', 10, 'A')
        records += self.buildSamRecordsMutationInChr1_10(False, 20, 'CCCC', 10, '')  # Contardiction
        location_obj = self.update_data(records)
        max_umi = self.classifier.max_mutation_rate_umi(location_obj, 'A')
        pure_frags_num, pure_counts_total, dirty_frags_num, dirty_pos_ratio_mean = self.classifier.mutation_stat_on_max_umi(
            location_obj, max_umi, 'A')
        o_umi_non_mut_num, o_umi_non_mut_counts_total, o_umi_mut_num, o_umi_mut_ratio_mean, o_umi_same_mut_more_than_one_fragment_pure_frags_num = self.classifier.mutation_stat_on_other_umis(
            location_obj, max_umi, 'A')

        self.assertEqual(max_umi, 'CCCC')
        self.assertEqual((pure_frags_num, pure_counts_total), (0, 0))
        self.assertEqual((dirty_frags_num, dirty_pos_ratio_mean), (1, 2.0))  # MEAN((20+10)/2)
        self.assertEqual((o_umi_non_mut_num, o_umi_non_mut_counts_total), (0, 0))
        self.assertEqual((o_umi_mut_num, o_umi_mut_ratio_mean), (0, 0.0))
        self.assertEqual(
            self.classifier.get_mutations_type(pure_frags_num, dirty_frags_num, o_umi_non_mut_num, o_umi_mut_num,
                                               o_umi_same_mut_more_than_one_fragment_pure_frags_num),
            'I')


class SamRecordTest(unittest.TestCase):
    def test_33(self):
        record1 = SamRecord(
            *'NB8585__QX: 1024 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record2 = SamRecord(
            *'NB8585__QX: 3328 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record3 = SamRecord(
            *'NB8585__QX: 16 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])

        self.assertEqual(SamRecord.is_record_umi_duplication(record1), True)
        self.assertEqual(SamRecord.is_record_umi_duplication(record2), True)
        self.assertEqual(SamRecord.is_record_umi_duplication(record3), False)

    def test_34(self):
        record1 = SamRecord(
            *'NB8585__QX: 1024 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record2 = SamRecord(
            *'NB8585__QX: 3328 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record3 = SamRecord(
            *'NB8585__QX: 16 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])
        record4 = SamRecord(
            *'NB8585__QX: 31 chr1 1000 255 3M500N9M * 0 0 AGCTAGCTAGCT ABCDEFGHIJKL'.split(),
            tags=['MD:Z:1C10', 'XS:A:+', 'XF:Z:GeneName', 'RX:Z:CCTCTTGA'])

        self.assertEqual(SamRecord.reverse_complement_if_needed(record1), False)
        self.assertEqual(SamRecord.reverse_complement_if_needed(record2), False)
        self.assertEqual(SamRecord.reverse_complement_if_needed(record3), True)
        self.assertEqual(SamRecord.reverse_complement_if_needed(record3), True)


class SamRecordReadFunctionTest(unittest.TestCase):

    def test_read_function(self):
        interval_size = 100
        max_gene_length = 200

        r = SamReader(os.path.join('test', 'data', 'test-SamReader-read-function.sam'))
        results = []
        for chr, chr_length in r.chr_list:
            for chr_start in xrange(0, int(chr_length), interval_size):
                # minus epsilon for the case that max_gene_length and interval_size are equal
                intervals_num = math.floor(float(max_gene_length) / interval_size + 1 - 0.000000001)
                chr_prev_start = int(max(0, chr_start - intervals_num * interval_size))
                chr_end = chr_length if chr_length == chr_start + interval_size else min(chr_length,
                                                                                         chr_start + interval_size - 1)

                title = '[chr: %s start: %s, end: %s, prev: %s]' % (chr, chr_start, chr_end, chr_prev_start)
                results.append(title)
                interval_results = []
                for i in r.read(chr=chr, chr_start=chr_start, chr_end=chr_end, chr_prev_start=chr_prev_start,
                                min_mapq=0,
                                max_gene_length=max_gene_length):  # int(sys.argv[2])):
                    interval_results.append((i.rname, i.pos))
                results.append(set(interval_results))
        self.assertEqual(results, ['[chr: chr1 start: 0, end: 99, prev: 0]', set([]),
                                   '[chr: chr1 start: 100, end: 199, prev: 0]', set([('chr1', 105), ('chr1', 190)]),
                                   '[chr: chr1 start: 200, end: 299, prev: 0]', set([('chr1', 210)]),
                                   '[chr: chr1 start: 300, end: 399, prev: 100]', set([('chr1', 308), ('chr1', 190)]),
                                   '[chr: chr1 start: 400, end: 499, prev: 200]', set([('chr1', 308)]),
                                   '[chr: chr1 start: 500, end: 599, prev: 300]', set([]),
                                   '[chr: chr2 start: 0, end: 99, prev: 0]', set([]),
                                   '[chr: chr2 start: 100, end: 199, prev: 0]', set([('chr2', 199)]),
                                   '[chr: chr2 start: 200, end: 299, prev: 0]',
                                   set([('chr2', 199), ('chr2', 202), ('chr2', 203)]),
                                   '[chr: chr2 start: 300, end: 399, prev: 100]', set([('chr2', 199)]),
                                   '[chr: chr2 start: 400, end: 499, prev: 200]', set([]),
                                   '[chr: chr2 start: 500, end: 599, prev: 300]', set([]),
                                   '[chr: chr2 start: 600, end: 699, prev: 400]', set([]),
                                   '[chr: chr2 start: 700, end: 799, prev: 500]', set([]),
                                   '[chr: chr2 start: 800, end: 899, prev: 600]', set([]),
                                   '[chr: chr2 start: 900, end: 999, prev: 700]', set([])])


if __name__ == '__main__':
    unittest.main()
