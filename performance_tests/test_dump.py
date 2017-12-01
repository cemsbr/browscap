"""Profile cache creation and dump."""
import cProfile
import csv
import pickle
import resource

from browscapy.node import FullPattern, Properties, Tree
from browscapy.database import Database

TREE = Tree()


def get_memory() -> int:
    """Return resident memory in bytes."""
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def init_database() -> Database:
    """Prepare a database for writing."""
    database = Database(readonly=False)
    FullPattern.DATABASE = database.shelve
    return database


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
    database = init_database()

    cProfile.run('build_tree()', sort=1)

    with open('dump.pkl', 'wb') as dump_file:
        print('Pickling')
        pickler = pickle.Pickler(dump_file, pickle.HIGHEST_PROTOCOL)
        pickler.dump(TREE)

    print('Writing shelve')
    database.close()


if __name__ == '__main__':
    pickle_tree()
