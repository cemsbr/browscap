class Pattern:

    @staticmethod
    def to_python(bcap_pat):
        """Convert browscap pattern to Python pattern."""
        return '^' + bcap_pat.replace('.', r'\.').replace('?', '.') \
            .replace('*', '.*?').replace('(', r'\(').replace(')', r'\)') \
            .replace('+', r'\+') + '$'

    @staticmethod
    def get_length(bcap_pat):
        """Return the length of the pattern after removing regex symbols."""
        return sum(1 for c in bcap_pat if c not in ('*', '?'))
