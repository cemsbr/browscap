"""Disk cache for browscap data."""
import shelve
from pathlib import Path
# Skip bandit low-severity issue
from pickle import HIGHEST_PROTOCOL  # nosec


class Database:  # pylint: disable=too-few-public-methods
    """Key-value database."""

    def __init__(self, readonly: bool = True) -> None:
        """Create folder if needed."""
        flag = 'r' if readonly else 'n'
        # Ignore: error: Expression type contains "Any" (has type "Type[Path]")
        # How to solve it?
        folder = Path.home() / '.browscapy'  # type: ignore
        filename = folder / 'cache'

        # Ignore wrong pylint error because it's a PosixPath, not PurePath
        if not folder.exists():  # pylint: disable=no-member
            folder.mkdir()       # pylint: disable=no-member

        self.shelve = shelve.open(str(filename), flag, HIGHEST_PROTOCOL)

    def close(self) -> None:
        """Close the shelve, persisting the data."""
        self.shelve.close()
