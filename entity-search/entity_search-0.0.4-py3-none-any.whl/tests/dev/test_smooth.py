import pytest
import colorlog
from entity_search.smooth import *
from .helpers import *

logger = colorlog.getLogger(__name__)

def test_smooth(dev_jaccard_query_response_set):
    qrs = Smooth(10).to_smooth(dev_jaccard_query_response_set)
    qrs.matrix[0, 0] == pytest.approx(2.4734e-6, 1e-6)
    qrs.matrix[1, 0] == pytest.approx(0.0090, 1e-3)
    qrs.matrix[1, 1] == pytest.approx(5.9049, 1e-6)
    qrs.matrix[2, 1] == pytest.approx(9.5367, 1e-7)
    qrs.matrix[3, 1] == pytest.approx(9.5367, 1e-7)
    qrs.matrix[4, 1] == pytest.approx(1.0, 1e-3)
    qrs.matrix[5, 1] == pytest.approx(5.499, 1e-5)
