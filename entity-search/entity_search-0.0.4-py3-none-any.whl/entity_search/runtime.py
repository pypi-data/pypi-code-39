import numpy as np
from scipy import stats
from . import preprocessing
from . import katz
from . import bfs
import time
from functools import reduce

def get_adjacency_for_knowledge_graph(base_path, kg_path, schema = 0):
    K, _ = get_adjacency_for_knowledge_graph_and_lemmas(base_path, kg_path, schema = 0)
    return K

def get_adjacency_for_knowledge_graph_and_lemmas(base_path, kg_path, schema = 0):
    K, lemmas, _ = get_adjacency_for_knowledge_graph_and_lemmas_and_triples(base_path, kg_path, schema)
    return (K, lemmas)

def get_adjacency_for_knowledge_graph_and_lemmas_and_triples(base_path, kg_path, schema = 0):
    wn31_path = base_path + kg_path
    wn31 = preprocessing.TripleSet()
    wn31.load(wn31_path + '/triples')
    triples = np.sort(wn31.triples, order = ['f2'])
    lemmas = preprocessing.LemmaDict()
    lemmas.load(wn31_path + '/lemma_dict')
    # Computing transition matrix
    adjacencies = katz.triples_to_adjacencies(triples, schema)
    A = katz.collapse_matrices(adjacencies)
    A = A + A.T
    return (katz.normalise(A), lemmas, triples)

def get_bfs_and_adjacency_and_triples_and_lemmas(base_path, kg_path, schema):
    wn31_path = base_path + kg_path
    wn31 = preprocessing.TripleSet()
    wn31.load(wn31_path + '/triples')
    triples = np.sort(wn31.triples, order = ['f2'])
    lemmas = preprocessing.LemmaDict()
    lemmas.load(wn31_path + '/lemma_dict')
    # Computing transition matrix
    adj = katz.triples_to_adjacencies(triples, schema)
    sbfs = bfs.SimpleBFS(triples)
    return (sbfs, adj, lemmas, triples)

def measure_katz_operator(base_path, kg_path, schema, beta, t_max):
    start_time = time.time()
    T = get_adjacency_for_knowledge_graph(base_path, kg_path)
    ini_time = (time.time() - start_time)*1000
    start_time = time.time()
    K = katz.katz_operator(T, beta, t_max)
    katz_time = (time.time() - start_time)*1000
    return (beta, t_max, ini_time, katz_time)

def load_groundtruth(base_path, gt_name, lemmas):
    gt_file = base_path + "/" + gt_name + ".txt"
    gt_scores = preprocessing.preprocess_groundtruth(gt_file, lemmas.dict)
    gt_ranking = stats.rankdata(gt_scores['f2'], method='min')
    return (gt_scores, gt_ranking)

def measure_katz_query(base_path, kg_path, schema, beta, t_max, base_path_gt, gt_name):
    T, lemmas = get_adjacency_for_knowledge_graph_and_lemmas(
        base_path, kg_path, schema)
    K = katz.katz_operator(T, beta, t_max)
    gt_scores, gt_ranking = load_groundtruth(base_path_gt, gt_name, lemmas)
    output = []
    for id1, id2, _ in gt_scores:
        start_time = time.time()
        score = K[id1, id2]
        end_time = (time.time() - start_time)*1000
        output.append((beta, t_max, id1, id2, end_time))
    return output

def measure_path_query(base_path, kg_path, schema, beta, t_max, base_path_gt, gt_name):
    sbfs, adj, lemmas, triples = get_bfs_and_adjacency_and_triples_and_lemmas(
        base_path, kg_path, schema)
    gt_scores, gt_ranking = load_groundtruth(base_path_gt, gt_name, lemmas)
    output = []
    for id1, id2, _ in gt_scores:
        start_time = time.time()
        if id1 != id2:
            ps = bfs.PathSet(sbfs.find_paths(id1, id2, t_max), triples)
            scores = [path.score(beta, adj) for path in ps.unique_paths()]
            score = reduce(np.add, scores)
        else:
            score = 1
        end_time = (time.time() - start_time)*1000
        output.append((beta, t_max, id1, id2, end_time))
    return output