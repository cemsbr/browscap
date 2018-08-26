"""Test pattern search."""
import unittest

from browscapy.database import IndexNode
from browscapy.node import FullPattern, Tree
from browscapy.properties import Properties
from browscapy.search import Browscapy, Database


class TestSearch(unittest.TestCase):
    """Test results for some user agents."""

    @unittest.skip('Possible fix: recreate the cache')
    def test_user_agent01(self):
        """Pattern should match PHP result."""
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0;' + \
            ' rv:11.0) like Gecko'
        Database.init_cache_file()
        database = Database()
        searcher = Browscapy(database)
        FullPattern.set_database(database)

        actual = searcher.search(user_agent)
        expected = 'Mozilla/5.0 (*Windows NT 10.0*WOW64*Trident/7.0*rv:11.0*'
        self.assertEqual(expected, actual)

    def test_last_node_is_star(self) -> None:
        """If the next and last node is a star, it should match, too."""
        tree = Tree()
        Database.kv_store = {}
        database = Database()
        FullPattern.set_database(database)

        prop_values = [''] * len(Properties._fields)
        properties = Properties(*prop_values)
        for pattern in 'abcd', 'abc*':
            node = FullPattern(pattern, properties)
            tree.add_node(node)
        tree.optimize()

        IndexNode.store_parsed_tree(tree, database)
        searcher = Browscapy(database)
        actual = searcher.search('abce')
        expected = 'abc*'
        self.assertEqual(expected, actual)
