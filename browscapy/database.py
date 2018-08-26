"""Disk cache for browscap data."""
import shelve
from pathlib import Path
# Skip bandit low-severity issue
from pickle import HIGHEST_PROTOCOL  # nosec
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    # pylint: disable=unused-import
    from .properties import Properties  # noqa
    from .search import IndexNode  # noqa


class Database:
    """Key-value database."""

    EMPTY_WRITE = 'n'
    READ = 'r'
    _INDEX_PREFIX = '__index__'

    kv_store: shelve.DbfilenameShelf = None

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
        """Add browscap properties to database."""
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
        cls.kv_store.close()
