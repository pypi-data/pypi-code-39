import _pickle as pkl
from pyCMeKG.knowledgeGraph import KnowledgeGraph

class cmekg(object):
    def __init__(self, db_file = "cmekg.pkl"):
        self.model =KnowledgeGraph(db_file)

    def subject(self, subject_name = None):
        """query by subject"""
        return self.query_by_subject(subject_name)

    def subject_predicate(self, subject_name = None, predicate_name = None):
        """query by subject, predicate"""
        return self.query_by_subject_predicate(subject_name, predicate_name)

