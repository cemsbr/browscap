"""Test Node class."""
from typing import Iterable
from unittest import TestCase

from browscapy.node import Node


class TestNode(TestCase):
    """Test Nodes with browscap patterns."""

    def test_add_node(self) -> None:
        """Add 2 nodes with a common prefix."""
        self._test_addition(
            patterns=('Mozilla/4.0 Test', 'Mozilla/5.0 Test'),
            expected_parent='Mozilla/',
            expected_children=('4.0 Test', '5.0 Test')
        )

    def test_add_node_no_prefix(self) -> None:
        """Should create a parent with an empty pattern."""
        pattern1 = 'Mozilla/4.0 Test'
        pattern2 = 'curl/7.52.1'
        node1 = Node(pattern1)
        node2 = Node(pattern2)

        parent = node1 + node2
        self.assertEqual('', parent.pattern)

        children_patts = [child.pattern for child in parent.children]
        expected = [pattern1, pattern2]
        self.assertListEqual(expected, children_patts)

    def test_add_same_patterns(self) -> None:
        """Shouldn't add 2 nodes with the same prefix."""
        node1 = Node('Mozilla/4.0 Test')
        node2 = Node('Mozilla/4.0 Test')

        self.assertRaises(ValueError, lambda: node1 + node2)

    def _test_addition(self, patterns: Iterable[str], expected_parent: str,
                       expected_children: Iterable[str]) -> None:
        """Add patterns and check results."""
        children = [Node(pattern) for pattern in patterns]
        parent = children[0] + children[1]
        self.assertEqual(expected_parent, parent.pattern)

        actual_children = [child.pattern for child in parent.children]
        self.assertSequenceEqual(expected_children, actual_children)
