"""Download and cache data from browscap.org.

Usage:
  browscapy -h | --help
  browscapy fetch   [--cache=DIR]
  browscapy convert [--cache=DIR]

Commands:
  fetch    Download browscap.csv file.
  convert  Create cache from browscap.csv.

Options:
  --cache=DIR  Cache folder [default: ~/.browscap].
  -h, --help   This help.
"""
import logging
from docopt import docopt
from .main import Main

logging.basicConfig(level=logging.INFO, format='%(message)s')


def entry_point():
    """Main function for CLI."""
    args = docopt(__doc__)
    if args['fetch']:
        Main.fetch(args['--cache'])
    elif args['convert']:
        Main.convert(args['--cache'])
