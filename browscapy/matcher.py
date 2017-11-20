"""Implement a simple matcher to be used instead of Python's re module.

This simplified matcher accepts the special characters "*" and "?" in the
pattern, meaning any set of characters and a single character, respectively.
"""
from typing import Tuple


def match(pattern: str, string: str) -> Tuple[bool, int]:
    """Return whether string matches pattern, and chars in common.

    The common chars count is how many chars in the pattern match the
    string, excluding "*" and "?".
    """
    matched_length, pat_i, str_i = 0, 0, 0
    string = string.lower()

    while pat_i < len(pattern) and str_i < len(string):
        pat_char = pattern[pat_i]
        str_char = string[str_i]
        if pat_char == '*':
            next_pat_i = pat_i + 1
            pat_i -= 1  # By default, match * again in the next iteration
            if next_pat_i < len(pattern):  # Check the next (non-*) char
                next_pat_char = pattern[next_pat_i]
                if next_pat_char == str_char:  # There's a match after *
                    # Compute a future match
                    matched_length += 1
                    pat_i += 2  # Next iter will match the 2nd char after *
        elif pat_char == str_char:
            matched_length += 1
        elif pat_char != '?':  # Don't count '?' as a matching character
            break
        # Always move both indexes
        pat_i += 1
        str_i += 1

    # There's a match if the string is over and:
    # - The pattern is also over; or
    # - The rest of the pattern is only a star
    does_match = (str_i == len(string)
                  and (pat_i == len(pattern)
                       or (pat_i < len(pattern)
                           and pattern[pat_i] == '*')))

    return does_match, matched_length
