
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
        # Feature.__init__(self, self.name, self.range[0], self.range[1], self.seq, None, None)

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
                                # print(f'p = {p}, rseq = {rseq}, rlen = {rlen}, repeat_name = {repeat_name}, rend = {rend}')
                                # print(f'self.seq = {self.seq}')
                                # def __init__(self, name, start, stop, contig, strand, seq, parent=None):
                                r = ShortFeature(repeat_name, p, rend, self.seq, None, rseq)
                                self.repeats.append(r)
                                self.repeat_seqs.append(rseq)
                                # print(repr(x))
                                # print(len(x.split('\t')))
                                if len(x.split('\t')) > 3:
                                    sseq = x.split('\t')[3]
                                    slen = len(sseq)
                                    spacer_name = f'{self.name}_spacer_{c}'
                                    send = rend+slen
                                    s = ShortFeature(spacer_name, rend, send, self.seq, None, sseq)
                                    self.spacers.append(s)
                                    self.spacer_seqs.append(sseq)
                                c += 1

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

    def __str__(self):
        rep = f'{self.name}\nRepeats: {self.repeat_seqs}\n'
        rep += f'Spacers: {self.spacer_seqs}'
        return rep
