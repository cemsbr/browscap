"""Measure memory required to create the cache."""
import cProfile
import csv
import pickle
import resource

from browscapy.node import FullPattern, Properties, Tree

TREE = Tree()


def get_memory() -> int:
    """Return resident memory in bytes."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def build_tree() -> None:
    """Build the whole tree."""
    with open('../browscap.csv') as browscap:
        csv_reader = csv.DictReader(browscap)
        print('Before nodes:', get_memory(), 'bytes')
        for row in csv_reader:
            properties = Properties(**row)
            node = FullPattern(properties)
            TREE.add_node(node)
        print('After nodes:', get_memory(), 'bytes')


def pickle_tree() -> None:
    """Create and dump the browscap tree."""
    cProfile.run('build_tree()', sort='tottime')
    with open('dump.pkl', 'wb') as dump_file:
        print('Pickling')
        pickle.Pickler(dump_file).dump(TREE)


if __name__ == '__main__':
    pickle_tree()
