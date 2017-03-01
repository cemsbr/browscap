from datetime import datetime
from email.utils import parsedate_to_datetime
from unittest import TestCase
from unittest.mock import patch

from browscapy.cli.main import Main


class TestMain(TestCase):

    @staticmethod
    @patch('urllib.request')
    @patch('browscapy.cli.main.utime')
    def test_download_mod_time(utime, _):
        """Should change file modification time to match server's."""
        Main('/notusedfolder').download(datetime.now())
        utime.assert_called()

    @staticmethod
    @patch('urllib.request')
    @patch('browscapy.cli.main.Path')
    def test_uptodate_file(path, request):
        """Should not download a remote file with same mod time."""
        utc_str = 'Tue, 31 Jan 2017 15:23:11 GMT'
        tstamp = parsedate_to_datetime(utc_str).timestamp()
        csv_file = path.return_value.expanduser.return_value.__truediv__
        csv_file.return_value.stat.return_value.st_mtime = tstamp
        res = request.urlopen.return_value.__enter__.return_value
        res.info.return_value = {'Last-Modified': utc_str}
        Main('/notusedfolder').update_file()
        request.urlretrieve.assert_not_called()
