"""Test json_utils.py"""

import json
import os
import tempfile
import unittest

from aind_json_utils_test_repo.json_utils import (
    deep_merge,
    is_empty_value,
    load_json_file,
    merge_arrays,
    merge_json_files,
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


class TestMergeArrays(unittest.TestCase):
    """Tests for merge_arrays."""

    def test_main_non_empty_is_preserved(self):
        """Test that a non-empty main array is returned unchanged."""
        self.assertEqual(merge_arrays([1, 2], [3, 4]), [3, 4])

    def test_main_empty_uses_incoming(self):
        """Test that an empty main array falls back to the incoming array."""
        self.assertEqual(merge_arrays([], [3, 4]), [3, 4])

    def test_both_empty_returns_empty(self):
        """Test that two empty arrays return an empty array."""
        self.assertEqual(merge_arrays([], []), [])


class TestIsEmptyValue(unittest.TestCase):
    """Tests for is_empty_value."""

    def test_none_is_empty(self):
        """Test that None is considered empty."""
        self.assertTrue(is_empty_value(None))

    def test_empty_string_is_empty(self):
        """Test that an empty string is considered empty."""
        self.assertTrue(is_empty_value(""))

    def test_empty_dict_is_empty(self):
        """Test that an empty dict is considered empty."""
        self.assertTrue(is_empty_value({}))

    def test_empty_list_is_empty(self):
        """Test that an empty list is considered empty."""
        self.assertTrue(is_empty_value([]))

    def test_zero_is_empty(self):
        """Test that 0 is considered empty (falsy)."""
        self.assertTrue(is_empty_value(0))

    def test_false_is_empty(self):
        """Test that False is considered empty (falsy)."""
        self.assertTrue(is_empty_value(False))

    def test_populated_string_is_not_empty(self):
        """Test that a non-empty string is not considered empty."""
        self.assertFalse(is_empty_value("value"))

    def test_populated_dict_is_not_empty(self):
        """Test that a non-empty dict is not considered empty."""
        self.assertFalse(is_empty_value({"a": 1}))

    def test_populated_list_is_not_empty(self):
        """Test that a non-empty list is not considered empty."""
        self.assertTrue(is_empty_value([]))


class TestDeepMerge(unittest.TestCase):
    """Tests for deep_merge."""

    def test_keys_only_in_main_are_preserved(self):
        """Test that keys unique to main_data appear in the merged result."""
        result = deep_merge({"a": 1}, {"b": 2})
        self.assertEqual(result, {"a": 1, "b": 2})

    def test_keys_only_in_incoming_are_added(self):
        """Test that keys unique to incoming_data appear in the merged result."""
        result = deep_merge({"a": 1}, {"b": 2, "c": 3})
        self.assertEqual(result, {"a": 1, "b": 2, "c": 3})

    def test_shared_populated_keys(self):
        """Test that a shared key with both values populated resolves to a single value.""" # noqa
        result = deep_merge({"a": "main"}, {"a": "incoming"})
        self.assertEqual(result, {"a": "main"})

    def test_incoming_fills_empty_main_value(self):
        """Test that an empty main value is filled by incoming value."""
        result = deep_merge({"a": ""}, {"a": "incoming"})
        self.assertEqual(result, {"a": "incoming"})

    def test_nested_dicts_are_merged_recursively(self):
        """Test that nested dictionaries are recursively merged."""
        main = {"outer": {"a": 1, "b": ""}}
        incoming = {"outer": {"b": 2, "c": 3}}
        result = deep_merge(main, incoming)
        self.assertEqual(result, {"outer": {"a": 1, "b": 2, "c": 3}})

    def test_list_values_use_merge_arrays(self):
        """Test that list values follow merge_arrays precedence rules."""
        result = deep_merge({"items": [1, 2]}, {"items": [3, 4]})
        self.assertEqual(result, {"items": [1, 2]})

    def test_empty_list_in_main_is_filled_by_incoming(self):
        """Test that an empty list in main is replaced by incoming list."""
        result = deep_merge({"items": []}, {"items": [3, 4]})
        self.assertEqual(result, {"items": [3, 4]})


class TestMergeJsonFiles(unittest.TestCase):
    """Tests for merge_json_files."""

    def _write_json(self, data):
        """Write data to a temp JSON file and return its path."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        ) as f:
            json.dump(data, f)
            path = f.name
        return path

    def test_merge_without_output(self):
        """Test that merging returns the merged dict when no output path given.""" # noqa
        main_path = self._write_json({"a": 1, "b": ""})
        incoming_path = self._write_json({"b": 2, "c": 3})
        try:
            result = merge_json_files(main_path, incoming_path)
            self.assertEqual(result, {"a": 1, "b": 2, "c": 3})
        finally:
            os.unlink(main_path)
            os.unlink(incoming_path)

    def test_merge_with_output_writes_file(self):
        """Test that the merged result is written to the output path."""
        main_path = self._write_json({"a": 1})
        incoming_path = self._write_json({"b": 2})
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = f.name
        try:
            merge_json_files(main_path, incoming_path, output_path)
            with open(output_path, "r") as f:
                written = json.load(f)
            self.assertEqual(written, {"a": 1, "b": 2})
        finally:
            os.unlink(main_path)
            os.unlink(incoming_path)
            os.unlink(output_path)

    def test_rejects_non_dict_main(self):
        """Test that a non-dict main JSON raises ValueError."""
        main_path = self._write_json([1, 2, 3])
        incoming_path = self._write_json({"a": 1})
        try:
            with self.assertRaises(ValueError):
                merge_json_files(main_path, incoming_path)
        finally:
            os.unlink(main_path)
            os.unlink(incoming_path)

    def test_rejects_non_dict_incoming(self):
        """Test that a non-dict incoming JSON raises ValueError."""
        main_path = self._write_json({"a": 1})
        incoming_path = self._write_json([1, 2, 3])
        try:
            with self.assertRaises(ValueError):
                merge_json_files(main_path, incoming_path)
        finally:
            os.unlink(main_path)
            os.unlink(incoming_path)


if __name__ == "__main__":
    unittest.main()
