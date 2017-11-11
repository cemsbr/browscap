import unittest

from browscapy.pattern import Pattern


class TestPattern(unittest.TestCase):

    def test_conversion_to_python(self):
        bcap_pat = '(.?*+)'
        expected = r'^\(\...*?\+\)$'
        pattern = Pattern(bcap_pat)
        actual = pattern.compiled.pattern
        self.assertEqual(actual, expected)

    def test_length(self):
        bcap_pat = '(.?*+)'
        expected = 4  # only * and ? are symbols
        pattern = Pattern(bcap_pat)
        actual = pattern.length
        self.assertEqual(actual, expected)
