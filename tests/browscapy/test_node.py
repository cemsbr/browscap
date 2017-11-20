"""Test Node class."""
from typing import Sequence
from unittest import TestCase

from browscapy.node import Node


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
        node1 = Node('Mozilla/4.0 Test')
        node2 = Node('Mozilla/4.0 Test')

        self.assertRaises(ValueError, lambda: node1.add_node(node2))

    def test_add_suffixed_pattern(self) -> None:
        """Should add normally if the other pattern has extra chars."""
        patterns = 'One', 'One Two'
        self._test_addition(patterns, expected_parent='One',
                            expected_children=patterns[1:])

    def _test_addition(self, patterns: Sequence[str], expected_parent: str,
                       expected_children: Sequence[str]) -> None:
        """Add patterns and check results."""
        parent = self._add_nodes(patterns)
        self.assertEqual(expected_parent, parent.pattern)

        children_patterns = [child.pattern for child in parent.children]
        self.assertSequenceEqual(expected_children, children_patterns)

    def test_first_grandchild(self) -> None:
        """Should add this node as a grandchild."""
        patterns = 'One', 'One Two', 'One Two Three'
        root = self._add_nodes(patterns)

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
        root = self._add_nodes(patterns)

        self.assertEqual(patterns[0], root.pattern)
        self.assertEqual(2, len(root.children))
        children_patterns = [child.pattern for child in root.children]
        self.assertSequenceEqual(patterns[1:], children_patterns)

    def test_add_to_root_node(self) -> None:
        """Should add child and grandchild to an empty pattern."""
        root = Node('')
        root.add_node(Node('ab'))
        root.add_node(Node('ac'))

        self.assertEqual(1, len(root.children))
        child = root.children[0]
        self.assertEqual('a', child.pattern)

        self.assertEqual(2, len(child.children))
        patterns = [gchild.pattern for gchild in child.children]
        self.assertSequenceEqual(['ab', 'ac'], patterns)

    @staticmethod
    def _add_nodes(patterns: Sequence[str]) -> Node:
        nodes = [Node(pattern) for pattern in patterns]
        root = nodes[0]
        for node in nodes[1:]:
            root.add_node(node)
        return root
