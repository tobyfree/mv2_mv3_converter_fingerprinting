#!/usr/bin/env python3
import os
import json
import csv
import ast
import re
from collections import defaultdict, Counter

# General Data
#PARENT_DIR = "D:\\extensions\\large-dataset\\V2"
#OUTPUT_CSV = "manifest_differences_general.csv"

# Malicious Dataset
PARENT_DIR = "D:\\extensions\\malicious\\Kapravelos\\V2"
OUTPUT_CSV = "manifest_differences_malicious.csv"

def flatten_manifest(d, parent_key="", sep="."):
    """
    Recursively flattens a manifest dictionary.
    • Applies key mapping (e.g. "browser_action" -> "action")
    • For list values, it now produces a list of individual string entries.
      For example, if a key "key1" has value ["value1", "value2"],
      the result will have: key1: [ "value1", "value2" ].
    • All non-dict, non-list values are converted to lowercased strings.
    """
    items = {}
    # Known key mapping for manifest migration.
    key_mapping = {
        "browser_action": "action",
        "page_action": "action",
        "background.scripts": "background.service_worker"
        # Extend as needed.
    }
    for k, v in d.items():
        # Map the key if needed.
        k = key_mapping.get(k, k)
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_manifest(v, new_key, sep=sep))
        elif isinstance(v, list):
            new_list = []
            for elem in v:
                if isinstance(elem, dict):
                    # For dicts in lists, flatten and join the items in sorted order.
                    flat_elem = flatten_manifest(elem)
                    sorted_items = sorted(flat_elem.items())
                    joined = ", ".join([f"{key}: {value}" for key, value in sorted_items])
                    new_list.append(joined)
                else:
                    new_list.append(str(elem).lower().strip())
            items[new_key] = new_list
        else:
            items[new_key] = str(v).lower().strip()
    return items

def compare_values(v2, v3):
    """
    Compare two values from flattened manifests.
    If both are lists, compare them as sets (order and duplicates are ignored).
    Otherwise, use simple equality.
    """
    if isinstance(v2, list) and isinstance(v3, list):
        return set(v2) == set(v3)
    else:
        return v2 == v3

def compare_manifests(manifest_v2, manifest_v3):
    """
    Compare two manifest dictionaries and return a dict with differences.
    Ignores keys like 'manifest_version' and 'version'.
    Uses the custom flattening (which now produces lists for array values)
    and the custom comparison.
    Returns:
      - 'added': keys present only in V3 with their values.
      - 'removed': keys present only in V2 with their values.
      - 'modified': keys present in both but with different values.
    """
    ignore_keys = {'manifest_version', 'version'}
    flat_v2 = flatten_manifest(manifest_v2)
    flat_v3 = flatten_manifest(manifest_v3)

    for key in ignore_keys:
        flat_v2.pop(key, None)
        flat_v3.pop(key, None)

    diff_result = {'added': {}, 'removed': {}, 'modified': {}}
    keys_v2 = set(flat_v2.keys())
    keys_v3 = set(flat_v3.keys())

    for key in keys_v3 - keys_v2:
        diff_result['added'][key] = flat_v3[key]
    for key in keys_v2 - keys_v3:
        diff_result['removed'][key] = flat_v2[key]
    for key in keys_v2.intersection(keys_v3):
        if not compare_values(flat_v2[key], flat_v3[key]):
            diff_result['modified'][key] = {"v2": flat_v2[key], "v3": flat_v3[key]}
    return diff_result

def process_extensions(parent_dir):
    """
    Process each extension folder in the main folder.
    V2 manifest is expected in:
      <ext_folder>/manifest.json
    V3 manifest is expected in:
      <parent_dir>/converted/<ext_name>_mv3/manifest.json
    Returns a list of dictionaries with diff information.
    """
    results = []
    for ext_name in os.listdir(parent_dir):
        ext_folder = os.path.join(parent_dir, ext_name)
        if os.path.isdir(ext_folder) and ext_name != "converted":
            manifest_v2_path = os.path.join(ext_folder, "manifest.json")
            manifest_v3_path = os.path.join(parent_dir, "converted", ext_name + "_mv3", "manifest.json")
            if os.path.exists(manifest_v2_path) and os.path.exists(manifest_v3_path):
                try:
                    with open(manifest_v2_path, 'r', encoding='utf-8') as f:
                        manifest_v2 = json.load(f)
                    with open(manifest_v3_path, 'r', encoding='utf-8') as f:
                        manifest_v3 = json.load(f)
                except Exception as e:
                    print(f"Error reading manifest files for '{ext_name}': {e}")
                    continue
                diff = compare_manifests(manifest_v2, manifest_v3)
                modified_details_v2 = {key: diff['modified'][key]["v2"] for key in diff['modified']}
                modified_details_v3 = {key: diff['modified'][key]["v3"] for key in diff['modified']}
                result = {
                    'extension': ext_name,
                    'added_keys': ";".join(diff['added'].keys()),
                    'added_details': json.dumps(diff['added'], ensure_ascii=False),
                    'removed_keys': ";".join(diff['removed'].keys()),
                    'removed_details': json.dumps(diff['removed'], ensure_ascii=False),
                    'modified_keys': ";".join(diff['modified'].keys()),
                    'modified_details_v2': json.dumps(modified_details_v2, ensure_ascii=False),
                    'modified_details_v3': json.dumps(modified_details_v3, ensure_ascii=False),
                    'count_added': len(diff['added']),
                    'count_removed': len(diff['removed']),
                    'count_modified': len(diff['modified'])
                }
                results.append(result)
            else:
                print(f"Skipping '{ext_name}': Missing V2 or V3 manifest file.")
    return results

def save_to_csv(results, output_csv):
    fieldnames = [
        'extension',
        'added_keys', 'added_details',
        'removed_keys', 'removed_details',
        'modified_keys', 'modified_details_v2', 'modified_details_v3',
        'count_added', 'count_removed', 'count_modified'
    ]
    try:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for res in results:
                writer.writerow(res)
        print(f"Results successfully saved to {output_csv}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

def main():
    results = process_extensions(PARENT_DIR)
    if results:
        save_to_csv(results, OUTPUT_CSV)
    else:
        print("No valid extensions found or no differences detected.")

if __name__ == "__main__":
    main()
