"""Disk cache for browscap data."""
import shelve
from pathlib import Path
# Skip bandit low-severity issue
from pickle import HIGHEST_PROTOCOL  # nosec
from typing import Dict, NamedTuple, Tuple, TYPE_CHECKING, Union, cast

from .node import FullPattern

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from .properties import Properties  # noqa
    from .node import Node, Tree  # noqa


class Database:
    """Key-value database."""

    EMPTY_WRITE = 'n'
    READ = 'r'
    _INDEX_PREFIX = '__index__'

    kv_store: Union[shelve.DbfilenameShelf,
                    Dict[str, Union['IndexNode', 'Properties']]]

    @classmethod
    def init_cache_file(cls, mode: str = 'r') -> None:
        """Create folder if needed."""
        # error: Expression type contains "Any" (has type "Type[Path]")
        # How to solve it?
        folder = Path.home() / '.browscapy'  # type: ignore
        filename = folder / 'cache'

        # Ignore wrong pylint error because it's a PosixPath, not PurePath
        if not folder.exists():  # pylint: disable=no-member
            folder.mkdir()       # pylint: disable=no-member

        cls.kv_store = shelve.open(str(filename), mode, HIGHEST_PROTOCOL)

    @classmethod
    def add_properties(cls, pattern: str, properties: 'Properties') -> None:
        """Add browscap properties to database."""
        cls.kv_store[pattern] = properties

    @classmethod
    def get_properties(cls, pattern: str) -> 'Properties':
        """Get browscap properties to database."""
        return cast('Properties', cls.kv_store[pattern])

    @classmethod
    def add_index_node(cls, pattern: str, index_node: 'IndexNode') -> None:
        """Add index node to database."""
        key = cls._INDEX_PREFIX + pattern
        cls.kv_store[key] = index_node

    @classmethod
    def get_index_node(cls, pattern: str) -> 'IndexNode':
        """Return an index node from database."""
        key = cls._INDEX_PREFIX + pattern
        return cast('IndexNode', cls.kv_store[key])

    @classmethod
    def close(cls) -> None:
        """Close the shelve, persisting the data."""
        if isinstance(cls.kv_store, shelve.DbfilenameShelf):
            cls.kv_store.close()


class IndexNodeInfo(NamedTuple):  # pylint: disable=too-few-public-methods
    """Information on whether to search the child."""

    max_length: int
    pattern: str


class IndexNode:  # pylint: disable=too-few-public-methods
    """Node optimized for searching."""

    def __init__(self) -> None:
        """Initialize attributes as a non-full-pattern node."""
        # Order: pattern length
        self.children_info: Tuple[IndexNodeInfo, ...] = tuple()
        self.is_full_pattern = False

    @classmethod
    def store_parsed_tree(cls, tree: 'Tree', database: Database) -> None:
        """Store the parsed tree in an optimized format."""
        root = cls()
        root.children_info = tuple(
            IndexNodeInfo(node.max_length, node.pattern)
            for node in tree.children)
        database.add_index_node('root', root)

        for child in tree.children:
            cls._store_parsed_node(child, database)

    @classmethod
    def _store_parsed_node(cls, node: 'Node', database: Database) -> None:
        """Store a parsed node in an optimized format, recursively."""
        index_node = cls()
        if isinstance(node, FullPattern):
            index_node.is_full_pattern = True
        if node.children:
            start = len(node.pattern)
            index_node.children_info = tuple(
                IndexNodeInfo(child.max_length, child.pattern[start:])
                for child in node.children)
        database.add_index_node(node.pattern, index_node)

        for child in node.children:
            cls._store_parsed_node(child, database)
