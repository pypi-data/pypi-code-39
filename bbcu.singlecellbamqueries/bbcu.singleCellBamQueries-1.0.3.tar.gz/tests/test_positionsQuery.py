from unittest import TestCase

from singleCellBamQueries.positions_query import PositionsQuery


class TestPositionsQuery(TestCase):
    def setUp(self):
        pos_q = PositionsQuery(*(17 * [None]))

    def test_valid_pos(self):
        pos_q = PositionsQuery(None, None, None, None, None,
                               min_cells=1, max_cells=2,
                               min_mutated_umis=1, max_mutated_umis=2,
                               min_reads_per_mutated_umi=2, max_reads_per_mutated_umi=3,
                               min_non_mutated_umis=1, max_non_mutated_umis=2,
                               min_reads_per_non_mutated_umi=2, max_reads_per_non_mutated_umi=3,
                               enable_cells_with_invalid_umis_num=False,
                               enable_umis_with_invalid_reads_num=False,
                               tag_of_umi=None, tag_of_cell_barcode=None,umi_start=None, umi_length=None,
                               cell_barcode_start=None, cell_barcode_length=None)

        # valid case:
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))

        # enable_cells_with_invalid_umis_num = False
        # enable_umis_with_invalid_reads_num = False
        # UMI with mutated and not mutated reads
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 2}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # one umi with reads above max in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 4, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # one umi with reads under min in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # one umi with reads above max in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 4}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # one umi with reads under min in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # valid one umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # no umi
        pos_data = {'AAA': {},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 1, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 1}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))

        pos_q = PositionsQuery(None, None, None, None, None,
                               min_cells=1, max_cells=2,
                               min_mutated_umis=1, max_mutated_umis=2,
                               min_reads_per_mutated_umi=2, max_reads_per_mutated_umi=3,
                               min_non_mutated_umis=1, max_non_mutated_umis=2,
                               min_reads_per_non_mutated_umi=2, max_reads_per_non_mutated_umi=3,
                               enable_cells_with_invalid_umis_num=False,
                               enable_umis_with_invalid_reads_num=True,
                               tag_of_umi=None, tag_of_cell_barcode=None,umi_start=None, umi_length=None,
                               cell_barcode_start=None, cell_barcode_length=None)

        # enable_cells_with_invalid_umis_num = False
        # enable_umis_with_invalid_reads_num = True
        # UMI with mutated and not mutated reads
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 2}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads above max in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 4, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads under min in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads above max in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 4}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads under min in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # no umi
        pos_data = {'AAA': {},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 1, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 1}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (False, False))

        pos_q = PositionsQuery(None, None, None, None, None,
                               min_cells=1, max_cells=2,
                               min_mutated_umis=1, max_mutated_umis=2,
                               min_reads_per_mutated_umi=2, max_reads_per_mutated_umi=3,
                               min_non_mutated_umis=1, max_non_mutated_umis=2,
                               min_reads_per_non_mutated_umi=2, max_reads_per_non_mutated_umi=3,
                               enable_cells_with_invalid_umis_num=True,
                               enable_umis_with_invalid_reads_num=False,
                               tag_of_umi=None, tag_of_cell_barcode=None,umi_start=None, umi_length=None,
                               cell_barcode_start=None, cell_barcode_length=None)

        # enable_cells_with_invalid_umis_num = True
        # enable_umis_with_invalid_reads_num = False
        # UMI with mutated and not mutated reads
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 2}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['CCC']))
        # one umi with reads above max in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 4, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['CCC']))
        # one umi with reads under min in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['CCC']))
        # one umi with reads above max in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 4}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['AAA']))
        # one umi with reads under min in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['AAA']))
        # no umi
        pos_data = {'AAA': {},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['CCC']))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 1, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['CCC']))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 1}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['AAA']))

        pos_q = PositionsQuery(None, None, None, None, None,
                               min_cells=1, max_cells=2,
                               min_mutated_umis=1, max_mutated_umis=2,
                               min_reads_per_mutated_umi=2, max_reads_per_mutated_umi=3,
                               min_non_mutated_umis=1, max_non_mutated_umis=2,
                               min_reads_per_non_mutated_umi=2, max_reads_per_non_mutated_umi=3,
                               enable_cells_with_invalid_umis_num=True,
                               enable_umis_with_invalid_reads_num=True,
                               tag_of_umi=None, tag_of_cell_barcode=None,umi_start=None, umi_length=None,
                               cell_barcode_start=None, cell_barcode_length=None)

        # enable_cells_with_invalid_umis_num = True
        # enable_umis_with_invalid_reads_num = True
        # UMI with mutated and not mutated reads
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 2}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads above max in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 4, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads under min in mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads above max in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 4}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # one umi with reads under min in not mut umi
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (2, ['AAA', 'CCC']))
        # no umi
        pos_data = {'AAA': {},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['CCC']))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 1, 'no_mut_reads': 0}, 'TT': {'mut_reads': 1, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 2}, 'TT': {'mut_reads': 0, 'no_mut_reads': 2}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['CCC']))
        # whole cell invalid
        pos_data = {'AAA': {'GG': {'mut_reads': 2, 'no_mut_reads': 0}, 'TT': {'mut_reads': 2, 'no_mut_reads': 0}},
                    'CCC': {'GG': {'mut_reads': 0, 'no_mut_reads': 1}, 'TT': {'mut_reads': 0, 'no_mut_reads': 1}}}
        self.assertEqual(pos_q.valid_pos(pos_data), (1, ['AAA']))
