from datetime import datetime
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
        brt_str = 'Tue, 31 Jan 2017 13:23:11 BRT'
        utc_str = 'Tue, 31 Jan 2017 15:23:11 GMT'
        dtime = datetime.strptime(brt_str, '%a, %d %b %Y %H:%M:%S %Z')
        csv_file = path.return_value.expanduser.return_value.__truediv__
        csv_file.return_value.stat.return_value.st_mtime = dtime.timestamp()
        res = request.urlopen.return_value.__enter__.return_value
        res.info.return_value = {'Last-Modified': utc_str}
        Main('/notusedfolder').update_file()
        request.urlretrieve.assert_not_called()
