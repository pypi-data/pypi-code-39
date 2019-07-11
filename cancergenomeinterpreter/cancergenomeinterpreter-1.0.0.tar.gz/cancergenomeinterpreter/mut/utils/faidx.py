import logging

# faidx python code adapted from Allen Yu
# http://www.allenyu.info/item/24-quickly-fetch-sequence-from-samtools-faidx-indexed-fasta-sequences.html
# and from TransVar
# https://github.com/zwdzwd/transvar
import mmap


def normalize_chrm(chrm):

    if chrm == '23' or chrm == 'chr23':
        chrm = 'X'

    if chrm == '24' or chrm == 'chr24':
        chrm = 'Y'

    if chrm == '25' or chrm == 'chr25':
        chrm = 'M'

    if chrm == 'MT' or chrm == 'chrMT':
        chrm = 'M'

    if chrm.isdigit() or chrm in ['X', 'Y', 'M']:
        # not chrm.startswith('chr')
        chrm = 'chr' + chrm

    return chrm


class RefGenome:

    def __init__(self, fasta_file):
        self.faidx = {}

        self.fasta_file = fasta_file
        try:
            self.fasta_fd = open(fasta_file)
            self.fasta_handle = mmap.mmap(self.fasta_fd.fileno(), 0, access=mmap.ACCESS_READ)
        except IOError:
            logging.error("Reference sequence doesn't exist")

        try:
            self.faidx_handle = open(fasta_file + ".fai")
        except IOError:
            logging.error("samtools faidx file doesn't exist for reference")
        self.load_faidx()

    # Function to cache fasta index in dictionary
    # faidx format contains the following columns:
    # .the name of the sequence
    # .the length of the sequence
    # .the offset of the first base in the file
    # .the number of bases in each fasta line
    # .the number of bytes in each fasta line
    def load_faidx(self):

        for line in self.faidx_handle:
            line = line.strip()
            cols = line.split('\t')
            chrom = cols[0]
            chrom = normalize_chrm(chrom)
            slen, offset, blen, bytelen = [int(i) for i in cols[1:]]
            self.faidx[chrom] = (slen, offset, blen, bytelen)

    # Function to fetch sequence from an indexed fasta
    # *chrom--Chromosome name (str)
    # *start--Start position (1-based) (int)
    # *end--End position (1-based) (int)
    # *keepN--Keep ambiguous bases in sequence (boolean)
    def fetch_sequence(self, chrom, start, end):

        # Fetch a sequence from start to end in 1-based coordinates
        seq = ""

        if chrom not in self.faidx:
            if chrom.startswith('chr') and chrom[3:] in self.faidx:
                chrom = chrom[3:]
            elif 'chr' + chrom in self.faidx:
                chrom = 'chr' + chrom
            else:
                # sys.stderr.write('Chromosome %s not found in reference\n' % chrom)
                raise RuntimeError('chromosome %s not found in reference' % chrom)

        slen, offset, blen, bytelen = self.faidx[chrom]
        start = start - 1  # To 0-base
        # Sanity check of start and end position
        if start < 0:
            raise RuntimeError('Sequence window out of bound--Chr: %s\tStart:%d\tEnd:%s' % (chrom, start + 1, end))
        elif end > slen and start - (end - slen) >= 0:  # end is out of bound, adjust the window towards start
            end = slen
            start = start - (end - slen)
        elif end > slen:
            raise RuntimeError('Sequence window out of bound--Chr: %s\tStart:%d\tEnd:%s' % (chrom, start + 1, end))

        if start >= end:
            raise RuntimeError('Start position %d is larger than end position %d' % (start + 1, end))

        self.fasta_handle.seek(offset + start // blen * bytelen + start % blen)

        while len(seq) < end - start:
            line = self.fasta_handle.readline().decode()
            line = line[:-1]  # Remove newline symbols
            seq = seq + line

        # chomp off extra bases
        return seq[:end - start].upper()

    def __exit__(self, type, value, traceback):
        self.fasta_fd.close()
        self.fasta_handle.close()
        self.faidx_handle.close()

    def chrm2len(self, chrm):
        slen, offset, blen, bytelen = self.faidx[chrm]
        return slen


def init_refgenome(r=None):
    global refgenome
    refgenome = RefGenome(r) if r else None


def get_seq(chrm, start, end):
    global refgenome
    return refgenome.fetch_sequence(chrm, start, end)
