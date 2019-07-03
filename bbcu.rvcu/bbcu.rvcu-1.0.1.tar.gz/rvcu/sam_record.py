import datetime
import re
import string
from ctypes import c_bool, c_int
from multiprocessing import Manager, Value


class SamReader(object):
    def __init__(self, sam_file):
        self.sam_file = sam_file
        self.sf = open(self.sam_file)
        self.first_line = Value(c_bool, True)
        self.first_chr = Value(c_bool, True)
        self.manager = Manager()
        self.sam_address_chr_intervals = self.manager.dict()  # shared memory
        self.buffer_size_of_next = Value(c_int, 0)
        self.chr_list = self.get_chr_list()  # skip on the headers lines and point to the first record in sam file

    def close_file(self):
        self.sf.close()

    def get_chr_list(self):
        chrs = []
        for line in self.sf:
            # Each interation of for loop invoke next() function that called block of data (not only one line).
            # We save the size of the block for future need.
            self.buffer_size_of_next.value = self.sf.tell()
            if not self.first_line.value and not line.startswith("@"):
                ls = line.split()
                sam_record = SamRecord(*ls[:11], tags=ls[11:])
                # save the position of the first line of first chr as first interval of the first chr
                self.sam_address_chr_intervals[sam_record.rname] = {0: 0}
                self.sf.seek(0)  # go to start of the file
                break
            if self.first_line.value and not line.startswith("@"):
                raise IOError("SAM file don't valid: SAM file must contains header lines")
            self.first_line.value = False
            chr_length = re.findall(r"@SQ\s+SN:(chr\S+)\s+LN:(\S+)", line)  # return [(chr, length)]
            if chr_length:
                chrs += chr_length
        return chrs

    # return reads that at least one part of them mapped into the chr between the [start,end] coordinates (including start and end).
    # We suppose that sam file is sorted
    # Can return reads several times, if they are mapped with gaps that each of the part falled into other interval
    def read(self, chr, chr_start, chr_end, chr_prev_start, min_mapq, max_gene_length):
        if chr in self.sam_address_chr_intervals and chr_start in self.sam_address_chr_intervals[chr]:
            self.sf.seek(self.sam_address_chr_intervals[chr][chr_prev_start])
            print "%s Start read the sam file from %s from chr %s coordinate %s" % (datetime.datetime.now(),
                                                                                    self.sam_address_chr_intervals[chr][
                                                                                        chr_prev_start], chr,
                                                                                    chr_prev_start)
            if not (chr_prev_start == 0 and self.first_chr.value):  # deny break on line in middle
                self.sf.readline()
        else:  # Not in use. To each intervael there is value in sam_address_chr_intervals
            if chr not in self.sam_address_chr_intervals:
                print "%s There are no reads on chromosome %s" % (datetime.datetime.now(), chr)
                return
            else:
                raise Exception('Cannot to be such situation')
            # return
        self.first_chr.value = False
        for l in self.sf:
            ls = l.split()
            if l.startswith("@"):
                continue
            sam_record = SamRecord(*ls[:11], tags=ls[11:])
            if sam_record.rname != chr:  # New chromosome
                if sam_record.rname not in self.sam_address_chr_intervals:
                    self.assign_shared_dict(chr, chr_end + 1,
                                            max(0, self.sf.tell() - 2 * self.buffer_size_of_next.value))
                    self.sam_address_chr_intervals[sam_record.rname] = {}
                    # go to start of the block that called by next() function (itration of the loop call to next function).
                    # At least we go back 2 blocks because maybe the start of the last line belongs to the previous block)
                    self.assign_shared_dict(sam_record.rname, 0,
                                            max(0, self.sf.tell() - 2 * self.buffer_size_of_next.value))
                    return
                else:  # The wrong chr came from the previous interval
                    continue
            else:  # mapped to chr
                if sam_record.pos > chr_end:  # The record belong to the next interval
                    self.assign_shared_dict(sam_record.rname, chr_end + 1,
                                            max(0, self.sf.tell() - 2 * self.buffer_size_of_next.value))
                    return
                umi = SamRecord.umi_from_record(sam_record)
                if SamRecord.filter_record(sam_record, umi, min_mapq, max_gene_length):
                    continue
                if sam_record.pos >= chr_start:  # i.e. sam_record <= chr_end, the record belongs to current interval
                    yield sam_record
                else:  # i.e. sam_record.pos < chr_start , the start of the record belongs to previous interval but maybe part of it belong to the current interval
                    for start_piece, end_piece in SamRecord.mapped_ref_ranges(sam_record.pos, sam_record.cigar):
                        # print 'piece', start_piece, end_piece
                        if end_piece < chr_start or start_piece > chr_end:  # this piece don't belong to current interval
                            continue
                        else:  # At least one piece of the read is mapped to current interval
                            # print start_piece, end_piece
                            # continue
                            yield sam_record
                            # break
        # If the last interval/s don't contain reads, we need to update the
        self.assign_shared_dict(chr, chr_end + 1, max(0, self.sf.tell() - 2 * self.buffer_size_of_next.value))
        # print 'end', sam_record.rname, chr_end + 1, self.buffer_size_of_next.value
        return

    def assign_shared_dict(self, basekey, key, value):
        temp = self.sam_address_chr_intervals[basekey]
        temp.update({key: value})
        self.sam_address_chr_intervals[basekey] = temp


class SamRecord(object):
    def __init__(self, qname='', flag=4, rname='*', pos=0, mapq=255, cigar='*', rnext='*', pnext=0, tlen=0, seq='*',
                 qual='*', tags=[]):
        self.qname = qname
        self.flag = int(flag)
        self.rname = rname
        self.pos = int(pos)
        self.mapq = int(mapq)
        self.cigar = cigar
        self.rnext = rnext
        self.pnext = int(pnext)
        self.tlen = int(tlen)
        self.seq = seq
        self.qual = qual
        self.tags = self.parse_sam_tags(tags)

    def decode_tag(self, tag_string):
        """ Parse a SAM format tag to a (tag, type, data) tuple. Python object
        types for data are set using the type code. Supported type codes are: A, i, f, Z, H, B

        >>> decode_tag('YM:Z:#""9O"1@!J')
        ('YM', 'Z', '#""9O"1@!J')
        >>> decode_tag('XS:i:5')
        ('XS', 'i', 5)
        >>> decode_tag('XF:f:100.5')
        ('XF', 'f', 100.5)
        """
        try:
            tag, data_type, data = tag_string.split(':', 2)
        except ValueError:
            match = re.match(r'([A-Z]{2}):([iZfHB]):(\S+)', tag_string)
            tag = match.group(1)
            data_type = match.group(2)
            data = match.group(3)
        if data_type == 'i':
            return (tag, data_type, int(data))
        elif data_type == 'Z':
            return (tag, data_type, data)
        elif data_type == 'f':
            return (tag, data_type, float(data))
        elif data_type == 'A':  # this is just a special case of a character
            return (tag, data_type, data)
        elif data_type == 'H':
            raise NotImplementedError("Hex array SAM tags are currently not parsed.")
        elif data_type == 'B':
            raise NotImplementedError("Byte array SAM tags are currently not parsed.")
        else:
            raise NotImplementedError("Tag {0} cannot be parsed.".format(tag_string))

    def parse_sam_tags(self, tagfields):
        """ Return a dictionary containing the tags """
        return dict([(tag, data) for tag, dtype, data in [self.decode_tag(x) for x in tagfields]])

    @staticmethod
    def umi_from_record(record):
        umi = record.tags['RX']
        # umi = re.findall(r"RX:Z:([AGCTN]+)", record.qname)[0]
        return umi

    @staticmethod
    def filter_record(record, umi, min_mapq, max_gene_length):
        if re.findall(r"([DSHI]+)", record.cigar):  # filter reads with mutation/insertion/softclipped/hardclipped
            return True
        if record.mapq < min_mapq:  # Mapq 10 and above is uniquely mapped
            return True
        if 'N' in umi:
            return True
        if record.tags['XF'].startswith('__'):  # filter out reads that didn't mapped to genes
            return True
        if SamRecord.map_length(record) > max_gene_length:
            return True
        else:
            return False

    @staticmethod
    # return True if the read mapped on position (not including junction)
    def read_on_position(record, position):
        md_match = re.findall(r"([0-9]+)?([MN])?", record.cigar)
        start_pos = record.pos
        for i, ref_letter in md_match:
            if i and ref_letter:
                i = int(i)
                if ref_letter == 'N':  # suppost that first is 'M' and in middle can appear 'N'
                    start_pos += (i + 1)
                elif ref_letter == 'M':
                    end_pos = start_pos + i - 1
                    if start_pos <= position and end_pos >= position:
                        return True
                    start_pos = end_pos
        return False

    @staticmethod
    def map_length(record):
        md_match = re.findall(r"([0-9]+)?([MN])?", record.cigar)
        length = 0
        for i, ref_letter in md_match:
            if i:
                length += int(i)
        return length

    @staticmethod
    def find_ref_pos_of_mis(rname, mapping_start, cigar, align_pos):  # align_pos start from 0
        # 1000,5
        cigar_match = re.findall(r"([0-9]+)([MN]+)", cigar)
        qry_aligned = -1
        ref_aligned = -1
        for i, l in cigar_match:
            i = int(i)
            if i:
                if qry_aligned < align_pos:
                    if l == 'M':
                        qry_aligned += i
                        ref_aligned += i
                    elif l == 'N':
                        ref_aligned += i
                if qry_aligned == align_pos:  # not else
                    return rname + "_" + str(mapping_start + ref_aligned), mapping_start + ref_aligned
                if qry_aligned > align_pos:
                    diff = align_pos - (qry_aligned - i)
                    ref_aligned = ref_aligned - i + diff
                    return rname + "_" + str(mapping_start + ref_aligned), mapping_start + ref_aligned

    @staticmethod
    def mutation_locations_from_md(record, filter_edge_mutations):
        mutation_locations = {}
        md = record.tags['MD']
        md_match = re.findall(r"([0-9]+)?([AGCTN])?", md)
        qry_pos = -1
        for i, ref_letter in md_match:
            if i:
                qry_pos += int(i)
            if ref_letter:
                qry_pos += 1
                if qry_pos + 1 <= filter_edge_mutations or len(record.seq) - (
                        qry_pos) <= filter_edge_mutations:  # In second condition we suppose EndToEnd mapping (all read is mapped)
                    continue
                if ref_letter == 'N' or record.seq[qry_pos] == 'N':
                    continue
                ref_pos_full_name, ref_pos_num = SamRecord.find_ref_pos_of_mis(record.rname, record.pos,
                                                                               cigar=record.cigar,
                                                                               align_pos=qry_pos)

                mutation_locations[ref_pos_num] = (ref_pos_full_name, qry_pos, ref_letter)
        return mutation_locations

    @staticmethod
    def reverse_complement_if_needed(record):
        if '-minusStrand' in record.rname:  # Already reversed in previous calling to this function on the read
            return True
        trans = string.maketrans('ATGC', 'TACG')
        max_exp = 12
        flag = record.flag
        for i in reversed(xrange(max_exp)):
            if flag - 2 ** i >= 0:
                if i == 4:
                    record.rname = record.rname + '-minusStrand'
                    record.seq = record.seq.translate(trans)
                    record.tags['MD'] = record.tags['MD'].translate(trans)
                    return True
                else:
                    flag -= 2 ** i
            else:
                if i == 4:
                    return False

    @staticmethod
    def is_record_umi_duplication(record):
        max_exp = 12
        flag = record.flag
        for i in reversed(xrange(max_exp)):
            if flag - 2 ** i >= 0:
                if i == 10:
                    return True
                else:
                    flag -= 2 ** i
            else:
                if i == 10:
                    return False

    @staticmethod
    def mapped_ref_ranges(mapping_start, cigar):
        cigar_match = re.findall(r"([0-9]+)([MN]+)", cigar)
        ranges = []
        start = mapping_start
        for i, l in cigar_match:
            i = int(i)
            if i:
                if l == 'M':
                    end = start + i - 1
                    ranges.append([start, end])
                elif l == 'N':
                    start = end + i + 1  # N must come after M, so end variable already defined
        return ranges


import sys
import math

if __name__ == "__main__":
    interval_size = 100
    max_gene_length = 200
    r = SamReader(sys.argv[1])
    print r.chr_list
    print(sys.argv[1])
    # def read(self, chr, chr_start, chr_end, chr_prev_start, min_mapq, max_gene_length):
    for chr, chr_length in r.chr_list:
        for chr_start in xrange(0, int(chr_length), interval_size):
            # minus epsilon for the case that max_gene_length and interval_size are equal
            intervals_num = math.floor(float(max_gene_length) / interval_size + 1 - 0.000000001)
            chr_prev_start = int(max(0, chr_start - intervals_num * interval_size))
            chr_end = chr_length if chr_length == chr_start + interval_size else min(chr_length,
                                                                                     chr_start + interval_size - 1)

            print 'chr: %s start: %s, end: %s, prev: %s, interval_s: %s, interval_num: %s' % (
                chr, chr_start, chr_end, chr_prev_start, interval_size, intervals_num)
            for i in r.read(chr=chr, chr_start=chr_start, chr_end=chr_end, chr_prev_start=chr_prev_start, min_mapq=0,
                            max_gene_length=max_gene_length):  # int(sys.argv[2])):
                print i.rname, i.pos

    # for i in r.read("chr1", 0, 2000, 0, 0, 100000000000000000):  # int(sys.argv[2])):
    #     print i.rname, i.pos
    # for i in r.read("chr1", 2001, 3000, 0, 0, 100000000000000000):  # int(sys.argv[2])):
    #     print i.rname, i.pos
    # for i in r.read("chr2", 0, 2000, 0, 0, 100000000000000000):  # int(sys.argv[2])):
    #     print i.rname, i.pos
    # for i in r.read("chr2", 2001, 3000, 0, 0, 100000000000000000):  # int(sys.argv[2])):
    #     print i.rname, i.pos
