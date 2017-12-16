#!/usr/bin/env python3
"""Measure time to find patterns from stdin."""
# import cProfile
import sys
import time

from browscapy.search import Browscapy

BC = Browscapy()


def search_stdin():
    """Read each input line as a user agent and print search results."""
    start_time = time.time()
    for line in sys.stdin:
        user_agent = line.rstrip()
        pattern = BC.search(user_agent)
        if pattern:
            print(pattern)
        else:
            print('-')
    return time.time() - start_time


# cProfile.run('search_stdin()', 'search.prof')
DURATION = search_stdin()
print(f'Total duration = {DURATION} sec', file=sys.stderr)
BC.close()
