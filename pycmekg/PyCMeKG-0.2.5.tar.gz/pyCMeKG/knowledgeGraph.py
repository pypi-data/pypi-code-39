import os
import _pickle as pkl

class KnowledgeGraph(object):

    def __init__(self, file_name = "cmekg.pkl"):

        pfile = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "model", file_name,
        )

        with open(pfile, "rb") as f:
            self.db_dic = pkl.load(f)

    def query_by_subject(self, subject_name = None):
        """A list of (subject, predicate, object) tuples for the given subject"""

        dic = {}
        if subject_name in self.db_dic.keys():
            dic = self.db_dic[subject_name]

        triples = []

        for key in dic.keys():
            if isinstance(dic[key], list):
                for val in dic[key]:
                    triple = (subject_name, key, val)
                    triples.append(triple)

        return triples

    def query_by_subject_predicate(self, subject = None, predicate = None):
        """A list of (subject, predicate, object) tuples for the given subject, predicate"""

        dic = {}
        if subject in self.db_dic.keys():
            dic = self.db_dic[subject]

        triples = []
        if predicate in dic.keys():
            for val in dic[predicate]:
                triple = (subject, predicate, val)
                triples.append(triple)

        return triples


if __name__ == "__main__":
    print("ok")
    kg = KnowledgeGraph()
    ls = kg.query_by_subject("支气管肺癌")
    print(ls)
    print("end")






