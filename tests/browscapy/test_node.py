"""Test Node class."""
from unittest import TestCase

from browscapy.node import Node


class TestNode(TestCase):
    """Test Nodes with browscap patterns."""

    def test_add_node(self) -> None:
        """Add 2 nodes with a common prefix."""
        node1 = Node('Mozilla/4.0 Test')
        node2 = Node('Mozilla/5.0 Test')

        parent = node1 + node2
        self.assertEqual('Mozilla/', parent.pattern)

        children_patts = [child.pattern for child in parent.children]
        expected = ['4.0 Test', '5.0 Test']
        self.assertListEqual(expected, children_patts)

    def test_add_node_no_prefix(self) -> None:
        """Shouldn't add 2 nodes without a common prefix."""
        node1 = Node('Mozilla/4.0 Test')
        node2 = Node('curl/7.52.1')

        with self.assertRaises(ValueError):
            node1 + node2  # pylint: disable=pointless-statement

    def test_add_same_patterns(self) -> None:
        """Shouldn't add 2 nodes with the same prefix."""
        node1 = Node('Mozilla/4.0 Test')
        node2 = Node('Mozilla/4.0 Test')

        with self.assertRaises(ValueError):
            node1 + node2  # pylint: disable=pointless-statement
