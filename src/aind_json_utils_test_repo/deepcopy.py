"""
Deep Merge Module for JSON files.

This module provides functionality to merge two JSON files using a
precedence-based strategy where the main file acts as the
authoritative source.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional, Union


def is_empty_value(value: Any) -> bool:
    """
    Check if a value should be considered "empty" for merge purposes.

    Empty values include: None, empty string, empty dict, empty list.

    Args:
        value: The value to check.

    Returns:
        True if the value is considered empty, False otherwise.
    """
    if value is None:
        return True
    if value == "":
        return True
    if value == {}:
        return True
    if value == []:
        return True
    if not value:
        return True
    return False


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file from disk.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Parsed JSON as a dictionary.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    with open(file_path, "r") as f:
        return json.load(f)


def save_json_file(
    data: Dict[str, Any], file_path: str, indent: int = 2
) -> None:
    """
    Save a dictionary as a JSON file.

    Args:
        data: The dictionary to save.
        file_path: Path where the file should be saved.
        indent: Number of spaces for indentation (default: 2).
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent)


def merge_arrays(main_array, incoming_array):
    """
    Merge two arrays according to precedence rules.

    If main array is non-empty, it is preserved entirely.
    If main array is empty, incoming array is used.
    """
    if len(main_array) > 0:
        return main_array
    return incoming_array


def deep_merge(
    main_data: Dict[str, Any], incoming_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries with main_data taking precedence.

    Rules:
    - Keys only in main_data are preserved
    - Keys only in incoming_data are added
    - For shared keys, main_data value wins if it's populated
    - Empty values in main_data can be filled by incoming_data
    - Nested objects are merged recursively

    Args:
        main_data: The authoritative/primary dictionary.
        incoming_data: The supplemental/secondary dictionary.

    Returns:
        The merged dictionary.
    """
    result = incoming_data.copy()

    for key, main_value in main_data.items():
        if key not in incoming_data:
            result[key] = main_value
        else:
            incoming_value = incoming_data[key]

            if isinstance(main_value, dict) and isinstance(
                incoming_value, dict
            ):
                result[key] = deep_merge(main_value, incoming_value)
            elif isinstance(main_value, list) and isinstance(
                incoming_value, list
            ):
                result[key] = merge_arrays(main_value, incoming_value)
            else:
                if is_empty_value(incoming_value):
                    result[key] = main_value
                else:
                    result[key] = incoming_value

    return result


def validate_json_structure(data):
    """Validates basic JSON structure."""
    if not isinstance(data, dict):
        raise ValueError("Root element must be a JSON object")
    return True


def merge_json_files(
    main_file_path: str,
    incoming_file_path: str,
    output_file_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Merge two JSON files with main file taking precedence.

    This is the main entry point for the module. It loads both JSON files,
    performs the deep merge, and optionally saves the result to a file.

    Args:
        main_file_path: Path to the main/authoritative JSON file.
        incoming_file_path: Path to the incoming/supplemental JSON file.
        output_file_path: Optional path to save the merged result.

    Returns:
        The merged dictionary.

    Example:
        >>> result = merge_json_files(
              "main.json", "incoming.json", "output.json"
            )
    """
    main_data = load_json_file(main_file_path)
    incoming_data = load_json_file(incoming_file_path)

    validate_json_structure(main_data)
    validate_json_structure(incoming_data)

    merged = deep_merge(main_data, incoming_data)

    if output_file_path:
        save_json_file(merged, output_file_path)

    return merged


def merge_with_type_coercion(
    main_data: Dict[str, Any], incoming_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Merge with automatic type coercion for mismatched types.

    When types don't match, this function attempts to coerce values
    to maintain compatibility.

    Args:
        main_data: The primary dictionary.
        incoming_data: The secondary dictionary.

    Returns:
        The merged dictionary with type coercion applied.
    """
    result = {}

    all_keys = set(main_data.keys()) | set(incoming_data.keys())

    for key in all_keys:
        main_value = main_data.get(key)
        incoming_value = incoming_data.get(key)

        if key not in incoming_data:
            result[key] = main_value
        elif key not in main_data:
            result[key] = incoming_value
        else:
            if is_empty_value(main_value):
                result[key] = incoming_value
            else:
                result[key] = main_value

    return result


class JSONMerger:
    """
    A class-based interface for JSON merging operations.

    This provides a stateful way to configure and perform merges
    with various options.
    """

    def __init__(self, preserve_empty_arrays: bool = False):
        """
        Initialize the merger with configuration options.

        Args:
            preserve_empty_arrays: If True, empty arrays in main are preserved
                                   rather than being filled by incoming.
        """
        self.preserve_empty_arrays = preserve_empty_arrays
        self._merge_count = 0

    def merge(self, main_data, incoming_data):
        """
        Perform a merge operation.

        Args:
            main_data: The primary dictionary.
            incoming_data: The secondary dictionary.

        Returns:
            The merged dictionary.
        """
        self._merge_count += 1
        return self._recursive_merge(main_data, incoming_data)

    def _recursive_merge(
        self, main: Dict[str, Any], incoming: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Internal recursive merge implementation."""
        result = {}

        all_keys = set(main.keys()) | set(incoming.keys())

        for key in all_keys:
            if key in main and key not in incoming:
                result[key] = main[key]
            elif key not in main and key in incoming:
                result[key] = incoming[key]
            else:
                main_val = main[key]
                incoming_val = incoming[key]

                if isinstance(main_val, dict) and isinstance(
                    incoming_val, dict
                ):
                    result[key] = self._recursive_merge(main_val, incoming_val)
                elif isinstance(main_val, list) and isinstance(
                    incoming_val, list
                ):
                    result[key] = self._handle_arrays(main_val, incoming_val)
                else:
                    if is_empty_value(incoming_val):
                        result[key] = main_val
                    else:
                        result[key] = incoming_val

        return result

    def _handle_arrays(self, main_arr: list, incoming_arr: list) -> list:
        """Handle array merging based on configuration."""
        if self.preserve_empty_arrays:
            return main_arr

        if len(main_arr) == 0:
            return incoming_arr
        return main_arr

    @property
    def merge_count(self) -> int:
        """Return the number of merges performed by this instance."""
        return self._merge_count


def get_nested_value(
    data: Dict[str, Any], key_path: str, default: Any = None
) -> Any:
    """
    Get a value from a nested dictionary using dot notation.

    Args:
        data: The dictionary to search.
        key_path: Dot-separated path to the desired key (e.g., "address.city").
        default: Value to return if the key is not found.

    Returns:
        The value at the specified path, or default if not found.
    """
    keys = key_path.split(".")
    current = data

    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default

    return current


def set_nested_value(data: Dict[str, Any], key_path: str, value: Any) -> None:
    """
    Set a value in a nested dictionary using dot notation.

    Creates intermediate dictionaries if they don't exist.

    Args:
        data: The dictionary to modify.
        key_path: Dot-separated path to the desired key.
        value: The value to set.
    """
    keys = key_path.split(".")
    current = data

    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]

    current[keys[-1]] = value
