"""Module to answer cli requests."""
import csv
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
        self.csv_file = Path(cache_folder).expanduser() / self.FILE

    @staticmethod
    def _get_obj_with_folder(cache_folder):
        obj = Main(cache_folder)
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
        if not self.csv_file.exists():
            log.error('browscap.csv not found. Did you run fetch?')
        else:
            self._parse()

    def _parse(self):
        with self.csv_file.open() as f:
            next(f)  # skip browscap version info
            next(f)
            reader = csv.reader(f)
            next(reader)  # field names
            row = next(reader)
            row = [True if c == 'true' else c for c in row]
            row = [False if c == 'false' else c for c in row]
            print(row)

    def assert_folder(self):
        folder = self.csv_file.parent
        if not folder.exists():
            folder.mkdir(parents=True)
            log.info('Created folder %s', folder)

    def update_file(self):
        local_time = self._get_local_mod_time()
        remote_time = self._get_remote_mod_time(local_time)
        if not local_time or local_time < remote_time:
            self.download(remote_time)
        else:
            log.info('No newer remote file available.')

    def _get_local_mod_time(self):
        if self.csv_file.exists():
            mod_time = self.csv_file.stat().st_mtime
            return datetime.fromtimestamp(mod_time, timezone.utc)
        return None

    def _get_remote_mod_time(self, local_mod_time=None):
        req = self._get_request(local_mod_time)
        with urllib.request.urlopen(req) as res:
            remote_time = res.info()['Last-Modified']
            log.info('Remote file date: %s', remote_time)
            # Currently, browscap.org ignores If-Modified-Since header.
            # This will let us know when they check for it.
            if res.getcode() == 304:
                log.warning('Got 304, no need for the workaround anymore.')
            res_headers = res.info()
            return parsedate_to_datetime(res_headers['Last-Modified'])

    def _get_request(self, local_mod_time=None):
        headers = {}
        if local_mod_time:
            if_mod_since = local_mod_time.strftime('%a, %d %b %Y %H:%M:%S GMT')
            headers['If-Modified-Since'] = if_mod_since
            log.info('Local file date:  %s', if_mod_since)
        return urllib.request.Request(self.URL, headers=headers, method='HEAD')

    def download(self, remote_time):
        log.info('Downloading browscap.csv...')
        urllib.request.urlretrieve(self.URL, str(self.csv_file))
        log.info('Downloaded %s', self.csv_file)
        tstamp = remote_time.timestamp()
        utime(str(self.csv_file), (tstamp, tstamp))
