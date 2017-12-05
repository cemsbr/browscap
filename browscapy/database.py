"""Disk cache for browscap data."""
import shelve
from pathlib import Path
# Skip bandit low-severity issue
from pickle import HIGHEST_PROTOCOL  # nosec


class Database:  # pylint: disable=too-few-public-methods
    """Key-value database."""

    EMPTY_WRITE = 'n'
    READ = 'r'

    dictionary: shelve.DbfilenameShelf = None

    @classmethod
    def init(cls, mode: str = 'r') -> None:
        """Create folder if needed."""
        # error: Expression type contains "Any" (has type "Type[Path]")
        # How to solve it?
        folder = Path.home() / '.browscapy'  # type: ignore
        filename = folder / 'cache'

        # Ignore wrong pylint error because it's a PosixPath, not PurePath
        if not folder.exists():  # pylint: disable=no-member
            folder.mkdir()       # pylint: disable=no-member

        cls.dictionary = shelve.open(str(filename), mode, HIGHEST_PROTOCOL)

    @classmethod
    def close(cls) -> None:
        """Close the shelve, persisting the data."""
        cls.dictionary.close()
