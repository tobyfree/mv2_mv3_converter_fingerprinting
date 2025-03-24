#!/usr/bin/env python3
import os
import json
import csv
import argparse
from tqdm import tqdm
from collections import defaultdict

# ========================
# Flatten Manifest Helpers
# ========================
def flatten_manifest(d, parent_key="", sep="."):
    key_mapping = {
        "browser_action": "action",
        "page_action": "action",
        "background.scripts": "background.service_worker"
    }
    items = {}
    for k, v in d.items():
        k = key_mapping.get(k, k)
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_manifest(v, new_key, sep=sep))
        elif isinstance(v, list):
            new_list = []
            for elem in v:
                if isinstance(elem, dict):
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
    if isinstance(v2, list) and isinstance(v3, list):
        return set(v2) == set(v3)
    return v2 == v3

def compare_manifests(manifest_v2, manifest_v3):
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

# ========================
# Core Functionality
# ========================
def process_extensions(parent_dir):
    results = []
    for ext_name in tqdm(os.listdir(parent_dir), desc="Comparing manifests", unit="ext"):
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

# ========================
# Main (argparse enabled)
# ========================
def main(args=None):
    parser = argparse.ArgumentParser(description="Compare V2 and V3 manifest files across extensions.")
    parser.add_argument("--input_dir", help="Path to the parent directory containing extensions", default="D:\\extensions\\large-dataset\\V2")
    parser.add_argument("--output_csv", help="Path to output CSV file", default="manifest_differences_general.csv")
    parsed = parser.parse_args(args)

    results = process_extensions(parsed.input_dir)
    if results:
        save_to_csv(results, parsed.output_csv)
    else:
        print("No valid extensions found or no differences detected.")

if __name__ == "__main__":
    main()
