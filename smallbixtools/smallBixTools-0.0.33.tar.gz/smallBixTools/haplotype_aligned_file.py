from collections import defaultdict
import argparse
import smallBixTools as st


def haplo_with_freq_aligned_file(infile, outfile, dp):
    '''
    Haplotypes an aligned fasta file. Each unique sequence is included once. The last sequence id in
    the file associated with a unique sequence is used as the seqid in the outfile.
    Frequencies are included on the sequence id, appended to the seqid as an underscore then frequency.
    eg: _0.743
    Three decimal places are included.
    :param infile: The .fasta formatted file to be haplotyped
    :param outfile: The full path and filename to write the haplotyped .fasta file to.
    :return: No return.
    '''
    print("Haplotyping the aligned input file: {}".format(infile))
    dct = st.fasta_to_dct(infile)

    total_seqs = len(dct)
    print("Input file has {} sequences".format(total_seqs))

    # adding seqids with same seq to same elements in dict
    rev_haplo_dct = {}
    for seqid, seq in dct.items():
        if seq not in rev_haplo_dct.keys():
            rev_haplo_dct[seq] = {'seqids': [seqid]}
        else:
            rev_haplo_dct[seq]['seqids'].append(seqid)

    # Counting seqids per sequence, calculate frequency, assign new seqid
    haplo_dct = {}
    for seq, seqids_lst in rev_haplo_dct.items():
        this_seq_freq = len(seqids_lst['seqids']) / total_seqs
        new_seqid = seqids_lst['seqids'][-1] + "_{}".format(round(this_seq_freq, dp))
        haplo_dct[new_seqid] = seq

    st.dct_to_fasta(haplo_dct, outfile)
    print("Output file has {} sequences".format(len(haplo_dct)))
    print("Completed. Written to file: {}".format(outfile))


def haplo_aligned_file(infile, outfile):
    '''
    Haplotypes an aligned fasta file. Each sequence which is the same is only included once. The last sequence id in
    the file associated with this sequence is used as the seqid in the outfile.
    :param infile: The .fasta formatted file to be haplotyped
    :param outfile: The place to write the haplotyped .fasta file to on disc.
    :return: No return.
    '''
    print("Haplotyping the aligned input file: {}".format(infile))
    dct = st.fasta_to_dct(infile)
    print("Input file has {} sequences".format(len(dct)))
    rev_haplo_dct = {}
    haplo_dct = {}
    for k, v in dct.items():
        rev_haplo_dct[v] = k
    for k, v in rev_haplo_dct.items():
        haplo_dct[v] = k
    st.dct_to_fasta(haplo_dct, outfile)
    print("Output file has {} sequences".format(len(haplo_dct)))
    print("Completed. Written to file: {}".format(outfile))


def main(infile, outfile, freq, dp):
    if freq:
        haplo_with_freq_aligned_file(infile, outfile, dp)
    else:
        haplo_aligned_file(infile, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Haplotypes the aligned input file.')
    parser.add_argument('-in', '--infile', type=str,
                        help='An aligned fasta file', required=True)
    parser.add_argument('-out', '--outfile', type=str,
                        help='A place to write the aligned haplotyped version of the input file.', required=True)
    parser.add_argument('-f', '--withFreq', type=bool,
                        help='Include frequecies on the output seqids?', required=False, default=True)
    parser.add_argument('-dp', '--decimalPoints', type=int,
                        help='How many decimal points to round to on frequencies?', required=False, default=3)

    args = parser.parse_args()
    infile = args.infile
    outfile = args.outfile
    freq = args.withFreq
    dp = args.decimalPoints

    main(infile, outfile, freq, dp)
