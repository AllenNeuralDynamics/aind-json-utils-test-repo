import json
from typing import Dict, Any


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


def save_json_file(
    data: Dict[str, Any], file_path: str, indent: int = 2
) -> None:
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