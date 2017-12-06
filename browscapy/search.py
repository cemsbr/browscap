"""Optimize read-only search."""
from typing import TYPE_CHECKING, NamedTuple, Tuple

from .database import Database
from .matcher import match
from .node import FullPattern

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from .node import Node, Tree  # noqa


class IndexNodeInfo(NamedTuple):  # pylint: disable=too-few-public-methods
    """Information on whether to search the child."""

    max_length: int
    pattern: str


class IndexNode:  # pylint: disable=too-few-public-methods
    """Node optimized for searching."""

    def __init__(self) -> None:
        """Initialize attributes as a non-full-pattern node."""
        # Order: pattern length
        self.children_info: Tuple[IndexNodeInfo, ...] = None
        self.is_full_pattern = False

    @classmethod
    def store_parsed_tree(cls, tree: 'Tree') -> None:
        """Store the parsed tree in an optimized format."""
        root = cls()
        root.children_info = tuple(
            IndexNodeInfo(node.max_length, node.pattern)
            for node in tree.children)
        Database.add_index_node('root', root)

        for child in tree.children:
            cls._store_parsed_node(child)

    @classmethod
    def _store_parsed_node(cls, node: 'Node') -> None:
        """Store a parsed node in an optimized format, recursively."""
        index_node = cls()
        if isinstance(node, FullPattern):
            index_node.is_full_pattern = True
        if node.children:
            start = len(node.pattern)
            index_node.children_info = tuple(
                IndexNodeInfo(child.max_length, child.pattern[start:])
                for child in node.children)
        Database.add_index_node(node.pattern, index_node)

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
        self._user_agent: str = None
        Database.init(Database.READ)
        self._root: IndexNode = Database.get_index_node('root')
        self._result: SearchResult = None
        self._ignore_case: bool = False

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

    def _search_children(self, node: IndexNode, pattern: str, length: int) \
            -> None:
        for child in node.children_info:
            if child.max_length <= length:
                break  # They are sorted by max_length desc
            child_pattern = partial_pattern = pattern + child.pattern
            if partial_pattern[-1] != '*':
                partial_pattern += '*'
            if match(partial_pattern, self._user_agent, self._ignore_case):
                child_length = length + self._get_length(child.pattern)
                self._search_child(child_pattern, child_length)

    def _search_child(self, pattern: str, length: int) -> None:
        node = Database.get_index_node(pattern)
        if node.is_full_pattern:
            # If ends with *, there was a match in _search_children
            if pattern[-1] == '*' or \
                    match(pattern, self._user_agent, self._ignore_case):
                self._result.update(pattern, length)
        if node.children_info:
            self._search_children(node, pattern, length)

    @staticmethod
    def _get_length(pattern: str) -> int:
        return sum(1 for char in pattern if char not in ('*', '?'))

    @staticmethod
    def close() -> None:
        """Close the database."""
        Database.close()
