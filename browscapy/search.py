"""Optimize read-only search."""
from typing import TYPE_CHECKING, NamedTuple, Tuple

from browscapy.database import Database
from browscapy.matcher import match
from browscapy.node import FullPattern

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from browscapy.node import Node, Parent, Tree  # noqa


class Child(NamedTuple):  # pylint: disable=too-few-public-methods
    """Information on whether to search the child."""

    max_length: int
    pattern: str


class SearchNode:  # pylint: disable=too-few-public-methods
    """Node optimized for searching."""

    def __init__(self) -> None:
        """Initialize attributes as a non-full-pattern node."""
        # Order: pattern length
        self.children: Tuple[Child, ...] = None
        self.is_full_pattern = False

    @classmethod
    def store_parsed_tree(cls, tree: 'Tree') -> None:
        """Store the parsed tree in an optimized format."""
        root = cls()
        root.children = tuple(Child(node.max_length, node.pattern)
                              for node in tree.children)
        Database.dictionary['__index__root'] = root

        for child in tree.children:
            cls._store_parsed_node(child)

    @classmethod
    def _store_parsed_node(cls, node: 'Node') -> None:
        """Store a parsed node in an optimized format, recursively."""
        search_node = cls()
        if isinstance(node, FullPattern):
            search_node.is_full_pattern = True
        if node.children:
            start = len(node.pattern)
            search_node.children = tuple(
                Child(child.max_length, child.pattern[start:])
                for child in node.children)
        Database.dictionary['__index__' + node.pattern] = search_node

        for child in node.children:
            cls._store_parsed_node(child)


class SearchResult:  # pylint: disable=too-few-public-methods
    """Save the best result found so far."""

    def __init__(self) -> None:
        """Prepare for new a search."""
        self.pattern = ''
        self.length = 0

    def update(self, pattern: str, length: int) -> None:
        """Update the search result."""
        if length > self.length:
            self.pattern = pattern
            self.length = length


class Browscapy:
    """High-level end-user class."""

    def __init__(self):
        """Initialize cache."""
        self._user_agent = ''
        Database.init(Database.READ)
        self._database = Database.dictionary
        self._root: SearchNode = self._database['__index__root']
        self._result: SearchResult = None
        self._ignore_case = False

    def search(self, user_agent: str) -> str:
        """Return browscap properties for a user_agent."""
        self._user_agent = user_agent
        pattern = self._search()
        if not pattern:
            self._ignore_case = True
            pattern = self._search()
        return pattern

    def _search(self) -> str:
        self._result = SearchResult()
        self._search_children(self._root, '', 0)
        return self._result.pattern

    def _search_children(self, node: SearchNode, pattern: str, length: int) \
            -> None:
        for child in node.children:
            if child.max_length <= length:
                break  # They are sorted by max_length desc
            child_pattern = partial_pattern = pattern + child.pattern
            if partial_pattern[-1] != '*':
                partial_pattern += '*'
            if match(partial_pattern, self._user_agent, self._ignore_case):  # type: ignore  # noqa  pylint: disable=line-too-long
                child_length = length + self._get_length(child.pattern)
                self._search_child(child_pattern, child_length)

    def _search_child(self, pattern: str, length: int) -> None:
        node: SearchNode = \
            self._database['__index__' + pattern]  # type: ignore
        if node.is_full_pattern:
            # If ends with *, there was a match in _search_children
            if pattern[-1] == '*' or match(pattern, self._user_agent, self._ignore_case):  # type: ignore  # noqa  pylint: disable=line-too-long
                self._result.update(pattern, length)
        if node.children:
            self._search_children(node, pattern, length)

    @staticmethod
    def _get_length(pattern: str) -> int:
        return sum(1 for char in pattern if char not in ('*', '?'))

    @staticmethod
    def close() -> None:
        """Close the database."""
        Database.close()
