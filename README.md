# Issue: Implement JSON Deep Merge Module with Main File Precedence

**Labels:** `interview-exercise` `code-review` `module`

---

## Summary

Create a module that merges two JSON files using a precedence-based strategy. A designated `main.json` file acts as the authoritative source — its existing values are never overwritten. A second "incoming" JSON file provides supplemental data that fills in missing keys only.

---

## Requirements

### Input
- The module accepts two JSON file paths as input.
- One file is always designated as `main.json` (the primary/authoritative source).
- The other file is the **incoming** JSON (the secondary/supplemental source).

### Merge Behavior

1. **Top-level keys that exist only in `main.json`** → preserved as-is.
2. **Top-level keys that exist only in the incoming JSON** → added to the merged result.
3. **Top-level keys that exist in both files:**
   - If the value in `main.json` is **already populated** (non-null, non-empty), it takes precedence and must **not** be overwritten.
   - If the value in `main.json` is `null`, `""`, `{}`, or `[]` (empty/unset), the incoming value may fill it in.
4. **Nested objects (recursive merge):**
   - When both files have an object at the same key, the merge should recurse into the nested structure and apply the same precedence rules at every level.
   - `main.json` values always win at any depth if they are populated.
5. **Arrays:**
   - If `main.json` has a non-empty array at a given key, it is preserved entirely (no element-level merge).
   - If `main.json` has an empty array and the incoming file has a non-empty one, the incoming array is used.

### Output
- The module returns (or writes) the merged JSON result.

---

## Example

**`main.json`**
```json
{
  "name": "Acme Corp",
  "address": {
    "street": "123 Main St",
    "city": "",
    "state": "WA"
  },
  "tags": ["enterprise"],
  "metadata": {
    "created_by": "admin",
    "notes": null
  },
  "contacts": []
}
```

**`incoming.json`**
```json
{
  "name": "Acme Corporation",
  "address": {
    "street": "456 Oak Ave",
    "city": "Redmond",
    "state": "ME",
    "zip": "98101"
  },
  "tags": ["startup", "west-coast"],
  "metadata": {
    "created_by": "import-script",
    "notes": "Imported from CRM",
    "source": "crm-v2"
  },
  "contacts": [
    { "email": "info@acme.com" }
  ],
  "industry": "Technology"
}
```

**Expected merged result:**
```json
{
  "name": "Acme Corp",
  "address": {
    "street": "123 Main St",
    "city": "Seattle",
    "state": "WA",
    "zip": "98101"
  },
  "tags": ["enterprise"],
  "metadata": {
    "created_by": "admin",
    "notes": "Imported from CRM",
    "source": "crm-v2"
  },
  "contacts": [
    { "email": "info@acme.com" }
  ],
  "industry": "Technology"
}
```
---

## Acceptance Criteria

- [ ] Module reads two JSON files from disk (or accepts two parsed objects).
- [ ] Merge is recursive for nested objects.
- [ ] `main.json` populated values are never overwritten at any depth.
- [ ] Empty/null values in `main.json` are filled by incoming data.
- [ ] Keys unique to either file appear in the final output.
- [ ] Non-empty arrays in `main.json` are preserved without element-level merging.
- [ ] Code handles edge cases: missing files, invalid JSON, deeply nested structures, and mismatched types at the same key.