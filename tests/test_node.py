"""Test Node class."""
from typing import List, Sequence
from unittest import TestCase
from unittest.mock import MagicMock

from browscapy.database import Database
from browscapy.node import FullPattern, Parent, PartialPattern, Tree
from browscapy.properties import Properties


class TestNode(TestCase):
    """Test Nodes with browscap patterns."""

    @classmethod
    def setUpClass(cls) -> None:
        """Mock the database."""
        Database.dictionary = MagicMock()

    def test_add_nodes(self) -> None:
        """Add 2 nodes with a common prefix."""
        patterns = 'Mozilla/4.0 Test', 'Mozilla/5.0 Test'
        self._test_addition(patterns, ['Mozilla/'], patterns)

    def test_add_nodes_no_prefix(self) -> None:
        """Should have 2 children in the first level."""
        patterns = 'Mozilla/4.0 Test', 'curl/7.52.1'
        self._test_addition(patterns, patterns)

    def test_add_same_patterns(self) -> None:
        """Shouldn't add 2 nodes with the same prefix."""
        node1 = self._get_full_pattern('Mozilla/4.0 Test')
        node2 = self._get_full_pattern('Mozilla/4.0 Test')
        tree = Tree()
        tree.add_node(node1)
        self.assertRaises(ValueError, lambda: tree.add_node(node2))

    def test_add_suffixed_pattern(self) -> None:
        """Should add normally if the other pattern has extra chars."""
        self._test_addition(['One', 'One Two'], ['One'], ['One Two'])

    def test_first_grandchild(self) -> None:
        """Should add this node as a grandchild."""
        self._test_addition(['One', 'One Two', 'One Two Three'],
                            ['One'], ['One Two'], ['One Two Three'])

    def test_second_child(self) -> None:
        """Add a node as a second child."""
        self._test_addition(['One', 'OneTwo', 'OneFour'],
                            ['One'], ['OneTwo', 'OneFour'])

    def test_add_two_children(self) -> None:
        """Add two siblings in the first level."""
        tree = self._add_patterns('a', 'b')
        self.assertEqual(2, len(tree.children))

    def test_add_longer_than_partial(self) -> None:
        """Should add a full pattern as child of a shorter partial pattern."""
        tree = self._add_patterns('ab', 'ac', 'ad')
        child = tree.children[0]
        self.assertIsInstance(child, PartialPattern)
        self.assertEqual('a', child.pattern)
        self.assertEqual('ad', child.children[2].pattern)

    def test_partial_becomes_full(self) -> None:
        """If a partial pattern equals a full one, change it to full."""
        tree = self._add_patterns('ab', 'ac', 'a')
        self.assertIsInstance(tree.children[0], FullPattern)

    def test_partial_change(self) -> None:
        """Create another PartialPattern from a PartialPattern."""
        patterns = '*Obigo/Q05*', '*Obigo/Q03*', '*Obigo/WAP2.0*'
        self._test_addition(patterns, ['*Obigo/'],
                            ['*Obigo/Q0', patterns[-1]])

    def _test_addition(self, patterns: Sequence[str],
                       *level_patterns: Sequence[str]) -> None:
        """Add patterns and compare resulting patterns of each level."""
        node: Parent = self._add_patterns(*patterns)
        for expected in level_patterns:
            actual = [child.pattern for child in node.children]
            self.assertSequenceEqual(expected, actual)
            node = node.children[0]

    @classmethod
    def _add_patterns(cls, *patterns: str) -> Tree:
        tree = Tree()
        for pattern in patterns:
            node = cls._get_full_pattern(pattern)
            tree.add_node(node)
        return tree

    @classmethod
    def _get_full_pattern(cls, pattern: str) -> FullPattern:
        properties = cls._get_properties(pattern)
        return FullPattern(properties)

    @staticmethod
    def _get_properties(pattern: str) -> Properties:
        prop_values: List[str] = [None] * len(Properties._fields)
        prop_values[0] = pattern
        return Properties(*prop_values)
