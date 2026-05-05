# aind-json-utils-test-repo

A small Python utility library for loading, saving, and validating JSON files.

## Features

- **`load_json_file(file_path)`** – Read and parse a JSON file into a Python dictionary.
- **`save_json_file(data, file_path, indent=2)`** – Write a dictionary to a JSON file with configurable indentation.
- **`validate_json_structure(data)`** – Verify that data is a dictionary, raising `ValueError` otherwise.

## Installation

Create a virtual environment, then install the package from the project root:

```bash
pip install -e .
```

To install with development dependencies:

```bash
pip install -e . --group dev
```

> **Note:** The `--group` flag requires pip >= 25.1.

Or, if using `uv`:

```bash
uv sync
```

## Usage

```python
from aind_json_utils_test_repo.json_utils import (
    load_json_file,
    save_json_file,
    validate_json_structure,
)

# Load a JSON file
data = load_json_file("config.json")

# Save a dictionary as JSON
save_json_file({"key": "value"}, "output.json")

# Validate that data is a dict
validate_json_structure(data)
```

## Running Tests

```bash
python -m unittest discover -s tests
```

## License

MIT
