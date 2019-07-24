import collections
import pcdhit
from math import log10
# import sys
# import os
import re

from statistics import stdev, mean
from metagenomi.helpers import avg_perc_identity, most_frequent

'''
Class used to parse a single entry in a minced output file
along with a script for splitting up a minced file

'''


def split_minced_output(infile):
    '''
    input = minced output file
    returns: an array with each CRISPR array
    '''
    total_crisprs = []
    names = []
    with open(infile, 'r') as file:
        i = 0
        lines = file.readlines()
        for i in range(len(lines)):
            line = lines[i].rstrip()
            if 'Sequence ' in line:
                seq_name = line.split(' ')[1][1:-1]
                seq_line = line

            if 'CRISPR' in line:
                num = line.split(' ')[1]
                name = seq_name + f'_CRISPR_{num}'
                new_array = [seq_line] + [''] + [line]
                j = i+1
                while 'Repeats:' not in lines[j]:
                    new_array.append(lines[j].rstrip())
                    j += 1
                new_array.append(lines[j].rstrip())
                new_array.append('')

                names.append(name)
                total_crisprs.append(new_array)

    # names and arrays are in conserved order
    return(names, total_crisprs)


class ShortFeature:
    '''
    Class used to represent a minced output file.

    '''
    def __init__(self, name, start, stop, contig, strand, seq, parent=None):
        self.name = name
        self.start = int(start)
        self.stop = int(stop)
        self.contig = contig
        self.strand = strand
        self.seq = seq
        self.mgid = self.name[:22]
        # Feature object
        self.parent = parent
        self.dummy = 'DUMMY'

        # self.sql =

    def export_sql(self, feature_type, source='proprietary', parent_id=None, cluster_id=None):
        # created_at = time.time()
        # updated_at = time.time()
        d = {'name': self.name, 'contig_name': self.contig,
             'feature_start': self.start, 'feature_end': self.stop,
             'strand': self.strand, 'mg_assembly_id': self.mgid,
             'source': source, 'feature_type': feature_type,
             'parent': parent_id, 'cluster': cluster_id}

        return d


class Crispr:
    '''
    Class used to represent a minced output file.

    '''
    def __init__(self, name, a):
        self.name = name
        self.spacers = []
        self.repeats = []
        self.spacer_seqs = []
        self.repeat_seqs = []
        self.pos = []
        self.parse_crispr(a)

        self.motif = self.check_motif_match()
        self.avg_repeat_identity = avg_perc_identity(self.write_repeats())

        self.spacer_clusters = cluster_seqs(self.spacer_seqs)
        self.repeat_clusters = cluster_seqs(self.repeat_seqs)
        self.repeat_length_deviation = get_length_deviation(self.repeat_seqs)
        self.spacer_length_deviation = get_length_deviation(self.spacer_seqs)
        # self.avg_spacer_identity = avg_perc_identity(self.spacer_seqs)

    def parse_crispr(self, a):
        for i in range(len(a)):
            line = a[i]
            # If first line
            if 'Sequence' in line:
                self.seq = line.split(' ')[1][1:-1]
                self.seqlen = int(line.split('(')[1][:-3])
                i += 1
            else:
                if 'CRISPR' in line:
                    self.number = int(line.split(' ')[1])
                    arraystart = int(line.split(': ')[1].split(' -')[0])
                    arrayend = int(line.split('- ')[1].rstrip())
                    self.range = (arraystart, arrayend)

                else:
                    if 'POSITION' in line:
                        start = i+2
                    else:
                        if 'Repeats: ' in line:
                            self.avgRepeatLen = int(line.split(': ')[2].split('\t')[0])
                            self.avgSpacerLen = int(line.split(': ')[3].rstrip())

                            end = i-1
                            array = a[start:end]
                            c = 1
                            for x in array:
                                p = int(x.split('\t')[0])
                                self.pos.append(p)

                                rseq = x.split('\t')[2]
                                rlen = len(rseq)
                                repeat_name = f'{self.name}_repeat_{c}'
                                rend = p+rlen
                                r = ShortFeature(repeat_name, p, rend, self.seq, None, rseq)
                                self.repeats.append(r)
                                self.repeat_seqs.append(rseq)
                                if len(x.split('\t')) > 3:
                                    sseq = x.split('\t')[3]
                                    slen = len(sseq)
                                    spacer_name = f'{self.name}_spacer_{c}'
                                    send = rend+slen
                                    s = ShortFeature(spacer_name, rend, send, self.seq, None, sseq)
                                    self.spacers.append(s)
                                    self.spacer_seqs.append(sseq)
                                c += 1

    def check_motif_match(self):
        '''
        Does a sequence end with ATTGAAA(N)?
        or does a sequence begin with the reverse complement?
        '''
        motif = 'ATTGAAA'
        rev_motif = 'TTTCAAT'

        for r in self.repeat_seqs:
            if r[:-1].endswith(motif):
                return True
            if r.endswith(motif):
                return True
            if r.startswith(rev_motif):
                return True
            if r[1:].startswith(rev_motif):
                return True
        return False

    def perc_identity(aln):
        i = 0
        for a in range(0, len(aln[0])):
            s = aln[:, a]
            if s == len(s) * s[0]:
                i += 1
        return 100*i/float(len(aln[0]))

    def score_array(self):
        score = 0
        # 3 : either +3 or 0
        # Repeat has at	least 23 bases and ATTGAAA(N) at the end
        if len(self.repeats) > 22 and self.motif:
            # print('Adding three for a motif')
            score += 3

        # 4 : range(0, 1)
        # 	Overall repeat identity	within	an	array
        # print('self.avg_repeat_identity = ', self.avg_repeat_identity)
        s = (self.avg_repeat_identity*100 - 80)/20
        score += s
        # print(f'Adding {s} for overall repeat identity within an array. Score = {score}')

        # 5: -1.5 or 0
        # The repeats in the array do not form one sequence similarity cluster
        # print('self.repeat_clusters = ', self.repeat_clusters)
        num_repeat_clusters = len(self.repeat_clusters)
        if num_repeat_clusters > 1:
            score = score - 1.5
            # print(f'Subtracting {1.5} because the repeats form two clusters. Score = {score}')

        # 6 : range(-3, +1)
        # Scoring the repeat lengths

        # print('repeat_length_deviation', repeat_length_deviation)
        s = self.repeat_length_deviation*(-2/5) + 1
        score += s
        # print(f'Adding {s} because of repeat length deviation. Score = {score}')

        # 7 : range(-3, +3)
        # Scoring the spacer lengths

        # print('spacer_length_deviation', spacer_length_deviation)
        s = self.spacer_length_deviation*(-1) + 3
        if s < -3:
            s = -3
        score += s
        # print(f'Adding {s} because of spacer length deviation. Score = {score}')

        # 8 : range(-3, +1)
        # Overall spacer identity
        num_spacer_clusters = len(self.spacer_clusters)
        # print('num_spacer_clusters', num_spacer_clusters)
        if num_spacer_clusters <= len(self.spacers)/2:
            s = -3
            # print(f'Adding {s} because spacers are very cluster-y')
        else:
            s = 0.2*num_spacer_clusters
            if s > 1:
                s = 1
            # print(f'Adding {s} because spacers do not cluster much')

        score += s
        # print(f'Score = {score}')

        # 9 : range(0, 1)
        # Scoring total number of identical repeats
        # unique_repeats = len(self.get_unique_repeats())
        total_repeats = len(self.repeats)
        most_frequent_repeat = most_frequent(self.repeat_seqs)
        total_mutated = len([i for i in self.repeat_seqs if i != most_frequent_repeat])
        # print(f'{total_mutated} mutated repeats out of {total_repeats}!', self.repeat_seqs)
        if total_mutated > 0:
            # print(f'Adding {s}. There are some mutated repeats.')
            s = log10(total_repeats) - log10(total_mutated)
        else:
            # print(f'Adding {s} because there are no mutated repeats')
            s = log10(total_repeats)

        if s > 1:
            s = 1
        score += s

        return score

    def write_repeats(self, filename='temp.repeats.fa'):
        with open(filename, 'w') as f:
            for r in self.repeats:
                f.write(f'>{r.name}\n')
                f.write(f'{r.seq}\n')
        return filename

    def write_spacers(self, filename='temp.spacers.fa'):
        with open(filename, 'w') as f:
            for r in self.spacers:
                f.write(f'>{r.name}\n')
                f.write(f'{r.seq}\n')
        return filename

    # def orient_repeats(self):
    #     '''check if repeat starts with GTT or ends with AAC
    #     or at least if they start with G/end with C.
    #     params repeats: list of repeats
    #     simple rules:
    #     if any of them starts GTT, then they are all forward
    #     if any of them ends AAC, then they are all reversed
    #     if any of them starts GYY, then they are all forward
    #     if any of them ends with the rev comp of GYY, then they are all reversed
    #     if any of them starts "G", then they are all forward
    #     if any of them ends "C", then they are all reversed
    #     FUTURE: add more complexity to CRISPR array directionality determination
    #     make it a majority rules, or know which is the "real" repeat
    #     '''
    #     repeats = self.repeat_seqs
    #
    #     repeat_directed = True
    #     repeat_GYYfwd = re.compile(r'^G[CT][CT]')
    #     repeat_GYYrev = re.compile(r'[AG][AG]C$')
    #
    #     if any(repeat.startswith("GTT") for repeat in repeats):
    #         pass
    #     elif any(repeat.endswith("AAC") for repeat in repeats):
    #         repeats = [str(Seq(x).reverse_complement()) for x in repeats]  # reverse complement all
    #     elif any(re.search(repeat_GYYfwd, repeat) for repeat in repeats):
    #         pass
    #     elif any(re.search(repeat_GYYrev, repeat) for repeat in repeats):
    #         repeats = [str(Seq(x).reverse_complement()) for x in repeats]  # reverse complement all
    #         pass
    #     elif any(repeat.startswith("G") for repeat in repeats):
    #         pass
    #     elif any(repeat.endswith("C") for repeat in repeats):
    #         repeats = [str(Seq(x).reverse_complement()) for x in repeats]  # reverse complement all
    #     else:
    #         repeat_directed = False
    #
    #         return(repeats, repeat_directed)  # flag these as un-directed, try blasting in both directions

    def get_consensus_repeat(self):
        pass

    def get_spacers(self):
        return self.spacer_seqs

    def get_range(self):
        return self.range

    def get_num_spacers(self):
        return len(self.spacer_seqs)

    def get_num_repeats(self):
        return len(self.repeat_seqs)

    def get_unique_repeats(self):
        return set(self.repeat_seqs)

    def get_name(self):
        return self.name

    def get_repeats(self):
        return self.repeat_seqs

    def get_seqlen(self):
        return self.seqlen

    def get_seq(self):
        return self.seq

    def get_avg_repeat_length(self):
        return self.avgRepeatLen

    def get_avg_spacer_length(self):
        return self.avgSpacerLen

    def get_spacer_stdev(self):
        slengths = [len(i) for i in self.spacer_seqs]
        return stdev(slengths)

    def get_repeat_stdev(self):
        rlengths = [len(i) for i in self.repeat_seqs]
        return stdev(rlengths)

    def get_longest_spacer(self):
        return max(self.spacer_seqs, key=len)

    def get_shortest_spacer(self):
        return min(self.spacer_seqs, key=len)

    def __str__(self):
        rep = f'{self.name}\nRepeats: {self.repeat_seqs}\n'
        rep += f'Spacers: {self.spacer_seqs}'
        return rep

    def to_dict(self):
        '''
        ['array_name', 'contig', 'contig_length', 'array_start',
         'array_end', 'avg_repeat_len', 'avg_spacer_len', 'num_repeats',
         'repeat_mode_dev', 'spacer_mode_dev', 'min_repeat_len',
         'min_spacer_len', 'max_spacer_len', 'max_repeat_len',
         'array_quality']
        '''

        spacer_lengths = [len(i) for i in self.spacer_seqs]
        repeat_lengths = [len(i) for i in self.repeat_seqs]

        d = {'name': self.get_name(), 'contig': self.get_seq(),
             'contig_length': self.get_seqlen(), 'start': self.get_range()[0],
             'end': self.get_range()[1],
             'avg_repeat_len': self.get_avg_repeat_length(),
             'avg_spacer_len': self.get_avg_spacer_length(),
             'num_repeats': self.get_num_repeats(),
             'min_repeat_length': min(repeat_lengths),
             'max_repeat_len': max(repeat_lengths),
             'min_spacer_len': min(spacer_lengths),
             'max_spacer_len': max(spacer_lengths),
             'spacer_clusters': len(self.spacer_clusters),
             'repeat_clusters': len(self.repeat_clusters),
             'repeat_length_deviation': self.repeat_length_deviation,
             'spacer_length_deviation': self.spacer_length_deviation,
             'avg_repeat_identity': self.avg_repeat_identity,
             'score': self.score_array(),
             'motif_ATTGAAAN': self.motif
             }

        # row = [self.get_name(), self.get_seq(), self.get_seqlen(),
        #        self.get_range()[0], self.get_range()[1],
        #        self.get_avg_repeat_length(), self.get_avg_spacer_length(),
        #        self.get_num_repeats(), self.repeat_length_deviation,
        #        self.spacer_length_deviation, min(spacer_lengths),
        #        min(repeat_lengths), max(spacer_lengths),
        #        max(repeat_lengths), self.score_array()]

        return d


def get_length_deviation(seqs):
    most_common_length = get_most_common_length(seqs)
    deviations = [abs(most_common_length-len(i)) for i in seqs]
    return sum(deviations)/len(seqs)


def get_most_common_length(seqs):
    lengths = [len(i) for i in seqs]

    common = collections.Counter(lengths).most_common()
    if len(common) > 1:
        return mean([i[0] for i in common])
    else:
        return common[0][0]


def cluster_seqs(seqs, threshold=0.8, verbose=False):
    records = [('>fake_header', i) for i in seqs]
    if verbose is False:
        filtered_records = pcdhit.filter(records, threshold)

    clusters = []
    for i in filtered_records:
        seq = i[1]
        clusters.append(seq)
    print('DONE CLUSTERING')
    return clusters
