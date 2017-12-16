#!/usr/bin/env python3
"""Change browscap pattern to match PHP output."""
import sys

for line in sys.stdin:
    line = line.rstrip()
    if line == '-':
        print('/^.*$/')
        continue
    print('/^' + line.rstrip().lower().replace('/', r'\/').replace('.', r'\.')
          .replace('?', '.').replace('*', '.*').replace('(', r'\(')
          .replace(')', r'\)').replace(':', r'\:') + '$/')
