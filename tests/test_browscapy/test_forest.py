import unittest

from browscapy import DB, Parser


class TestForest(unittest.TestCase):

    _UA = 'Mozilla/5.0 Firefox'

    def test_tree_key(self):
        """Tree key should not have space or regex symbols."""
        self._parse_ua('Mozilla?.* Firefox')
        # The tree key is the only key in DB
        self.assertEqual(['Mozilla'], list(DB.kv.keys()))

    def test_multiple_trees(self):
        """Should consider all user agent substrings."""
        forest = self._parse_ua('Mozilla/5.* Firefox',
                                'Mozilla/*.* Firefox',
                                'Moz* Firefox')
        trees = self._count_trees(forest, self._UA)
        self.assertEqual(3, trees)

    def test_no_match(self):
        """Do not use tree key substrings."""
        forest = self._parse_ua('Mozilla/4.0 Firefox',
                                'Mozilla/5.1 Firefox')
        trees = self._count_trees(forest, self._UA)
        self.assertEqual(0, trees)

    @staticmethod
    def _parse_ua(*uas):
        parser = Parser()
        for ua in uas:
            parser.parse((ua, 'data_col0'))
        return parser.forest

    @staticmethod
    def _count_trees(forest, ua):
        trees = forest.get_trees(ua)
        return sum(1 for _ in trees)
