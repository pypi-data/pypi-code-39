#def find_synset_with_relationships(synset_set):
#    """
#    Find synsets that do have relationships
#    """
#    synset_no_pointer = np.array([ synset.id  for synset in synset_set 
#                  if len(synset.pointers.list) == 0 ])
#    synset_not_pointed = np.unique([ _id  for synset in synset_set 
#                        for _type, _id, ad in synset.pointers.list])
#    synset_ids = np.array(list(range(0, len(synset_set))))
#    synset_pointed = np.setdiff1d(synset_ids, synset_not_pointed)
#    synset_no_pointer_not_pointed = np.intersect1d(synset_pointed, 
#                                                   synset_no_pointer)
#    return np.setdiff1d(synset_ids, synset_no_pointer_not_pointed)


from functools import reduce
import numpy as np
import scipy as sp
from .utilities import Serialiser, Parser, Dict, StrAndInt, StrAndStr
from .katz import group_by

class WordList(object):
    """
    It represents a list of word for a given synset
    """
    def __init__(self, entry):
        words = entry[::2]
        lex_ids = entry[1::2]
        self.list = list(zip(words, lex_ids))
        
class PointerList(object):
    """
    It contains the pointers of the relationships of a synset
    """
    def __init__(self, entry, ids):
        symbols = entry[::4]
        offsets = entry[1::4]
        pos = entry[2::4]
        targets = entry[3::4]
        _ids = [ ids[o + p] for o, p in zip(offsets, pos)]
        self.list = list(zip(symbols, _ids, targets))

class Synset(object):
    """
    Synset is a meaning that many word might refer to it.
    """
    def __init__(self, entry, ids):
        items = entry.split()
        self.id = ids[get_synset_id(items)]
        self.key = items[0] + items[2]
        self.lexfilenum = int(items[1])
        self.w_cnt = int(items[3], 16)
        self.words = WordList(items[4:self.w_cnt*2+4])
        w = 4+2*(self.w_cnt)
        self.p_cnt = int(items[w])
        w += 1
        self.pointers = PointerList(items[w:self.p_cnt*4+w], ids)
        
    def __str__(self):
        return self.words
    
class Entry(object):
    """
    Entry in the index file
    """
    def __init__(self, entry, ids):
        items = entry.split()
        self.word = items[0]
        self.pos = items[1]
        self.synset_cnt = int(items[2])
        self.pointer_cnt = int(items[3])
        self.pointer_symbols = items[4:self.pointer_cnt + 4]
        w = 4 + self.pointer_cnt + 2
        self.synsets = [ids[synset_id + self.pos] 
                        for synset_id in items[w:self.synset_cnt + w]]

def get_synset_id(data_entry, *args):
    if type(data_entry) == str:
        data_entry = data_entry.split()
    if data_entry[2] != "s":
        return data_entry[0] + data_entry[2]
    else:
        return data_entry[0] + 'a'

class PreprocessingWordnet(Parser):
    """
    Preprocess wordnet files presented in base_path.
    It generates an id dictionary (for wordnet_ids to simple ids), a list of
    synsets and a word (lemma) dictionary
    """
    extensions = ['adv', 'adj', 'noun', 'verb']
    relationships = [
        "!",   # Antonym
        "@",   # Hypernym
        "@i",  # Instance Hypernym
        "~",   # Hyponym
        "~i",  # Instance Hyponym 
        "#m",  # Member holonym 
        "#s",  # Substance holonym 
        "#p",  # Part holonym 
        "%m",  # Member meronym 
        "%s",  # Substance meronym
        "%p",  # Part meronym 
        "&",   # Similar to 
        "<",   # Participle of verb 
        "\\",  # Pertainym (pertains to noun) || Derived from adjective
        "=",   # Attribute
        "*",   # Entailment 
        ">",   # Cause 
        "^",   # Also see 
        "$",   # Verb Group 
        "+",   # Derivationally related form         
        ";c",  # Domain of synset - TOPIC 
        "-c",  # Member of this domain - TOPIC 
        ";r",  # Domain of synset - REGION 
        "-r",  # Member of this domain - REGION 
        ";u",  # Domain of synset - USAGE 
        "-u",  # Member of this domain - USAGE
        ]
    
    def __init__(self):
        pass
    
    def preprocess(self, base_path):
        """
        Given a base_path, extract the ids, synsets and dictionary of lemmas
        for any wordnet file present in base_path
        """
        self.files = np.array([(base_path + "/data." + ext, 
                                base_path + "/index." + ext ) 
                      for ext in self.extensions], dtype = "O,O")
        ids = self.parse(self.files['f0'], get_synset_id)
        self.id_dict = SynsetIdDict(ids)
        self.synsets = self.parse(self.files['f0'], Synset, self.id_dict.dict)
        indices = self.parse(self.files['f1'], Entry, self.id_dict.dict)
        self.lemma_dict = LemmaDict(indices)
        self.rel_dict = { self.relationships[i]: i 
                         for i in range(0, len(self.relationships))}
    
    def make_triples(self):
        """
        Transform a synset set into a set of triples
        """
        triples = np.array([(synset.id, pointer[1], self.rel_dict[pointer[0]] ) 
            for synset in self.synsets for pointer in synset.pointers.list], 
            dtype = "u4,u4,u2")
        ts = TripleSet()
        ts.triples = triples
        return ts
    
class SynsetIdDict(Dict):
    def __init__(self, ids = None):
        tuples = []
        if ids is not None:
            tuples = [(old_id, new_id) for old_id, new_id in zip(ids, range(len(ids))) ]
        super().__init__(StrAndInt, tuples)

class LemmaDict(Dict):
    def __init__(self, entries = None):
        tuples = []
        if entries is not None:
            tuples = [ (entry.word + "." + entry.pos + "." + str(i+1).zfill(2), 
                entry.synsets[i] )
                for entry in entries for i in range(len(entry.synsets))]
        super().__init__(StrAndStr, tuples)
    
class Triple(object):
    """
    simple triple
    """
    def __init__(self, entry, *argv):
        self.values = tuple(entry.split(','))

class TripleSet(Serialiser, Parser):
    """
    Class that define a triple set. It can store triples as well as 
    load them from/into a text file
    """
        
    def store(self, file_path):
        """
        Save triples into file_path as text
        """
        self.serialise(self.triples, file_path)
        
    def load(self, file_path):
        """
        Load triples from text
        """
        self.triples = self.parse([file_path], Triple)
        self.triples = np.array([t.values for t in self.triples], 
                                dtype = 'u4,u4,u2')
        
    def print_statistics(self):
        """
        Print triple set statistics
        """
        l_triples = len(self.triples)
        uni_edges = len(np.unique(self.triples['f2']))
        uni_vertices = len(np.union1d(np.unique(self.triples['f1']), 
                                      np.unique(self.triples['f0'])))
        print("Total triples %d" % l_triples)
        print("unique edges %d" %uni_edges)
        print("unique vertices %d" % uni_vertices)
        out_degree = group_by(self.triples['f0'])
        max_out_degree = np.max(out_degree['f1'])
        ave_out_degree = np.average(out_degree['f1'])
        print("max out degree %d" % max_out_degree)
        print("average out degree %f" % ave_out_degree)
        in_degree = group_by(self.triples['f1'])
        max_in_degree = np.max(in_degree['f1'])
        ave_in_degree = np.average(in_degree['f1'])
        print("max in degree %d" % max_in_degree)
        print("average in degree %f" % ave_in_degree)
        degree = group_by(np.concatenate((self.triples['f0'], 
                                          self.triples['f1'])))
        max_degree = np.max(degree['f1'])
        ave_degree = np.average(degree['f1'])
        print("max degree %d" % max_degree)
        print("average degree %f" %ave_degree)

class Sense(object):
    """
    A sense is a tuple of word, pos and num
    """
    def __init__(self, sense):
        items = sense.split('#')
        self.word = items[0].lower()
        self.pos = items[1]
        self.num = int(items[2])
    
    def __str__(self):
        return self.word + "." + self.pos + "." + str(self.num).zfill(2)

def read_senses(file_path):
    """
    Read senses pairs from file
    """
    with open(file_path) as f:
        lines = f.readlines()
    return [ tuple(line.split()) for line in lines]

def format_senses(senses):
    """
    Set format for the senses
    """
    return [ (str(Sense(s1)), str(Sense(s2)), float(value) )
            for s1, s2, value in senses]

def senses_to_ids(senses, word_dict):
    """
    Use ids found in adjacency matrix
    """
    return np.array([ (word_dict[s1], word_dict[s2], value) 
            for s1, s2, value in senses], dtype="u4,u4,f")

def preprocess_groundtruth(file_path, word_dict):
    return senses_to_ids(format_senses(read_senses(file_path)), word_dict)