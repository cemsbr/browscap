"""Tests for the matcher algorithm."""
from unittest import TestCase

from browscapy.matcher import match


class TestMatcher(TestCase):
    """Test the Matcher class."""

    def test_both_empty(self) -> None:
        """Should match when both are empty."""
        self._test_match('', '', True, 0)

    def test_both_equal_non_empty(self) -> None:
        """Equal non-empty strings should match."""
        self._test_match('abc', 'abc', True, 3)

    def test_smaller_user_agent(self) -> None:
        """Should not match if user_agent hasn't the last pattern char."""
        self._test_match('abc', 'ab', False, 2)

    def test_smaller_pattern(self) -> None:
        """Should not match if pattern hasn't the last user agent char."""
        self._test_match('ab', 'abc', False, 2)

    def test_ending_star(self) -> None:
        """Trailing UA chars should match ending pattern star."""
        self._test_match('ab*', 'abcde', True, 2)

    def test_starting_star(self) -> None:
        """Starting UA chars should match starting pattern star."""
        self._test_match('*de', 'abcde', True, 2)

    def test_middle_start(self) -> None:
        """Should match a pattern with a star in the middle."""
        self._test_match('a*d', 'abcd', True, 2)

    def _test_match(self, pattern, user_agent, does_match, length):
        """Assert user_agent matches pattern with expected return values."""
        actual_does_match, actual_length = match(pattern, user_agent)
        self.assertEqual(does_match, actual_does_match)
        self.assertEqual(length, actual_length)
