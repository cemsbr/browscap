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

    @classmethod
    @patch('urllib.request')
    @patch('browscapy.cli.main.Path')
    def test_uptodate_file(cls, path, request):
        """Should not download a remote file with same mod time."""
        utc_str = 'Tue, 31 Jan 2017 15:23:11 GMT'
        tstamp = parsedate_to_datetime(utc_str).timestamp()
        csv_file = cls.get_csv_file(path)
        csv_file.stat.return_value.st_mtime = tstamp
        res = request.urlopen.return_value.__enter__.return_value
        res.info.return_value = {'Last-Modified': utc_str}
        Main('/notusedfolder').update_file()
        request.urlretrieve.assert_not_called()

    @classmethod
    @patch('urllib.request')
    @patch.object(Main, 'update_file')
    @patch('browscapy.cli.main.Path')
    def test_fetch_dir_creation(cls, path, *args):
        """Should create a folder to store file if it doesn't exist."""
        parent = cls.get_cache_folder(path, False)
        Main.fetch(path)
        parent.mkdir.assert_called()

    @classmethod
    @patch('urllib.request')
    @patch.object(Main, 'update_file')
    @patch('browscapy.cli.main.Path')
    def test_convert_dir_creation(cls, path, *args):
        """Should create a folder for the cache if it doesn't exist."""
        parent = cls.get_cache_folder(path, False)
        Main.convert(path)
        parent.mkdir.assert_called()

    @classmethod
    @patch('urllib.request')
    @patch.object(Main, 'download')
    @patch('browscapy.cli.main.Path')
    def test_update_download(cls, path, download, *args):
        """Should download file if there's no local file."""
        csv_file = cls.get_csv_file(path)
        csv_file.exists.return_value = False
        main = Main(csv_file)
        main.update_file()
        download.assert_called()

    @patch('browscapy.cli.main.log')
    @patch('browscapy.cli.main.Path')
    def test_error_file_not_found(self, path, log):
        """When csv_file is not found, should log as error."""
        csv_file = self.get_csv_file(path)
        csv_file.exists.return_value = False

        main = Main(csv_file)
        log.error.assert_not_called()
        main.create_cache()
        log.error.assert_called()

    @staticmethod
    def get_csv_file(path):
        return path.return_value.expanduser.return_value.__truediv__\
            .return_value

    @classmethod
    def get_cache_folder(cls, path, exists):
        parent = cls.get_csv_file(path).parent
        parent.exists.return_value = exists
        return parent
