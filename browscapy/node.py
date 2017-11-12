"""Node used to search for patterns."""
from typing import List, Tuple


class Node:
    """Full browscap pattern or partial with children.

    Attributes:
        pattern (str): Partial browscap pattern, excluding parent's and
            children's.
        children (List[Node]): Children nodes.

    """

    def __init__(self, pattern: str) -> None:
        """Build a node from a browscap pattern string."""
        self.pattern = pattern
        self.children: List[Node] = []

    def __add__(self, other: 'Node') -> 'Node':
        """Add a new Node to the tree."""
        parent_patt, child_patts = self._split_patterns(other.pattern)
        parent = Node(parent_patt)
        children = [Node(patt) for patt in child_patts]
        parent.children.extend(children)
        return parent

    def _split_patterns(self, other_pattern: str) \
            -> Tuple[str, Tuple[str, str]]:
        """Separate the common prefix from :attr:`pattern` and ``pattern2``.

        Return the common prefix and a tuple with the suffixes.
        """
        prefix_len = self._get_common_prefix_length(other_pattern)
        self._validate_common_prefix(prefix_len)

        parent = self.pattern[:prefix_len]
        child1 = self.pattern[prefix_len:]
        child2 = other_pattern[prefix_len:]

        return parent, (child1, child2)

    def _get_common_prefix_length(self, other_pattern: str) -> int:
        """Return the length of the common prefix."""
        length = 0
        for char1, char2 in zip(self.pattern, other_pattern):
            if char1 != char2:
                break
            length += 1
        return length

    def _validate_common_prefix(self, prefix_len: int) -> None:
        if prefix_len == 0:
            raise ValueError("Can't add nodes without a common prefix.")
        elif prefix_len == len(self.pattern):
            raise ValueError("Can't add nodes with the same pattern.")
