import yaml
import os

cfg = None
if cfg is None:
    m_path = os.path.dirname(os.path.realpath(__file__))
    config_path = "{}/../etc/config.yaml".format(m_path)
    with open(config_path, 'r') as f:
        cfg = yaml.load(f)

# Formats used to transform corpora
class Formats(object):
    raw = "raw"
    binary = "binary"
    cosine = "cosine"
    bm25 = "bm25"

# URIs to filter from output
expressions = ['<dbpedia:Category:',
               'http://www.w3.org/2002/07/owl',
               'http://dbpedia.org/ontology',
               'http://www.wikidata.org',
               'http://www.ontologydesignpatterns.org',
               'http://schema.org',
               'http://www.w3.org/2004/02/skos']
# Types of diffusions
diffusions = ['hpprankpi','hprankpi','pprankpi','prankpi','katzpi','text']
# Types of queries
queries = [
    ('SemSearch_ES', ['SemSearch_ES']),
    ('INEX_LD', ['INEX_LD']),
    ('ListSearch', ['SemSearch_LS','INEX_XER', 'TREC_Entity']),
    ('QALD-2', ['QALD2_te', 'QALD2_tr']) ]
# Generat type of queries
query_types = [ query_type for query_type, _ in queries]

# Functions for names and paths
def make_name(prefix, suffix, sep = '-'):
    return "{}{}{}".format(prefix, sep, suffix)

def make_path(base_path, name, extension = None):
    if extension:
        return "{}/{}.{}".format(base_path, name, extension)
    return "{}/{}".format(base_path, name)

class Environment(object):
    corpus_suffix = "text"
    corpus_extension = "json.bz2"
    corpus_extension_mm = "mm"
    mapping_suffix = "mapping"
    mapping_extension = "csv.bz2"
    adjacency_suffix = "adjacency"
    adjacency_extension = "csv.bz2"
    query_suffix = "queries"
    query_extension = "txt"
    groundtruth_suffix = "qrels"
    groundtruth_extension = "txt"
    index_suffix = "index"
    index_extension = "pkl"
    result_suffix = "result"
    result_extension = "pkl"
    transition_suffix = "transition"
    transition_extension = "pkl"
    def __init__(self, dataset_path, dataset_name, query_path, query_name, groundtruth_name,
            output_path):
        # Main paths
        self.dataset_path = dataset_path
        self.query_path = query_path
        try:
            os.mkdir(output_path)
        except FileExistsError as e:
            print('Directory exists?')
        self.output_path = output_path
        # Names
        self.dataset_name = dataset_name
        self.corpus_name = make_name(dataset_name, self.corpus_suffix)
        self.mapping_name = make_name(dataset_name, self.mapping_suffix)
        self.adjacency_name = make_name(dataset_name, self.adjacency_suffix)
        self.query_name = query_name
        self.groundtruth_name = groundtruth_name
        result_name = make_name(query_name, self.result_suffix)
        self.result_name = result_name
        self.transition_name = make_name(dataset_name, self.transition_suffix)
        # Files
        self.corpus_file = make_path(dataset_path, self.corpus_name, self.corpus_extension)
        self.mapping_file = make_path(dataset_path, self.mapping_name, self.mapping_extension)
        self.adjacency_file = make_path(dataset_path, self.adjacency_name, self.adjacency_extension)
        self.query_file = make_path(query_path, self.query_name, self.query_extension)
        self.groundtruth_file = make_path(query_path, self.groundtruth_name, self.groundtruth_extension)
        # Output names
        self.raw_corpus_name = make_name(dataset_name, Formats.raw, sep = '.')
        self.binary_corpus_name = make_name(dataset_name, Formats.binary, sep = '.')
        self.cosine_corpus_name = make_name(dataset_name, Formats.cosine, sep = '.')
        self.bm25_corpus_name = make_name(dataset_name, Formats.bm25, sep = '.')
        self.binary_query_name = make_name(query_name, Formats.binary, sep = '.')
        self.cosine_query_name = make_name(query_name, Formats.cosine, sep = '.')
        self.bm25_query_name = make_name(query_name, Formats.bm25, sep = '.')
        self.binary_result_name = make_name(result_name, Formats.binary, sep = '.')
        self.cosine_result_name = make_name(result_name, Formats.cosine, sep = '.')
        self.bm25_result_name = make_name(result_name, Formats.bm25, sep = '.')
        # Output files
        self.mm_raw_corpus_file = make_path(output_path, self.raw_corpus_name)
        self.mm_binary_corpus_file = make_path(output_path, self.binary_corpus_name)
        self.mm_cosine_corpus_file = make_path(output_path, self.cosine_corpus_name)
        self.mm_bm25_corpus_file = make_path(output_path, self.bm25_corpus_name)
        self.raw_index_file = make_path(output_path, self.raw_corpus_name, self.index_extension)
        self.binary_index_file = make_path(output_path, self.binary_corpus_name, self.index_extension)
        self.cosine_index_file = make_path(output_path, self.cosine_corpus_name, self.index_extension)
        self.bm25_index_file = make_path(output_path, self.bm25_corpus_name, self.index_extension)
        self.mm_binary_query_file = make_path(output_path, self.binary_query_name)
        self.mm_cosine_query_file = make_path(output_path, self.cosine_query_name)
        self.mm_bm25_query_file = make_path(output_path, self.bm25_query_name)
        self.binary_result_file = make_path(output_path, self.binary_result_name, self.result_extension)
        self.cosine_result_file = make_path(output_path, self.cosine_result_name, self.result_extension)
        self.bm25_result_file = make_path(output_path, self.bm25_result_name, self.result_extension)
        self.transition_file = make_path(output_path, self.transition_name, self.transition_extension)
        # Others
        self.fields = ["name", "attributes", "categories", "similar", "related"]
