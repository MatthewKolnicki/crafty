"""
String normalization services.

This module contains business logic for string normalization operations,
including manual implementations and built-in method usage.
"""

from collections import defaultdict
from typing import List, Dict


def lower(s: str) -> str:
    """
    Manually convert string to lowercase without using built-in methods.

    Args:
        s: Input string to convert

    Returns:
        Lowercase version of the input string
    """
    result = ""
    for char in s:
        if "A" <= char <= "Z":
            # Convert uppercase to lowercase by adding 32 to ASCII value
            result += chr(ord(char) + 32)
        else:
            result += char
    return result


def strip(s: str) -> str:
    """
    Manually remove leading and trailing whitespace without using built-in methods.

    Args:
        s: Input string to strip

    Returns:
        String with leading and trailing whitespace removed
    """
    # Find start of non-whitespace
    start = 0
    while start < len(s) and s[start] in " \t\n\r":
        start += 1

    # Find end of non-whitespace
    end = len(s)
    while end > start and s[end - 1] in " \t\n\r":
        end -= 1

    return s[start:end]


def normalize_strings_manual(strings: List[str]) -> Dict[str, int]:
    """
    Manually normalize strings without using built-in methods.
    Converts to lowercase and removes leading/trailing whitespace.

    Args:
        strings: List of strings to normalize

    Returns:
        Dictionary with normalized strings as keys and their frequencies as values
    """
    normalized_types = [strip(lower(x)) for x in strings]
    frequency = defaultdict(int)
    for item in normalized_types:
        frequency[item] += 1
    return dict(frequency)


def normalize_strings_built_in(strings: List[str]) -> Dict[str, int]:
    """
    Use the built-in lower and strip methods to normalize strings.

    Args:
        strings: List of strings to normalize

    Returns:
        Dictionary with normalized strings as keys and their frequencies as values
    """
    normalized_types = [x.lower().strip() for x in strings]
    frequency = defaultdict(int)
    for item in normalized_types:
        frequency[item] += 1
    return dict(frequency)
