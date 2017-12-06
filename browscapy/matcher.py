"""Implement a simple matcher to be used instead of Python's re module.

This simplified matcher accepts the special characters "*" and "?" in the
pattern, meaning any set of characters and a single character, respectively.
"""


def match(pattern: str, string: str, ignore_case: bool = False) -> bool:
    """Return whether string matches pattern, and chars in common.

    The common chars count is how many chars in the pattern match the
    string, excluding "*" and "?".
    """
    if ignore_case:
        pattern = pattern.lower()
        string = string.lower()

    pat_i, str_i = 0, 0
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
                    pat_i += 2  # Next iter will match the 2nd char after *
        elif pat_char != str_char and pat_char != '?':
            break
        # Always move both indexes
        pat_i += 1
        str_i += 1

    # There's a match if the string is over and:
    # - The pattern is also over; or
    # - The rest of the pattern is only a star
    return (str_i == len(string)
            and (pat_i == len(pattern)
                 or (pat_i == len(pattern) - 1
                     and pattern[pat_i] == '*')))
