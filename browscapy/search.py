"""Optimize read-only search."""
from types import TracebackType
from typing import TYPE_CHECKING, Optional, Type

from .database import Database
from .matcher import match
from .database import IndexNode

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from .node import Node, Tree  # noqa


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

    def __init__(self, database: Optional[Database]) -> None:
        """Initialize cache."""
        if database is None:
            database = Database()
        self._database = database
        self._user_agent: str
        self._root: IndexNode = database.get_index_node('root')
        self._result: SearchResult
        self._ignore_case: bool = False

    def __enter__(self) -> 'Browscapy':
        """Context manager to automatically close the database."""
        return self

    def __exit__(self,
                 exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]) -> Optional[bool]:
        """Close the database in a context manager."""
        self.close()
        return exc_type is None

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
            if child.max_length < length:  # last node can be '*' -> <
                break  # They are sorted by max_length desc
            child_pattern = partial_pattern = pattern + child.pattern
            if partial_pattern[-1] != '*':
                partial_pattern += '*'
            if match(partial_pattern, self._user_agent, self._ignore_case):
                child_length = length + self._get_length(child.pattern)
                self._search_child(child_pattern, child_length)

    def _search_child(self, pattern: str, length: int) -> None:
        node = self._database.get_index_node(pattern)
        if node.is_full_pattern:
            # If it ends with *, there was a match in _search_children
            if pattern[-1] == '*' or \
                    match(pattern, self._user_agent, self._ignore_case):
                self._result.update(pattern, length)
        if node.children_info:
            self._search_children(node, pattern, length)

    @staticmethod
    def _get_length(pattern: str) -> int:
        return sum(1 for char in pattern if char not in ('*', '?'))

    def close(self) -> None:
        """Close the database."""
        self._database.close()
