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
