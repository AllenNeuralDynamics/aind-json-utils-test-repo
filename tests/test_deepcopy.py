"""
Tests for the deepcopy JSON merge module.
"""

import json
import os
import tempfile
from pathlib import Path

from aind_json_utils_test_repo.deepcopy import (
    JSONMerger,
    deep_merge,
    get_nested_value,
    is_empty_value,
    load_json_file,
    merge_arrays,
    merge_json_files,
    save_json_file,
    set_nested_value,
)


class TestIsEmptyValue:
    """Tests for the is_empty_value function."""

    def test_none_is_empty(self):
        assert is_empty_value(None) is True

    def test_empty_string_is_empty(self):
        assert is_empty_value("") is True

    def test_empty_dict_is_empty(self):
        assert is_empty_value({}) is True

    def test_empty_list_is_empty(self):
        assert is_empty_value([]) is True

    def test_populated_string_not_empty(self):
        assert is_empty_value("hello") is False

    def test_populated_dict_not_empty(self):
        assert is_empty_value({"key": "value"}) is False

    def test_populated_list_not_empty(self):
        assert is_empty_value([1, 2, 3]) is False


class TestMergeArrays:
    """Tests for the merge_arrays function."""

    def test_main_non_empty_preserved(self):
        main = [1, 2, 3]
        incoming = [4, 5, 6]
        result = merge_arrays(main, incoming)
        assert result == [1, 2, 3]

    def test_main_empty_uses_incoming(self):
        main = []
        incoming = [4, 5, 6]
        result = merge_arrays(main, incoming)
        assert result == [4, 5, 6]

    def test_both_empty(self):
        main = []
        incoming = []
        result = merge_arrays(main, incoming)
        assert result == []


class TestDeepMerge:
    """Tests for the deep_merge function."""

    def test_key_only_in_main(self):
        main = {"a": 1}
        incoming = {}
        result = deep_merge(main, incoming)
        assert "a" in result
        assert result["a"] == 1

    def test_key_only_in_incoming(self):
        main = {}
        incoming = {"b": 2}
        result = deep_merge(main, incoming)
        assert "b" in result
        assert result["b"] == 2

    def test_nested_merge(self):
        main = {"outer": {"inner": "main_value"}}
        incoming = {"outer": {"inner": "incoming_value", "extra": "bonus"}}
        result = deep_merge(main, incoming)
        assert result["outer"]["inner"] == "main_value"
        assert result["outer"]["extra"] == "bonus"

    def test_empty_main_value_filled(self):
        main = {"key": ""}
        incoming = {"key": "filled"}
        result = deep_merge(main, incoming)
        assert result["key"] == "filled"

    def test_null_main_value_filled(self):
        main = {"key": None}
        incoming = {"key": "filled"}
        result = deep_merge(main, incoming)
        assert result["key"] == "filled"


class TestJSONMerger:
    """Tests for the JSONMerger class."""

    def test_basic_merge(self):
        merger = JSONMerger()
        main = {"a": 1}
        incoming = {"b": 2}
        result = merger.merge(main, incoming)
        assert result == {"a": 1, "b": 2}

    def test_merge_count_increments(self):
        merger = JSONMerger()
        merger.merge({}, {})
        merger.merge({}, {})
        assert merger.merge_count == 2

    def test_preserve_empty_arrays_option(self):
        merger = JSONMerger(preserve_empty_arrays=True)
        main = {"arr": []}
        incoming = {"arr": [1, 2, 3]}
        result = merger.merge(main, incoming)
        assert result["arr"] == []


class TestFileOperations:
    """Tests for file I/O operations."""

    def test_load_and_save_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            filepath = os.path.join(tmpdir, "test.json")
            data = {"key": "value", "nested": {"inner": 123}}

            save_json_file(data, filepath)
            loaded = load_json_file(filepath)

            assert loaded == data

    def test_merge_json_files_with_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            main_path = os.path.join(tmpdir, "main.json")
            incoming_path = os.path.join(tmpdir, "incoming.json")
            output_path = os.path.join(tmpdir, "output.json")

            save_json_file({"name": "Main"}, main_path)
            save_json_file(
                {"name": "Incoming", "extra": "data"}, incoming_path
            )

            result = merge_json_files(main_path, incoming_path, output_path)

            assert os.path.exists(output_path)


class TestNestedValueHelpers:
    """Tests for get_nested_value and set_nested_value."""

    def test_get_nested_value(self):
        data = {"a": {"b": {"c": "deep"}}}
        assert get_nested_value(data, "a.b.c") == "deep"

    def test_get_nested_value_missing(self):
        data = {"a": 1}
        assert (
            get_nested_value(data, "b.c", default="not found") == "not found"
        )

    def test_set_nested_value(self):
        data = {}
        set_nested_value(data, "a.b.c", "value")
        assert data["a"]["b"]["c"] == "value"


class TestIntegration:
    """Integration tests using the example from requirements."""

    def test_full_example_from_requirements(self):
        """Test the exact example provided in the requirements document."""
        main = {
            "name": "Acme Corp",
            "address": {"street": "123 Main St", "city": "", "state": "WA"},
            "tags": ["enterprise"],
            "metadata": {"created_by": "admin", "notes": None},
            "contacts": [],
        }

        incoming = {
            "name": "Acme Corporation",
            "address": {
                "street": "456 Oak Ave",
                "city": "Seattle",
                "state": "OR",
                "zip": "98101",
            },
            "tags": ["startup", "west-coast"],
            "metadata": {
                "created_by": "import-script",
                "notes": "Imported from CRM",
                "source": "crm-v2",
            },
            "contacts": [{"email": "info@acme.com"}],
            "industry": "Technology",
        }

        expected = {
            "name": "Acme Corp",
            "address": {
                "street": "123 Main St",
                "city": "Seattle",
                "state": "WA",
                "zip": "98101",
            },
            "tags": ["enterprise"],
            "metadata": {
                "created_by": "admin",
                "notes": "Imported from CRM",
                "source": "crm-v2",
            },
            "contacts": [{"email": "info@acme.com"}],
            "industry": "Technology",
        }

        result = deep_merge(main, incoming)

        assert result == expected
