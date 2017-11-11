import sys
import unittest
from unittest.mock import patch

from browscapy.cli import entry_point


class TestCli(unittest.TestCase):

    @staticmethod
    @patch('browscapy.cli.main.Main.fetch')
    def test_fetch_command(fetch):
        sys.argv = ('browscapy', 'fetch')
        entry_point()
        fetch.assert_called_once()

    @staticmethod
    @patch('browscapy.cli.main.Main.convert')
    def test_convert_command(convert):
        sys.argv = ('browscapy', 'convert')
        entry_point()
        convert.assert_called_once()
