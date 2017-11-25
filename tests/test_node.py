"""Test Node class."""
from typing import List, Sequence
from unittest import TestCase

from browscapy.node import FullPattern, Node, PartialPattern, Tree
from browscapy.properties import Properties


class TestNode(TestCase):
    """Test Nodes with browscap patterns."""

    def test_add_node(self) -> None:
        """Add 2 nodes with a common prefix."""
        patterns = 'Mozilla/4.0 Test', 'Mozilla/5.0 Test'
        self._test_addition(patterns, expected_parent='Mozilla/',
                            expected_children=patterns)

    def test_add_node_no_prefix(self) -> None:
        """Should create a parent with an empty pattern."""
        patterns = 'Mozilla/4.0 Test', 'curl/7.52.1'
        self._test_addition(patterns, expected_parent='',
                            expected_children=patterns)

    def test_add_same_patterns(self) -> None:
        """Shouldn't add 2 nodes with the same prefix."""
        node1 = self._get_full_pattern('Mozilla/4.0 Test')
        node2 = self._get_full_pattern('Mozilla/4.0 Test')
        tree = Tree()
        tree.add_node(node1)
        self.assertRaises(ValueError, lambda: tree.add_node(node2))

    def test_add_suffixed_pattern(self) -> None:
        """Should add normally if the other pattern has extra chars."""
        patterns = 'One', 'One Two'
        self._test_addition(patterns, expected_parent='One',
                            expected_children=patterns[1:])

    def _test_addition(self, patterns: Sequence[str], expected_parent: str,
                       expected_children: Sequence[str]) -> None:
        """Add patterns and check results."""
        parent = self._add_nodes(*patterns)
        self.assertEqual(expected_parent, parent.pattern)

        children_patterns = [child.pattern for child in parent.children]
        self.assertSequenceEqual(expected_children, children_patterns)

    def test_first_grandchild(self) -> None:
        """Should add this node as a grandchild."""
        patterns = 'One', 'One Two', 'One Two Three'
        root = self._add_nodes(*patterns)

        self.assertEqual(patterns[0], root.pattern)

        self.assertEqual(1, len(root.children))
        child = root.children[0]
        self.assertEqual(patterns[1], child.pattern)

        self.assertEqual(1, len(child.children))
        grandchild = child.children[0]
        self.assertEqual(patterns[2], grandchild.pattern)

    def test_second_child(self) -> None:
        """Add a node as a second child."""
        patterns = 'One', 'OneTwo', 'OneFour'
        root = self._add_nodes(*patterns)

        self.assertEqual(patterns[0], root.pattern)
        self.assertEqual(2, len(root.children))
        children_patterns = [child.pattern for child in root.children]
        self.assertSequenceEqual(patterns[1:], children_patterns)

    def test_add_to_root_node(self) -> None:
        """Should add child and grandchild to an empty pattern."""
        root = self._add_nodes('', 'ab', 'ac')

        self.assertEqual(1, len(root.children))
        child = root.children[0]
        self.assertEqual('a', child.pattern)

        self.assertEqual(2, len(child.children))
        actual = [gchild.pattern for gchild in child.children]
        expected = 'ab', 'ac'
        self.assertSequenceEqual(expected, actual)

    def test_add_longer_than_partial(self) -> None:
        """Should add a full pattern as child of a shorter partial pattern."""
        root = self._add_nodes('ab', 'ac', 'ad')
        self.assertIsInstance(root, PartialPattern)
        self.assertEqual('a', root.pattern)
        self.assertEqual('ad', root.children[2].pattern)

    def test_partial_becomes_full(self) -> None:
        """If a partial pattern equals a full one, change it to full."""
        root = self._add_nodes('ab', 'ac', 'a')
        self.assertIsInstance(root, FullPattern)

    @classmethod
    def _add_nodes(cls, *patterns: str) -> Node:
        tree = Tree()
        for pattern in patterns:
            node = cls._get_full_pattern(pattern)
            tree.add_node(node)
        assert len(tree.children) == 1
        return tree.children[0]

    @classmethod
    def _get_full_pattern(cls, pattern: str) -> FullPattern:
        properties = cls._get_properties(pattern)
        return FullPattern(properties)

    @staticmethod
    def _get_properties(pattern: str) -> Properties:
        prop_values: List[str] = [None] * len(Properties._fields)
        prop_values[0] = pattern
        return Properties(*prop_values)
