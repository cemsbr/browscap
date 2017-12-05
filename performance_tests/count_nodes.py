"""Count and verify the number of entries for each entry type."""
import shelve
from pathlib import Path

# error: Expression type contains "Any" (has type "Type[Path]")
# How to solve it?
FILE: Path = Path.home() / '.browscapy' / 'cache'  # type: ignore
BROWSCAP_PATTERNS = 220154


def count_nodes(database):
    """Count node types"""
    total, partial, full, properties = 0, 0, 0, 0
    for key in database:
        total += 1
        if key.startswith('__index__'):
            node = database[key]
            if node.is_full_pattern:
                full += 1
            else:
                partial += 1
        else:
            properties += 1
    return total, partial, full, properties


def main():
    """Count, verify and print the number of node types."""
    with shelve.open(str(FILE)) as database:
        total, partial, full, properties = count_nodes(database)
        assert total == partial + full + properties
        assert full == BROWSCAP_PATTERNS, f'{full} != {BROWSCAP_PATTERNS}'
        assert full == properties, f'{full} != {properties}'
        print(total, 'entries in total:')
        print(full, '(x2) browscap patterns and properties.')
        print('', partial, 'partial nodes created.')


if __name__ == '__main__':
    main()
