import pytest
from scipy import integrate
import numpy as np

def trie(f, a, b):
    return integrate.quad(f, a, b)[0]

def test_trie():
    def f(x):
        return x**2
    a = 0
    b = 1
    assert np.isclose(trie(f, a, b), 1/3)

def test_trie_lineal():
    def f(x):
        return 2*x + 1
    a = 0
    b = 1
    assert np.isclose(trie(f, a, b), 2)

def test_trie_constante():
    def f(x):
        return 2
    a = 0
    b = 1
    assert np.isclose(trie(f, a, b), 2)

def test_trie_exponencial():
    def f(x):
        return np.exp(x)
    a = 0
    b = 1
    assert np.isclose(trie(f, a, b), np.exp(1) - 1)

def test_trie_error():
    def f(x):
        return x**2
    a = 1
    b = 0
    with pytest.raises(ValueError):
        trie(f, a, b)