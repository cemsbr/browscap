"""Profile cache creation and dump."""
import cProfile
import csv
import resource
from sys import stderr

from browscapy.node import FullPattern, Properties, Tree
from browscapy.database import Database
from browscapy.search import SearchTree

TREE = Tree()


def get_memory() -> int:
    """Return resident memory in bytes."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def build_tree() -> None:
    """Build the whole tree."""
    with open('../browscap.csv') as browscap:
        csv_reader = csv.DictReader(browscap)
        print('Memory before:', get_memory(), 'bytes')
        print('Parsing and saving properties...', file=stderr)
        for row in csv_reader:
            properties = Properties(**row)
            node = FullPattern(properties)
            TREE.add_node(node)
        print('Calculating max length...', file=stderr)
        TREE.calc_max_length()
        print('Sorting tree...', file=stderr)
        TREE.sort_children()
        print('Storing index...', file=stderr)
        SearchTree.store_parsed_tree(TREE)
        print('Memory after:', get_memory(), 'bytes')


def pickle_tree() -> None:
    """Create and dump the browscap tree."""
    Database.init(Database.EMPTY_WRITE)
    cProfile.run('build_tree()', sort=1)
    print('Writing shelve...', file=stderr)
    Database.close()


if __name__ == '__main__':
    pickle_tree()
