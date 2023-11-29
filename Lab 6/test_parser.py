from unittest import TestCase

from grammar import Grammar
from parser import LL1


class TestLL1(TestCase):
    def setUp(self):
        self.grammar = Grammar()
        self.grammar.readFromFile("g1.txt")
        self.parser = LL1(self.grammar)
        self.parser.parse()

    def test__find_first(self):
        self.assertSetEqual(self.parser.get_first['D'], {'d', 'b'})
        self.assertSetEqual(self.parser.get_first['c'], {'c'})
        self.assertSetEqual(self.parser.get_first['A'], set())

    def test__find_follow(self):
        self.assertSetEqual(self.parser.get_follow['C'], {'b', '$'})
        self.assertSetEqual(self.parser.get_follow['D'], set())
        self.assertEqual(len(self.grammar.get_nonterminals), len(self.parser.get_follow))
        for follow in self.parser.get_follow:
            self.assertNotIn('epsilon', follow)
