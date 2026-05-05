"""Test json_utils.py"""

import json
import os
import tempfile
import unittest

from aind_json_utils_test_repo.json_utils import (
    load_json_file,
    save_json_file,
    validate_json_structure,
)


class TestLoadJsonFile(unittest.TestCase):
    """Tests for load_json_file."""

    def test_load_valid_json(self):
        """Test loading a valid JSON file returns the expected dict."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f: # noqa
            f.write('{"key": "value", "num": 42}')
            f.flush()
            path = f.name
        try:
            result = load_json_file(path)
            self.assertEqual(result, {"key": "value", "num": 42})
        finally:
            os.unlink(path)

    def test_load_file_not_found(self):
        """Test that loading a nonexistent file raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_json_file("nonexistent.json")

    def test_load_invalid_json(self):
        """Test that loading invalid JSON raises JSONDecodeError."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f: # noqa
            f.write("{invalid json}")
            f.flush()
            path = f.name
        try:
            with self.assertRaises(json.JSONDecodeError):
                load_json_file(path)
        finally:
            os.unlink(path)


class TestSaveJsonFile(unittest.TestCase):
    """Tests for save_json_file."""

    def test_save_and_read_back(self):
        """Test that saved data can be read back and matches the original."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            data = {"name": "test", "values": [1, 2, 3]}
            save_json_file(data, path)
            with open(path, "r") as f:
                content = json.load(f)
            self.assertEqual(content, data)
        finally:
            os.unlink(path)

    def test_save_default_indent(self):
        """Test that the default indent of 2 spaces is applied."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_json_file({"a": 1}, path)
            with open(path, "r") as f:
                text = f.read()
            self.assertIn("  ", text)
        finally:
            os.unlink(path)

    def test_save_custom_indent(self):
        """Test that a custom indent of 4 spaces is applied."""
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name
        try:
            save_json_file({"a": 1}, path, indent=4)
            with open(path, "r") as f:
                text = f.read()
            self.assertIn("    ", text)
        finally:
            os.unlink(path)


class TestValidateJsonStructure(unittest.TestCase):
    """Tests for validate_json_structure."""

    def test_valid_dict(self):
        """Test that a valid dict returns True."""
        self.assertTrue(validate_json_structure({"key": "value"}))

    def test_rejects_list(self):
        """Test that a list raises ValueError."""
        with self.assertRaises(ValueError):
            validate_json_structure([1, 2, 3])

    def test_rejects_string(self):
        """Test that a string raises ValueError."""
        with self.assertRaises(ValueError):
            validate_json_structure("not a dict")

    def test_rejects_none(self):
        """Test that None raises ValueError."""
        with self.assertRaises(ValueError):
            validate_json_structure(None)


if __name__ == "__main__":
    unittest.main()
