import numpy as np
from collections import deque
from itertools import chain, repeat

class SimpleBFS(object):
    """
    Simple BFS for triple-based graph. 
    It uses a queue to keep track of the paths 
    """
    
    def __init__(self, triples):
        self.triples = triples
        
    def neighbours_subjects(self, x):
        """
        Find neighbours that are subjects to x
        """
        return self.triples[np.where(self.triples['f0'] == x)[0]]['f1']
    
    def neighbours_objects(self, x):
        """
        Find neighbours that are objects to x
        """
        return self.triples[np.where(self.triples['f1'] == x)[0]]['f0']
    
    def neighbours(self, x):
        """
        Find neighbours (objects and subjects) for x
        """
        #subjects
        subjects = self.neighbours_subjects(x)
        #objects
        objects = self.neighbours_objects(x)
        # Concatenate and unique
        all_ = np.concatenate((objects, subjects))
        #all_.sort()
        return np.unique(all_)

    def find_paths(self, x, y, hop):
        """
        Find any proto paths (vertex-vertex connections) between x and
        y such that their length is less or equal to hop.
        """
        # Place to store proto_paths
        solutions = []
        initial_path = np.array([x], dtype = 'u4')
        path_queue = deque([initial_path])
        
        # This is just to speed up comparison between ids. 
        # It is faster to check if an id is in set y_set.
        y_set = set([y])
        
        # Main loop. For each path in the queue, find new paths.
        while len(path_queue) > 0:
            path = path_queue.pop()
            if path is None or len(path) > hop :
                break
            latest_vertex_id = path[len(path)-1]
            path_list = path.tolist()
            path_set = set(path_list)
            
            # Find new paths using neighbours
            new_paths = np.array(
                [(np.array(path_list + [vertex_id], dtype ="u4"),  
                  vertex_id in y_set)
                  for vertex_id in self.neighbours(latest_vertex_id)
                  if not vertex_id in path_set], 
                dtype = "object,bool")
            # Find solutions
            solutions.extend( new_paths['f0'][ new_paths['f1'] == True])
            path_queue.extendleft( new_paths['f0'][ new_paths['f1'] == False])
        return solutions
    
class PathSet(object):
    """
    Paths produced by find_paths
    """
    def __init__(self, pr_paths, triples):
        self.pr_paths = pr_paths
        self.triples = triples
        self.paths = None
        #self.printer = PathPrinter(self)
        
    def _search_in_triples(self, id1, id2):
        ts = self.triples[np.where(self.triples['f0'] == id1)[0]]
        return ts[np.where(ts['f1'] == id2)[0]]
    
    def as_list(self):
        """
        Find paths (vertex-edge_type-vertex connections) between x and y
        such that their length is less or equal to hop.
        """
        if self.paths is None:
            path_set_predicate_list = [
                np.array([
                    # Search for any linking between i and i+1
                    np.array(
                        [p for s,o,p in self._search_in_triples(path[i], path[i+1])] +
                        [p for s,o,p in self._search_in_triples(path[i+1], path[i])],
                        dtype = "u4")
                    for i in range(0, len(path) - 1)], 
                    dtype = "object")
                for path in self.pr_paths ]
            self.paths = list(zip(self.pr_paths, path_set_predicate_list))
        return self.paths
    
    def count_paths(self):
        """
        Count Paths according to their lengths
        """
        paths = self.as_list()
        return sum_by(np.array(
            [ ( len(vertices), np.prod([len(edge) for edge in edges]) ) 
                for vertices, edges in paths]
               , dtype = "u4,u4"))
    
    def unique_paths(self):
        paths = self.as_list()
        if len(paths) == 0:
            return [ Path([], []) ]
        ex_paths = []
        for seq, rels in paths:
            ex_rels = []
            max_rel = [len(rel) for rel in rels]
            number = np.zeros((len(max_rel)), dtype = "u4")
            ex_rels = []
            for i in range(0, np.prod(max_rel)):
                for j in range(len(max_rel)):
                    if number[j] >= max_rel[j]:
                        number[j] = 0
                        number[j+1] += 1
                digit = [ rels[k][number[k]] for k in range(len(number)) ]
                ex_rels.append(digit)
                number[0] += 1
            ex_paths.extend( [ Path(seq, rel) for rel in ex_rels])
        return ex_paths
                
class Path(object):
    def __init__(self, seq, rel):
        self.seq = seq
        self.rel = rel
        self.length = len(rel)
    
    def score(self, beta, adj):
        triples = [(self.seq[i],self.seq[i+1],self.rel[i]) 
                for i in range(self.length)]
        #print(triples)
        out = 0;
        for x,y,z in triples:
            if adj[z][x,y] > 0:
                out += adj[z][x,y]
            else:
                out += adj[z][y,x]
        return out*np.power(beta, self.length)