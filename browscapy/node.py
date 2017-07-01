"""Node used to search for patterns."""


class Node:
    """A Node has a pattern and can be matched against an user agent."""

    def __init__(self, pattern):
        """Initialize with a pattern object.

        Args:
            pattern (Pattern): Browscap pattern.
        """
        self._pattern = pattern

    @property
    def length(self):
        """int: pattern length."""
        return self._pattern.length

    def match(self, user_agent):
        return self._pattern.match(user_agent) is not None
