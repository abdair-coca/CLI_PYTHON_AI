import pytest

def multi_dos(a, b):
    return a * b

def test_multi_dos_positivos():
    assert multi_dos(2, 3) == 6

def test_multi_dos_negativos():
    assert multi_dos(-2, -3) == 6

def test_multi_dos_mixtos():
    assert multi_dos(-2, 3) == -6

def test_multi_dos_cero():
    assert multi_dos(0, 3) == 0

def test_multi_dos_float():
    assert multi_dos(2.5, 3) == 7.5

def test_multi_dos_no_numeros():
    with pytest.raises(TypeError):
        multi_dos("a", 3)