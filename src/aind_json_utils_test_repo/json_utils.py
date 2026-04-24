"""json utility module"""

import json
from typing import Any, Dict, Optional


def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a JSON file from disk.

    Parameters
    ----------
    file_path : str
        Path to the JSON file.

    Returns
    -------
    Dict[str, Any]
        Parsed JSON as a dictionary.

    Raises
    ------
    FileNotFoundError
        If the file doesn't exist.
    json.JSONDecodeError
        If the file contains invalid JSON.
    """
    with open(file_path, "r") as f:
        return json.load(f)


def save_json_file(data: Dict[str, Any], file_path: str, indent: int = 2) -> None:  # noqa
    """
    Save a dictionary as a JSON file.

    Parameters
    ----------
    data : Dict[str, Any]
        The dictionary to save.
    file_path : str
        Path where the file should be saved.
    indent : int
        Number of spaces for indentation (default: 2).
    """
    with open(file_path, "w") as f:
        json.dump(data, f, indent=indent)


def validate_json_structure(data: Any):
    """
    Validates basic JSON structure.

    Parameters
    ----------
    data: Any
        data to validate
    """
    if not isinstance(data, dict):
        raise ValueError("Data structure must be type Dict")
    return True


def merge_arrays(main_array, incoming_array):
    """
    Merge two arrays according to precedence rules.

    If main array is non-empty, it is preserved entirely.
    If main array is empty, incoming array is used.

    Parameters
    ----------
    main_array
        The authoritative/primary array.
    incoming_array
        The supplemental/secondary array.

    Returns
    -------
    list
        The merged array.
    """
    if len(main_array) > 0:
        return main_array
    return incoming_array


def deep_merge(main_data: Dict[str, Any], incoming_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Recursively merge two dictionaries with main_data taking precedence.

    Rules:
    - Keys only in main_data are preserved
    - Keys only in incoming_data are added
    - For shared keys, main_data value wins if it's populated
    - Empty values in main_data can be filled by incoming_data
    - Nested objects are merged recursively

    Parameters
    ----------
    main_data : Dict[str, Any]
        The authoritative/primary dictionary.
    incoming_data : Dict[str, Any]
        The supplemental/secondary dictionary.

    Returns
    -------
    Dict[str, Any]
        The merged dictionary.
    """
    result = incoming_data.copy()

    for key, main_value in main_data.items():
        if key not in incoming_data:
            result[key] = main_value
        else:
            incoming_value = incoming_data[key]

            if isinstance(main_value, dict) and isinstance(incoming_value, dict):
                result[key] = deep_merge(main_value, incoming_value)
            elif isinstance(main_value, list) and isinstance(incoming_value, list):
                result[key] = merge_arrays(main_value, incoming_value)
            else:
                if is_empty_value(incoming_value):
                    result[key] = main_value
                else:
                    result[key] = incoming_value

    return result


def is_empty_value(value: Any) -> bool:
    """
    Check if a value should be considered "empty" for merge purposes.

    Empty values include: None, empty string, empty dict, empty list.

    Parameters
    ----------
    value : Any
        The value to check.

    Returns
    -------
    bool
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


def merge_json_files(
    main_file_path: str, incoming_file_path: str, output_file_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Merge two JSON files with main file taking precedence.

    This is the main entry point for the module. It loads both JSON files,
    performs the deep merge, and optionally saves the result to a file.

    Parameters
    ----------
    main_file_path : str
        Path to the main/authoritative JSON file.
    incoming_file_path : str
        Path to the incoming/supplemental JSON file.
    output_file_path : Optional[str]
        Optional path to save the merged result.

    Returns
    -------
    Dict[str, Any]
        The merged dictionary.

    Examples
    --------
    >>> result = merge_json_files("main.json", "incoming.json", "output.json")
    """
    main_data = load_json_file(main_file_path)
    incoming_data = load_json_file(incoming_file_path)

    validate_json_structure(main_data)
    validate_json_structure(incoming_data)

    merged = deep_merge(main_data, incoming_data)

    if output_file_path:
        save_json_file(merged, output_file_path)

    return merged
