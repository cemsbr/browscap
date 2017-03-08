import unittest

from browscapy.pattern import Pattern


class TestPattern(unittest.TestCase):

    def test_conversion_to_python(self):
        bcap_pat = '(.?*+)'
        expected = r'^\(\...*?\+\)$'
        actual = Pattern.to_python(bcap_pat)
        self.assertEqual(actual, expected)

    def test_length(self):
        bcap_pat = '(.?*+)'
        expected = 4  # only * and ? are symbols
        actual = Pattern.get_length(bcap_pat)
        self.assertEqual(actual, expected)
