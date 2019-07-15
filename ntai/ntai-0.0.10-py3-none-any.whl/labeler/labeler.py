import os
from multiprocessing import Pool
from .defaults import (LABEL_ORDER, USE_OTHER_CLASS, OTHER_CLASS)
# from ntai.ranges import LabeledRange, LabeledRanges
from lrng import LabeledRange, LabeledRanges
from lrng.numba import coalesce, label_range, relevant_labels
class Labeler:
    def __init__(
        self,
        label_order: str = LABEL_ORDER,
        use_other_class: bool = USE_OTHER_CLASS,
        other_class: str = OTHER_CLASS,
        processes: int = 1
    ):
        '''
        Arguments:
            label_order (str): the order labels should be embedded.
            use_other_class (bool): whether or not a class `"Other"` should be
                used.
            other_class (str): the class name of `"Other"`
            processes (int): number of CPU cores to use when encoding / decoding.
                By default 1. If set to None, uses all.
        '''
        if processes is None: processes = os.cpu_count()
        self.processes = processes
        self.use_other_class = use_other_class
        self.other_class = other_class

        if (use_other_class):
            if other_class not in label_order:
                label_order += [other_class]
        self.label_order = label_order

    def encode(self, sequence:str, ranges, offset:int=0) -> list:
        '''
        Arguments:
            sequence (str): the sequence to embed.
            ranges (LabeledRanges): the reference ranges to use to generate the
                embedding of the sequence.
            offset (int): how far to offset each index. By default `0`.
        Returns:
            embedding (list): the embedded sequence.
        '''
        if isinstance(ranges, LabeledRanges):
            ranges = ranges.as_list()
        return label_range(offset, offset+len(sequence), ranges, self.label_order, self.use_other_class)

    def label(self, sequence:list, reference_labels:dict):
        '''
        Arguments:
            sequence (list): a list consisting of the at least the bed6
                information of the sequence e.g.
                    `[chromosome, start, stop, name, score, strand,]`

            reference_labels (dict): a dctionary consisting the following
                structure:
                    ```
                    {
                        <chromosome>: {
                            <strand>: LabeledRanges(...),
                            ...
                        }, ...
                    }
                    ```
        Returns:
            sequence_ranges (LabeledRanges): the ranges for which a given class
                appear in the provided sequence
        '''
        chromosome, start, stop, name, score, strand, *_ = sequence
        reference_ranges = reference_labels[chromosome][strand]
        if isinstance(reference_ranges, LabeledRanges):
            reference_ranges = reference_ranges.as_list()
        result = relevant_labels(int(start), int(stop), reference_ranges, self.label_order)
        return LabeledRanges(result)
