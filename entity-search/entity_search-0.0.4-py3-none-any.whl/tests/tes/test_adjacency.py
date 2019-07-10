import pytest
import colorlog
import sparse
from entity_search.adjacency import Compressor, EqualWeight, PfitfWeight, ExclusivityWeight
from entity_search.utilities import read_adjacency_file
from .helpers import *

#TODO: Computing Pfitf over a small real-world dataset is very slow.
#@pytest.mark.parametrize("schema", [(EqualWeight), (PfitfWeight), (ExclusivityWeight)])
@pytest.mark.parametrize("schema, name", [(EqualWeight, 'eqv'), (ExclusivityWeight, 'excl')])
def test_adjacency_init(tes_adjacency_path, schema, name):
    w = schema(read_adjacency_file(tes_adjacency_path))
    assert w.tensor.shape == (6221, 6221, 115)
    assert w.tensor.nnz == 6708
    assert str(w) == name
    c = Compressor(w)
    assert c.tensor.shape == (6221, 6221)
    assert c.tensor.nnz == 6595
    assert str(c) == name

