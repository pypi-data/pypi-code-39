import pytest
import colorlog
import sparse
import numpy as np
import scipy as sp
from entity_search.math import *
from gensim.matutils import corpus2csc
from .helpers import *

def test_corpus2sparse_plain(tes_json_multi_field_corpus):
    s = corpus2sparse(tes_json_multi_field_corpus.fields[0])
    assert s.shape == (19949, 6221)
    assert s.nnz == 15249

def test_corpus2sparse_mm(tes_mm_multi_field_corpus):
    s = corpus2sparse(tes_mm_multi_field_corpus.fields[0])
    assert s.shape == (19949, 6221)
    assert s.nnz == 15249
