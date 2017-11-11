"""Test Node class."""
from unittest import TestCase
from unittest.mock import Mock, sentinel

from browscapy.node import Node


class TestNode(TestCase):

    def test_length(self):
        """Node length should be pattern's."""
        pattern = Mock(length=sentinel.length)
        node = Node(pattern)
        self.assertIs(sentinel.length, node.length)

    def test_pattern_match(self):
        """Should return False when pattern match is None."""
        pattern = Mock()
        pattern.match.return_value = None
        node = Node(pattern)
        self.assertFalse(node.match('user agent'))
