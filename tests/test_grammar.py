import preamble
import unittest

from metaparse import *


class G(metaclass=cfg):

    a, b, c, d = r'abcd'

    def S(A, B, C): pass
    def S(D): pass
    def A(a, A): pass
    def A(): pass
    def B(B, b): pass
    def B(): pass
    def C(c): pass
    def C(D): pass
    def D(d, D): pass
    def D(E): pass
    def E(D): pass
    def E(B): pass


class TestGrammar(unittest.TestCase):

    def test_first0(self):
        self.assertEqual(G.FIRST0['S'], {'a', 'd', EPSILON})
        self.assertEqual(G.FIRST0['E'], {'d', EPSILON})

    def test_first_all(self):
        self.assertEqual(G.first_of_seq(['A', 'B', 'C'], '#'), {'a', 'b', 'c', 'd', '#'})

    def test_nullalbe(self):
        self.assertEqual(set(G.NULLABLE), {'S^', 'S', 'A', 'B', 'C', 'D', 'E'})

if __name__ == '__main__':
    unittest.main()
    # pass
