import numpy as np 
from dragonn.utils import one_hot_encode, get_sequence_strings
import pdb
from collections import defaultdict
from random import shuffle


#compile the dinucleotide edges
def prepare_edges(s):
    edges = defaultdict(list)
    for i in range(len(s)-1):
        edges[tuple(s[i])].append(s[i+1])
    return edges


def shuffle_edges(edges):
    #for each character, remove the last edge, shuffle, add edge back
    for char in edges:
        last_edge = edges[char][-1]
        edges[char] = edges[char][:-1]
        the_list = edges[char]
        shuffle(the_list)
        edges[char].append(last_edge)
    return edges


def traverse_edges(s, edges):
    generated = [s[0]]
    edges_queue_pointers = defaultdict(lambda: 0)
    for i in range(len(s)-1):
        last_char = generated[-1]
        generated.append(edges[tuple(last_char)][edges_queue_pointers[tuple(last_char)]])
        edges_queue_pointers[tuple(last_char)] += 1
    if isinstance(generated[0],str):
        return "".join(generated)
    return np.asarray(generated)


def dinuc_shuffle(s):
    if isinstance(s, str):
        s=s.upper()
    return traverse_edges(s, shuffle_edges(prepare_edges(s)))
        
    

#seqs=['ACGTACGTACGTCGCGCGATATAT','ACGTACGTACGTCGCGCGATATAT']
#encoded=one_hot_encode(seqs)
#shuffled=[dinuc_shuffle(encoded[i].squeeze()) for i in range(encoded.shape[0])]
#shuffled=np.expand_dims(np.asarray(shuffled),axis=1)
#decoded=get_sequence_strings(shuffled)
#print(seqs)
#print(decoded) 
#from_string=dinuc_shuffle(seqs[0])
#print(from_string)

