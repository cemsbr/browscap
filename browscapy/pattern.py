import regex as re


class Pattern:
    """Convert browscap pattern to compiled Python regex pattern.

    Use _regex_ module instead of built-in _re_ to later unpickle already
    compiled pattern.
    """

    def __init__(self, bcap_pat):
        """Store length and compiled regex.

        Args:
            bcap_nat (str): Browscap pattern.
        """
        #: int: Browscap pattern length. Longer must be prefered.
        self.length = self._get_length(bcap_pat)
        #: compiled regex: compiled Python regex.
        self.compiled = self._compile(bcap_pat)

    @classmethod
    def _compile(cls, bcap_pat):
        """Convert a browscap pattern to a compiled Python regex."""
        pattern = cls._to_python(bcap_pat)
        return re.compile(pattern)

    @staticmethod
    def _to_python(bcap_pat):
        """Convert browscap pattern to Python pattern."""
        return '^' + bcap_pat.replace('.', r'\.').replace('?', '.') \
            .replace('*', '.*?').replace('(', r'\(').replace(')', r'\)') \
            .replace('+', r'\+') + '$'

    @staticmethod
    def _get_length(bcap_pat):
        """Return the length of the pattern after removing regex symbols."""
        return sum(1 for c in bcap_pat if c not in ('*', '?'))
