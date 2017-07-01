"""Module to answer cli requests."""
import logging
import urllib.request
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from os import utime
from pathlib import Path

log = logging.getLogger('browscapy')


class Main:
    URL = 'http://browscap.org/stream?q=BrowsCapCSV'
    FILE = 'browscap.csv'

    def __init__(self, cache_folder):
        self._csv_file = Path(cache_folder).expanduser() / self.FILE

    @classmethod
    def _get_obj_with_folder(cls, cache_folder):
        obj = cls(cache_folder)
        obj.assert_folder()
        return obj

    @classmethod
    def fetch(cls, cache_folder):
        obj = cls._get_obj_with_folder(cache_folder)
        obj.update_file()

    @classmethod
    def convert(cls, cache_folder):
        obj = cls._get_obj_with_folder(cache_folder)
        obj.create_cache()

    def create_cache(self):
        if not self._csv_file.exists():
            log.error('browscap.csv not found. Did you run fetch?')
        else:
            self._parse()

    def _parse(self):
        pass

    def assert_folder(self):
        folder = self._csv_file.parent
        if not folder.exists():
            folder.mkdir(parents=True)
            log.info('Created folder %s', folder)

    def update_file(self):
        local_time = self._get_local_mod_time()
        if not local_time:
            self.download()
        else:
            remote_time = self._get_remote_mod_time()
            if local_time < remote_time:
                self.download(remote_time)
            else:
                log.info('No newer remote file available.')

    def _get_local_mod_time(self):
        if self._csv_file.exists():
            tstamp = self._csv_file.stat().st_mtime
            dtime = datetime.fromtimestamp(tstamp, timezone.utc)
            if log.isEnabledFor(logging.INFO):
                string = dtime.strftime('%a, %d %b %Y %H:%M:%S GMT')
                log.info('Local file:  %s', string)
            return dtime

    def _get_remote_mod_time(self):
        # Currently, browscap.org ignores If-Modified-Since header.
        req = urllib.request.Request(self.URL, method='HEAD')
        with urllib.request.urlopen(req) as res:
            remote_time = res.info()['Last-Modified']
            log.info('Remote file: %s', remote_time)
            return parsedate_to_datetime(remote_time)

    def download(self, last_modified=None):
        log.info('Downloading browscap.csv...')
        headers = urllib.request.urlretrieve(self.URL, str(self._csv_file))[1]
        if last_modified is None:
            last_modified = parsedate_to_datetime(headers['Last-Modified'])
        log.info('Downloaded %s', self._csv_file)
        tstamp = last_modified.timestamp()
        utime(str(self._csv_file), (tstamp, tstamp))
