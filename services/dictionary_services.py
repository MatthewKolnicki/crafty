"""
Dictionary flattening services.

This module contains business logic for flattening nested dictionaries
using various approaches: recursive, iterative, and library-based.
"""

from typing import Dict, Any
import flatdict


def _flatten_recursive(
    dictionary: dict, parent_key: str = "", delimiter: str = "."
) -> dict:
    """
    Recursively flatten a nested dictionary.

    Args:
        dictionary: The dictionary to flatten
        parent_key: The parent key prefix
        delimiter: The delimiter to use between keys

    Returns:
        Flattened dictionary with dot-notation keys
    """
    items = {}
    for k, v in dictionary.items():
        # If parent_key is not empty, add the separator and the key, otherwise just the key
        new_key = f"{parent_key}{delimiter}{k}" if parent_key else str(k)
        if isinstance(v, dict):
            items.update(_flatten_recursive(v, new_key, delimiter=delimiter))
        else:
            items[new_key] = v
    return items


def flatten_dictionary_iterative(
    dictionary: Dict[str, Any], delimiter: str = "."
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary using iterative approach with stack.

    Args:
        dictionary: The dictionary to flatten
        delimiter: The delimiter to use between keys

    Returns:
        Flattened dictionary with delimiter-separated keys
    """
    flattened = {}
    # Use a stack to store (key_prefix, dictionary) pairs
    stack = [("", dictionary)]

    while stack:
        prefix, current_dict = stack.pop()

        for key, value in current_dict.items():
            # Build the full key with prefix
            full_key = f"{prefix}{delimiter}{key}" if prefix else key

            if isinstance(value, dict):
                # Add nested dictionary to stack for processing
                stack.append((full_key, value))
            else:
                # Add leaf value to flattened result
                flattened[full_key] = value

    return flattened


def flatten_dictionary_recursive(
    dictionary: Dict[str, Any], parent_key: str = "", delimiter: str = "."
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary using recursive approach.

    Args:
        dictionary: The dictionary to flatten
        parent_key: The parent key prefix
        delimiter: The delimiter to use between keys

    Returns:
        Flattened dictionary with delimiter-separated keys
    """
    return _flatten_recursive(dictionary, parent_key, delimiter)


def flatten_dictionary_library(
    dictionary: Dict[str, Any], delimiter: str = "."
) -> Dict[str, Any]:
    """
    Flatten a nested dictionary using the flatdict library.

    Args:
        dictionary: The dictionary to flatten
        delimiter: The delimiter to use between keys

    Returns:
        Flattened dictionary with delimiter-separated keys
    """
    flattened_dict = flatdict.FlatDict(dictionary, delimiter=delimiter)
    return dict(flattened_dict)
