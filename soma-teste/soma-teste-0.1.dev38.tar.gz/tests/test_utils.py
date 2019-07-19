
import pytest
import sys
sys.path.append("..")
import soma
import soma.estilo
from soma.estilo import format_produto_animale
from soma.estilo import connect_and_query
from soma.estilo import calculate_giro


def test_fma():
    string1 = '00.00.0000'
    string2 = 'anything'


    assert string2 == format_produto_animale(string2)
    assert string1 == format_produto_animale(string1+'A')

if __name__ == '__main__':
    pytest.main([__file__])
