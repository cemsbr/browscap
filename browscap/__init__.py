import re


class DB:
    kv = {}

    @classmethod
    def clear(cls):
        cls.kv.clear()


class Parser:

    TREE_KEY_RX = re.compile(r'( |\*|\?)')

    def __init__(self):
        DB.clear()
        self.forest = Forest()

    def parse(self, csv_row):
        br_pat = csv_row[0]
        root_key = self.TREE_KEY_RX.split(br_pat)[0]
        self.forest.add_tree(root_key)


class Forest:

    @staticmethod
    def get_trees(ua):
        first_word = ua.split()[0]
        while first_word:
            if first_word in DB.kv:
                yield DB.kv[first_word]
            first_word = first_word[:-1]

    @staticmethod
    def add_tree(root_key):
        if root_key not in DB.kv:
            DB.kv[root_key] = Node()


class Node:
    pass
