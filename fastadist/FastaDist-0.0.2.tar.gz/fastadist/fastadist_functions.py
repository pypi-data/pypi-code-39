from bitarray import bitarray
import itertools
import re
from  collections import OrderedDict
from Bio import SeqIO
from multiprocessing import Pool

def create_sequence_bitarrays(sequence):
    """
    create 6 bit arrays from sequence
    Args:
        sequence (str): A nucleotide sequnce made up of characters G,A,T,C,- or N. Any other characters will be converted to N
    Returns:
        bitarrays (dict): A dictionary containing 6 bit arrays with keys G,A,T,C,- or N
    """
    # initialise bitarrays dictionary
    sequence_length = len(sequence)
    sequence = re.sub('[^GATC\-N]', 'N', sequence.upper())
    bitarrays = {
        "G": bitarray(sequence_length),
        "A": bitarray(sequence_length),
        "T": bitarray(sequence_length),
        "C": bitarray(sequence_length),
        "-": bitarray(sequence_length),
        "N": bitarray(sequence_length)
        }
    # make sure the bitarrays are zeroed
    for base in bitarrays:
        bitarrays[base].setall(False)
    for index, base in enumerate(sequence):
        bitarrays[base][index] = True

    return bitarrays

def calculate_distance(bitarray1, bitarray2):
        """
        calculate distance between two sequences encoded as bitarrays
        Args:
            bitarray1 (dict): A dictionary containing 6 bit arrays with keys G,A,T,C,- or N encoded from sequence 1
            bitarray2 (dict): A dictionary containing 6 bit arrays with keys G,A,T,C,- or N encoded from sequence 2
        Returns:
            distance (int): The distance between the two sequences
        """
        # check 2 sequences are the same length
        sequence1_length = bitarray1["G"].length()
        sequence2_length = bitarray2["G"].length()
        if sequence1_length != sequence2_length:
            exit("The two sequences must be of the same length")
        else:
            # initialise a bit array that will eventually contain the positions that are callable differences
            difference_bitarray = bitarray(sequence1_length)
            difference_bitarray.setall(False)
            # first work out distances based on G,A,T,C by applying XOR the G,A,T and C bitarrays:
            for base in ["G", "A", "T", "C"]:
                difference_bitarray = difference_bitarray | (bitarray1[base] ^ bitarray2[base])
            # next remove positions where a gap or N exists in one but not the other sequence
            for base in ["-", "N"]:
                difference_bitarray = difference_bitarray ^ (bitarray1[base] ^ bitarray2[base])
            return difference_bitarray.count()


def create_sequence_bitarrays_linked_to_id(sequence_record):
    """
    create 6 bit arrays from a biopython sequence record
    Args:
        sequence (str): A biopython sequence record
    Returns:
        bitarrays_for_sequence (tuple): A tuple of (seq_id, dict of 6 bit arrays with keys G,A,T,C,- or N)
    """
    return sequence_record.id, create_sequence_bitarrays(str(sequence_record.seq))


def create_all_sequence_bitarrays(alignment_filepath, processes = 1):
    """
    create bit arrays for all sequences in an alignment
    Args:
        alignment_filepath (str): Path to a multiple sequence alignment file in fasta format
    Returns:
        sequence_bitarray_dict (dict): A dictionary whose keys are the sequence names and values are
                                   a representation of the sequence as 6 bit arrays with keys G,A,T,C,- or N
    """
    sequence_bitarray_dict = OrderedDict() # keys sequence name, value is the sequence
    # make bit arrays
    with Pool(processes) as pool:
        all_sequence_bitarrays = pool.map(create_sequence_bitarrays_linked_to_id, SeqIO.parse(alignment_filepath, 'fasta'))
    for seq_id, sequence_bitarrays in all_sequence_bitarrays:
        sequence_bitarray_dict[seq_id] = sequence_bitarrays
    return sequence_bitarray_dict


def calculate_distance_linked_to_two_seq_ids(seq_id1, seq_id2, seq1_bitarrays, seq2_bitarrays):
    """
    Return the distance and associated seqids
    Args:
        seq_id1 (str): Id of sequence 1
        seq_id2 (str): Id of sequence 2
        seq1_bitarrays (dict): A dict for sequence 1 of 6 bit arrays with keys G,A,T,C,- or N)
        seq2_bitarrays (dict): A dict for sequence 2 of 6 bit arrays with keys G,A,T,C,- or N)
    Returns:
        seq_id1, seq_id2, distance (tuple)
    """
    return seq_id1, seq_id2, calculate_distance(seq1_bitarrays, seq2_bitarrays)

def calculate_all_distances(sequence_bitarrays, processes = 1):
    """
    calculate distances from bit arrays
    Args:
        sequence (sequence_bitarrays): A dictionary whose keys are the sequence names and values are
                                   a representation of the sequence as 6 bit arrays with keys G,A,T,C,- or N
    Returns:
        distances (dict): A dictionary containing the number of differences where the dict structure is
                          distances[seq_id1][seq_id2] = distance
    """
    distances_dict =  {}
    with Pool(processes) as pool:
        distances_tuple = pool.starmap(
            calculate_distance_linked_to_two_seq_ids,
            [
                (seq_id1, seq_id2, sequence_bitarrays[seq_id1], sequence_bitarrays[seq_id2])
                for seq_id1, seq_id2 in itertools.combinations(sequence_bitarrays.keys(),2)
            ]
        )
        for seq_id1, seq_id2, distance in distances_tuple:
            if seq_id1 not in distances_dict:
                distances_dict[seq_id1] = {}
            distances_dict[seq_id1][seq_id2] = distance
    return distances_dict

def write_distances_to_file(sequence_ids, distances, output_filepath, format = 'tsv'):
    """
    write distances to file
    Args:
        sequence_ids (list): A list of sequence ids
        distances (dict): A dictionary containing the number of differences where the dict structure is
                          distances[seq_id1][seq_id2] = distance
        output_filepath (str): The path to the output file
        format (str): One of either 'tsv' (default), 'csv' or 'phylip'
    Returns:
        None but an output file will be written
    """
    with open(output_filepath, "w") as output_file:
        # set separator
        if format in ['tsv', 'phylip']:
            separator = '\t'
        else:
            separator = ','
        
        # set header
        if format in ['csv', 'tsv']:
            header = [""]
            header.extend(sequence_ids)
            output_file.write('{0}\n'.format(separator.join(header)))
        else:
            output_file.write('{0}\n'.format(len(sequence_ids)))

        for seq_id1 in sequence_ids:
            row_elements = [seq_id1]
            for seq_id2 in sequence_ids:
                if  seq_id1 == seq_id2:
                    row_elements.append(0) # sequence vs self distance is 0
                elif seq_id1 in distances:
                    if seq_id2 in distances[seq_id1]:
                        row_elements.append(distances[seq_id1][seq_id2])
                    elif seq_id1 in distances[seq_id2]:
                        row_elements.append(distances[seq_id2][seq_id1])
                else:
                    row_elements.append(distances[seq_id2][seq_id1])

            output_file.write('{0}\n'.format(separator.join([str(x) for x in row_elements])))

def calculate_alignment_distances(alignment_filepath, output_filepath, format, processes = 1):
    """
    Write distance matrix based on sequences in an alignment
    Args:
        alignment_filepath (str): Path to a multiple sequence alignment file in fasta format
        output_filepath (str): Path to a the outputfile where the distance matrix will be written
        format (str): One of either 'tsv' (default), 'csv' or 'phylip'
    Returns:
        None but an output file will be written
    """
    sequence_bitarrays = create_all_sequence_bitarrays(alignment_filepath, processes)
    distances = calculate_all_distances(sequence_bitarrays, processes)
    write_distances_to_file(sequence_bitarrays.keys(), distances, output_filepath, format)
